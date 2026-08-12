from langchain_core.messages import AIMessage

from src.state.state import AgentState


def finalize_transaction_node(state: AgentState) -> dict:
    transaction = state.get("transaction") or {}
    customer = state.get("customer") or {}
    items = transaction.get("items", [])

    if not items:
        return {
            "messages": [AIMessage(content="No tienes productos en tu pedido para confirmar.")]
        }

    lines = ["📋 Resumen de tu pedido:"]
    total = 0.0

    for item in items:
        qty = item.get("quantity") or 1
        price = float(item.get("unit_price") or 0)
        subtotal = qty * price
        total += subtotal
        variant = f" ({item['variant_name']})" if item.get("variant_name") else ""
        lines.append(f"- {qty}x {item['product_name']}{variant}: ${subtotal:,.0f}")

    lines.append(f"\n💰 Total: ${total:,.0f}")

    if customer.get("address"):
        lines.append(f"📍 Dirección: {customer['address']}")

    if customer.get("payment_method"):
        lines.append(f"💳 Pago: {customer['payment_method']}")

    lines.append("\n✅ ¡Pedido confirmado! Gracias por tu compra.")

    return {
        "messages": [AIMessage(content="\n".join(lines))],
        "transaction": {**transaction, "is_complete": True}
    }
