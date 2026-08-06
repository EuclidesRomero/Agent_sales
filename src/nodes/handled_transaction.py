from typing import Literal, Optional

from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage

from src.state.state import AgentState
from src.app.repositories.catalog_repository import search_catalog
from src.app.database import async_session_maker
from src.app.models import Business
from src.model.model import llm

class OrderExtraction(BaseModel):
    message_type: Literal["provide_info", "status_query", "other"] = Field(
        description="Tipo de mensaje del cliente dentro del flujo de compra. "
        "'provide_info' si está dando datos del pedido (producto, cantidad, "
        "dirección, método de pago). 'status_query' si está preguntando qué "
        "ha pedido hasta el momento, o pidiendo un resumen de su pedido "
        "actual. 'other' para cualquier otro caso."
    )
    product_name: Optional[str] = Field(
        description="Nombre del producto o servicio que el cliente quiere, tal "
        "como lo menciona en su mensaje (ej: 'torta de chocolate', 'decoración "
        "personalizada'). Si el cliente no menciona ningún producto en este "
        "mensaje puntual, deja este campo como null -- no asumas ni reutilices "
        "un producto mencionado en un turno anterior."
    )
    quantity: Optional[int] = Field(
        description="Cantidad de unidades que el cliente quiere, incluso si la "
        "escribió en palabras (ej: 'dos' -> 2). Si el cliente no menciona "
        "ninguna cantidad en el mensaje actual, deja este campo como null -- "
        "no asumas 1 por defecto."
    )
    address: Optional[str] = Field(
        description="Dirección de entrega que el cliente proporciona en este "
        "mensaje (ej: 'Cra 45 #12-30'). Si el cliente no menciona ninguna "
        "dirección en este mensaje puntual, deja este campo como null."
    )
    payment_method: Optional[str] = Field(
        description="Método de pago que el cliente menciona (ej: 'efectivo', "
        "'tarjeta', 'transferencia', 'Nequi'). Si no lo menciona en este "
        "mensaje puntual, deja este campo como null."
    )

def _match_by_words(text: str, candidates: list, name_key: str = "name") -> Optional[object]:
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


def _extract_quantity_fallback(text: str) -> Optional[int]:
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


def _create_order_item(product_name, resource_id, variant_id, variant_name, quantity, unit_price) -> dict:
    return {
        "product_name": product_name,
        "resource_id": resource_id,
        "variant_id": variant_id,
        "variant_name": variant_name,
        "quantity": quantity,
        "unit_price": unit_price,
    }


def _add_item_to_transaction(state: AgentState, item: dict) -> dict:
    transaction = dict(state.get("transaction") or {
        "items": [], "is_complete": False, "requires_human": False, "request_id": None
    })
    transaction["items"] = transaction["items"] + [item]
    return transaction


def _missing_fields(transaction: dict, customer: dict) -> list[str]:
    missing = []
    if not transaction.get("items"):
        missing.append("qué producto quieres pedir")
    else:
        for item in transaction["items"]:
            if not item.get("quantity"):
                missing.append("la cantidad")
                break
    if not customer.get("address"):
        missing.append("tu dirección de entrega")
    if not customer.get("payment_method"):
        missing.append("tu método de pago")
    return missing


def _finalize_turn(transaction: dict, customer: dict, product_query: dict, lead_message: Optional[str] = None) -> dict:
    missing = _missing_fields(transaction, customer)

    if not missing:
        transaction["is_complete"] = True
        closing = "¡Perfecto! Ya tengo todo tu pedido, dame un momento para confirmarlo."
    else:
        closing = f"Ahora dime {missing[0]}."

    content = f"{lead_message} {closing}" if lead_message else closing

    return {
        "transaction": transaction,
        "customer": customer,
        "product_query": product_query,
        "messages": [AIMessage(content=content)],
    }


def _build_order_summary(transaction: dict, customer: dict) -> str:
    items = transaction.get("items", [])
    if not items:
        return "Todavía no has agregado ningún producto a tu pedido."

    lines = ["Hasta el momento tienes:"]
    total = 0.0
    for item in items:
        qty = item.get("quantity") or 1
        price = float(item.get("unit_price") or 0)
        subtotal = qty * price
        total += subtotal
        variant = f" ({item['variant_name']})" if item.get("variant_name") else ""
        lines.append(f"- {qty}x {item['product_name']}{variant}: ${subtotal:,.0f}")

    lines.append(f"\nTotal: ${total:,.0f}")
    if customer.get("address"):
        lines.append(f"Dirección: {customer['address']}")
    if customer.get("payment_method"):
        lines.append(f"Pago: {customer['payment_method']}")

    return "\n".join(lines)


async def _get_accepted_payment_methods(business_id: int) -> list[str]:
    async with async_session_maker() as db:
        business = await db.get(Business, business_id)
        policies = (business.policies or {}) if business else {}
        return policies.get("metodos_pago", [])


async def transaction_node(state: AgentState) -> dict:
    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    last_message = human_messages[-1] if human_messages else None

    if last_message is None:
        return {"messages": [AIMessage(content="¿Podrías repetir tu pedido?")]}

    business_id = int(state["business_id"])
    customer = dict(state.get("customer") or {})
    product_query = state.get("product_query") or {}

    if product_query.get("results"):
        matched = _match_by_words(last_message.content, product_query["results"], name_key="name")

        if matched is None:
            options = ", ".join(c["name"] for c in product_query["results"])
            return {"messages": [AIMessage(
                content=f"No logré identificar cuál prefieres. Opciones: {options}. ¿Cuál eliges?"
            )]}

        quantity = _extract_quantity_fallback(last_message.content) or 1
        selected_product = product_query.get("selected_product")

        if selected_product:
            item = _create_order_item(
                selected_product["name"], selected_product["resource_id"],
                matched["variant_id"], matched["name"], quantity, matched["price"],
            )
            transaction = _add_item_to_transaction(state, item)
            empty_query = {"query": None, "results": [], "selected_product": None}
            return _finalize_turn(
                transaction, customer, empty_query,
                lead_message=f"Agregué {selected_product['name']} ({matched['name']}) a tu pedido.",
            )

        variants = matched.get("variants", [])
        if len(variants) > 1:
            options = ", ".join(v["name"] for v in variants)
            new_query = {
                "query": matched["name"],
                "selected_product": {"resource_id": matched["resource_id"], "name": matched["name"]},
                "results": variants,
            }
            return {
                "product_query": new_query,
                "messages": [AIMessage(content=f"¿Qué variante de {matched['name']} prefieres? Opciones: {options}")],
            }

        variant = variants[0]
        item = _create_order_item(
            matched["name"], matched["resource_id"],
            variant["variant_id"], variant["name"], quantity, variant["price"],
        )
        transaction = _add_item_to_transaction(state, item)
        empty_query = {"query": None, "results": [], "selected_product": None}
        return _finalize_turn(
            transaction, customer, empty_query,
            lead_message=f"Agregué {matched['name']} ({variant['name']}) a tu pedido.",
        )

    structured_llm = llm.with_structured_output(OrderExtraction, method="function_calling")
    extraction = await structured_llm.ainvoke([last_message])

    transaction = dict(state.get("transaction") or {
        "items": [], "is_complete": False, "requires_human": False, "request_id": None
    })

    if extraction.message_type == "status_query":
        summary = _build_order_summary(transaction, customer)
        return {"messages": [AIMessage(content=summary)]}

    if extraction.address:
        customer["address"] = extraction.address

    if extraction.payment_method:
        accepted = await _get_accepted_payment_methods(business_id)
        accepted_lower = [m.lower() for m in accepted]
        if accepted_lower and extraction.payment_method.lower() not in accepted_lower:
            accepted_text = ", ".join(accepted)
            return {
                "customer": customer,
                "messages": [AIMessage(
                    content=f"No aceptamos {extraction.payment_method}. Métodos disponibles: {accepted_text}. ¿Cuál usarías?"
                )],
            }
        customer["payment_method"] = extraction.payment_method

    if not extraction.product_name:
        empty_query = {"query": None, "results": [], "selected_product": None}
        return _finalize_turn(transaction, customer, empty_query)

    async with async_session_maker() as db:
        matched_products = await search_catalog(db, business_id=business_id, search_query=extraction.product_name)

    if not matched_products:
        return {
            "customer": customer,
            "messages": [AIMessage(
                content=f"No encontré '{extraction.product_name}'. ¿Podrías confirmarme el nombre del producto?"
            )],
        }

    if len(matched_products) > 1:
        results = [
            {
                "resource_id": r.id,
                "name": r.name,
                "variants": [{"variant_id": v.id, "name": v.name, "price": float(v.price)} for v in r.variants],
            }
            for r in matched_products
        ]
        options = ", ".join(r.name for r in matched_products)
        new_query = {"query": extraction.product_name, "results": results, "selected_product": None}
        return {
            "customer": customer,
            "product_query": new_query,
            "messages": [AIMessage(content=f"Encontré varias opciones: {options}. ¿Cuál prefieres?")],
        }

    resource = matched_products[0]

    if len(resource.variants) > 1:
        matched_variant = _match_by_words(last_message.content, resource.variants, name_key="name")

        if matched_variant:
            item = _create_order_item(
                resource.name, resource.id, matched_variant.id, matched_variant.name,
                extraction.quantity or 1, matched_variant.price,
            )
            transaction = _add_item_to_transaction(state, item)
            empty_query = {"query": None, "results": [], "selected_product": None}
            return _finalize_turn(
                transaction, customer, empty_query,
                lead_message=f"Agregué {resource.name} ({matched_variant.name}) a tu pedido.",
            )

        results = [{"variant_id": v.id, "name": v.name, "price": float(v.price)} for v in resource.variants]
        options = ", ".join(v["name"] for v in results)
        new_query = {
            "query": extraction.product_name,
            "selected_product": {"resource_id": resource.id, "name": resource.name},
            "results": results,
        }
        return {
            "customer": customer,
            "product_query": new_query,
            "messages": [AIMessage(content=f"¿Qué variante de {resource.name} prefieres? Opciones: {options}")],
        }

    variant = resource.variants[0]
    item = _create_order_item(
        resource.name, resource.id, variant.id, variant.name,
        extraction.quantity or 1, variant.price,
    )
    transaction = _add_item_to_transaction(state, item)
    empty_query = {"query": None, "results": [], "selected_product": None}
    return _finalize_turn(
        transaction, customer, empty_query,
        lead_message=f"Agregué {resource.name} ({variant.name}) a tu pedido.",
    )