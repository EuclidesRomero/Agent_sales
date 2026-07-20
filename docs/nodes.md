# Nodes

Este documento describe los nodos que conforman el flujo del agente conversacional.

Cada nodo posee una única responsabilidad y puede leer o modificar el estado de la conversación. Los nodos no interactúan directamente con bases de datos o APIs; toda comunicación con sistemas externos se realiza mediante herramientas (Tools).

---

# Receive User Message

## Descripción

Representa el punto de entrada del agente.

Recibe el mensaje enviado por el usuario, construye o recupera el estado de la conversación y da inicio a la ejecución del flujo.

---

## Responsabilidades

- Recibir el mensaje del usuario.
- Recuperar el historial de conversación.
- Inicializar el AgentState.
- Iniciar la ejecución del grafo.

---

## Entradas

- Mensaje del usuario.
- Identificador de la conversación.
- Identificador del cliente.

---

## Salidas

- AgentState actualizado.

---

## Herramientas

Ninguna.

---

## Nodo siguiente

- Handle Intent

---

# Handle Intent

## Descripción

Analiza el mensaje del usuario para determinar cuál es su intención principal.

Este nodo representa el punto de decisión del agente y define qué camino seguirá la conversación.

---

## Responsabilidades

- Analizar la intención del usuario.
- Clasificar la consulta.
- Decidir el siguiente nodo del flujo.

---

## Entradas

- Historial de mensajes.
- Contexto de la conversación.

---

## Salidas

- Intención detectada.
- Actualización del estado.

---

## Herramientas

Ninguna.

---

## Posibles transiciones

- Business Information
- Product & Service Knowledge
- Handle Transaction

---

# Business Information

## Descripción

Gestiona consultas relacionadas con la información institucional del negocio.

---

## Responsabilidades

Responder preguntas relacionadas con:

- Horarios.
- Dirección.
- Redes sociales.
- Teléfonos.
- Cobertura.
- Políticas generales.

---

## Entradas

- Intención detectada.
- Estado de la conversación.

---

## Salidas

- Respuesta al usuario.

---

## Herramientas

- get_business_information()

---

## Nodo siguiente

END

---

# Product & Service Knowledge

## Descripción

Gestiona consultas relacionadas con los productos o servicios ofrecidos por el negocio.

---

## Responsabilidades

Responder preguntas como:

- Productos disponibles.
- Precios.
- Ingredientes.
- Características.
- Disponibilidad.
- Promociones.

---

## Entradas

- Intención detectada.
- Estado actual.

---

## Salidas

- Información solicitada.

---

## Herramientas

- search_catalog()
- get_product_details()
- check_stock()

---

## Nodo siguiente

END

---

# Handle Transaction

## Descripción

Gestiona conversaciones donde existe una intención de compra.

Este nodo recopila toda la información necesaria para construir una solicitud de pedido.

---

## Responsabilidades

Solicitar y validar información como:

- Producto.
- Cantidad.
- Fecha.
- Dirección.
- Personalización.
- Datos del cliente.

Actualizar continuamente el estado del pedido durante la conversación.

---

## Entradas

- Estado actual.
- Historial de conversación.

---

## Salidas

- Pedido parcialmente o completamente construido.

---

## Herramientas

- create_customer_request()
- save_order()

---

## Nodo siguiente

- Finalize Transaction

---

# Finalize Transaction

## Descripción

Realiza el cierre de la interacción antes de transferir la conversación a un asesor humano.

---

## Responsabilidades

- Mostrar un resumen del pedido.
- Solicitar confirmación.
- Permitir correcciones.
- Marcar la conversación como lista para transferencia.

---

## Entradas

- Pedido completo.
- Estado de la conversación.

---

## Salidas

- Pedido confirmado.
- Estado listo para transferencia.

---

## Herramientas

Ninguna.

---

## Nodo siguiente

- Human Assistance

---

# Human Assistance

## Descripción

Representa la entrega de la conversación a un asesor humano.

El agente finaliza su participación y el proceso continúa de forma manual.

---

## Responsabilidades

- Finalizar la conversación automática.
- Entregar el contexto recopilado.
- Finalizar la ejecución del agente.

---

## Entradas

- Estado completo de la conversación.
- Información del pedido.

---

## Salidas

- Conversación transferida.

---

## Herramientas

Ninguna (la transferencia será realizada por la infraestructura del sistema).

---

## Nodo siguiente

END