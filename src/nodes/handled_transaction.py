import json

from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from src.state.state import AgentState
from src.app.repositories.catalog_repository import search_catalog, get_product_details
from src.app.database import async_session_maker
from src.app.models import Business
from src.model.model import llm


def _match_by_words(text: str, candidates: list, name_key: str = "name"):
    text_words = set(text.lower().split())
    scored = []
    for c in candidates:
        name = c[name_key] if isinstance(c, dict) else getattr(c, name_key)
        candidate_words = set(name.lower().split())
        overlap = text_words & candidate_words
        if overlap:
            scored.append((len(overlap), c))
    if not scored:
        return None
    scored.sort(key=lambda x: -x[0])
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        return None
    return scored[0][1]


def _extract_quantity_fallback(text: str):
    words_to_num = {
        "un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
        "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    }
    for word in text.lower().split():
        if word.isdigit():
            return int(word)
        if word in words_to_num:
            return words_to_num[word]
    return None


async def _get_accepted_payment_methods(business_id: int) -> list[str]:
    async with async_session_maker() as db:
        business = await db.get(Business, business_id)
        policies = (business.policies or {}) if business else {}
        return policies.get("metodos_pago", [])


async def _resolve_product_logic(business_id: int, query: str) -> str:
    async with async_session_maker() as db:
        matched = await search_catalog(db, business_id=business_id, search_query=query)
        if not matched:
            all_products = await search_catalog(db, business_id=business_id)
            fallback = _match_by_words(query, all_products, name_key="name")
            if fallback is not None:
                matched = [fallback]

    if not matched:
        return json.dumps({"not_found": True, "query": query})

    if len(matched) > 1:
        options = [{"resource_id": r.id, "name": r.name} for r in matched]
        return json.dumps({"ambiguous": True, "options": options})

    resource = matched[0]

    if len(resource.variants) > 1:
        variant_match = _match_by_words(query, resource.variants, name_key="name")
        if variant_match is not None:
            return json.dumps({
                "resolved": True,
                "resource_id": resource.id,
                "product_name": resource.name,
                "variant_id": variant_match.id,
                "variant_name": variant_match.name,
                "unit_price": float(variant_match.price),
            })

        options = [{"variant_id": v.id, "name": v.name, "price": float(v.price)} for v in resource.variants]
        return json.dumps({
            "needs_variant": True,
            "resource_id": resource.id,
            "product_name": resource.name,
            "options": options,
        })

    variant = resource.variants[0]
    return json.dumps({
        "resolved": True,
        "resource_id": resource.id,
        "product_name": resource.name,
        "variant_id": variant.id,
        "variant_name": variant.name,
        "unit_price": float(variant.price),
    })


def _add_item_logic(context: dict, resource_id: int, variant_id: int, variant_name: str,
                     product_name: str, unit_price: float, quantity: int = 1) -> str:
    item = {
        "product_name": product_name,
        "resource_id": resource_id,
        "variant_id": variant_id,
        "variant_name": variant_name,
        "quantity": quantity,
        "unit_price": unit_price,
    }
    context["transaction"]["items"] = context["transaction"]["items"] + [item]
    return json.dumps({"added": True, "item": item})


def _set_address_logic(context: dict, address: str) -> str:
    context["customer"]["address"] = address
    return json.dumps({"address_set": True, "address": address})


async def _set_payment_method_logic(context: dict, business_id: int, payment_method: str) -> str:
    accepted = await _get_accepted_payment_methods(business_id)
    accepted_lower = [m.lower() for m in accepted]

    if accepted_lower and payment_method.lower() not in accepted_lower:
        return json.dumps({
            "accepted": False,
            "reason": "not_supported",
            "available_methods": accepted,
        })

    context["customer"]["payment_method"] = payment_method
    return json.dumps({"accepted": True, "payment_method": payment_method})


def _get_order_summary_logic(context: dict) -> str:
    transaction = context["transaction"]
    customer = context["customer"]

    missing = []
    if not transaction["items"]:
        missing.append("producto")
    else:
        for item in transaction["items"]:
            if not item.get("quantity"):
                missing.append("cantidad")
                break
    if not customer.get("address"):
        missing.append("direccion de entrega")
    if not customer.get("payment_method"):
        missing.append("metodo de pago")

    total = sum(
        (item.get("quantity") or 1) * float(item.get("unit_price") or 0)
        for item in transaction["items"]
    )

    return json.dumps({
        "items": transaction["items"],
        "address": customer.get("address"),
        "payment_method": customer.get("payment_method"),
        "total": total,
        "missing_fields": missing,
        "is_complete": len(missing) == 0,
    })


async def transaction_node(state: AgentState) -> dict:
    context = {
        "transaction": dict(state.get("transaction") or {
            "items": [], "is_complete": False, "requires_human": False, "request_id": None
        }),
        "customer": dict(state.get("customer") or {}),
    }
    business_id = int(state["business_id"])


    @tool
    async def resolve_product(query: str) -> str:
        """
        Busca un producto o servicio en el catálogo del negocio a partir de lo
        que el cliente mencionó (puede ser el nombre completo, parcial, o
        mezclado con el nombre de una variante, ej: "hamburguesa clásica
        simple" o solo "la doble").

        Devuelve un JSON con uno de estos casos:
        - resolved: true -- ya se identificó un único producto y una única
          variante, con su resource_id y variant_id listos para usar en
          add_item_to_order.
        - needs_variant: true -- se identificó el producto, pero tiene varias
          variantes y no se pudo determinar cuál. Pregúntale al cliente cuál
          prefiere, usando la lista de "options".
        - ambiguous: true -- hay varios productos distintos que calzan con la
          búsqueda. Pregúntale al cliente cuál, usando la lista de "options".
        - not_found: true -- no existe nada parecido en el catálogo.
        """
        return await _resolve_product_logic(business_id, query)

    @tool
    async def add_item_to_order(resource_id: int, variant_id: int, variant_name: str,
        product_name: str, unit_price: float, quantity: int = 1) -> str:
        """
        Agrega un ítem al pedido en curso. SIEMPRE debes haber llamado antes a
        resolve_product para obtener resource_id, variant_id, variant_name,
        product_name y unit_price reales -- nunca inventes estos valores.

        Args:
            resource_id: id del producto, obtenido de resolve_product.
            variant_id: id de la variante específica, obtenido de resolve_product.
            variant_name: nombre de la variante, obtenido de resolve_product.
            product_name: nombre del producto, obtenido de resolve_product.
            unit_price: precio de la variante, obtenido de resolve_product.
            quantity: cantidad que el cliente quiere. Si no lo dijo explícitamente, usa 1.
        """
        return _add_item_logic(context, resource_id, variant_id, variant_name, product_name, unit_price, quantity)

    @tool
    async def set_delivery_address(address: str) -> str:
        """
        Guarda la dirección de entrega que el cliente proporcionó para el pedido.
        """
        return _set_address_logic(context, address)

    @tool
    async def set_payment_method(payment_method: str) -> str:
        """
        Intenta guardar el método de pago que el cliente mencionó (ej:
        'efectivo', 'tarjeta', 'transferencia', 'Nequi'). Valida contra los
        métodos que acepta el negocio -- si devuelve accepted: false, informa
        al cliente qué métodos sí están disponibles (available_methods) y
        pídele que elija uno de esos, SIN guardar el que había mencionado.
        """
        return await _set_payment_method_logic(context, business_id, payment_method)

    @tool
    async def get_order_summary() -> str:
        """
        Devuelve el estado actual del pedido: ítems agregados, dirección,
        método de pago, total, qué campos faltan (missing_fields), y si el
        pedido ya está completo (is_complete). Úsala cuando el cliente
        pregunte qué ha pedido hasta el momento, o para revisar tú mismo qué
        falta antes de responder.
        """
        return _get_order_summary_logic(context)

    tools = [resolve_product, add_item_to_order, set_delivery_address, set_payment_method, get_order_summary]
    llm_with_tools = llm.bind_tools(tools)
    
    messages = [m for m in state["messages"]]
    
    while True:
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            break
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            tool_func = next((t for t in tools if t.name == tool_name), None)
            if tool_func:
                result = await tool_func.ainvoke(tool_args)
                tool_message = ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
                messages.append(tool_message)
    
    return {
        "messages": messages,
        "transaction": context["transaction"],
        "customer": context["customer"],
    }