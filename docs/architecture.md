# Arquitectura del Sistema

## Visión general

El sistema está compuesto por un agente conversacional basado en LangGraph cuyo objetivo es atender automáticamente las consultas de clientes de diferentes tipos de negocio mediante WhatsApp o Telegram.

La arquitectura está diseñada para ser desacoplada del dominio del negocio, permitiendo reutilizar el mismo flujo conversacional para diferentes empresas mediante la configuración de herramientas y fuentes de información específicas.

---

# Arquitectura General

```
Cliente (WhatsApp / Telegram)
            │
            ▼
      Webhook / Backend
            │
            ▼
      LangGraph Agent
            │
 ┌──────────┼──────────┐
 │          │          │
State     Nodes      Tools
 │                     │
 │                     ▼
 │             Base de datos
 │             APIs internas
 │             Servicios externos
 ▼
Respuesta al usuario
```

---

# Componentes

## Cliente

Es el canal de comunicación con el usuario final.

Responsabilidades:

- Enviar mensajes.
- Recibir respuestas.
- Mantener la conversación.

Canales soportados:

- WhatsApp
- Telegram

---

## Backend

El backend actúa como punto de entrada del sistema.

Responsabilidades:

- Recibir mensajes desde el canal.
- Crear o recuperar la conversación.
- Construir el estado inicial.
- Ejecutar el agente.
- Enviar la respuesta al usuario.

Tecnología propuesta:

- Python
- FastAPI

---

## Agente (LangGraph)

Representa el núcleo del sistema.

Su responsabilidad es decidir cómo atender cada mensaje recibido.

No contiene lógica de acceso a bases de datos ni integraciones externas; dichas responsabilidades son delegadas a herramientas especializadas.

El flujo del agente está compuesto por varios nodos que colaboran para resolver la conversación.

---

# Flujo del agente

```
START

↓

Receive User Message

↓

Handle Intent

├── Business Information

├── Product & Service Knowledge

└── Handle Transaction

↓

Finalize Transaction

↓

Human Assistance

↓

END
```

---

# Nodos

## Receive User Message

Punto de entrada del agente.

Recibe el mensaje enviado por el usuario y lo incorpora al estado de la conversación.

---

## Handle Intent

Nodo encargado de interpretar la intención del usuario.

Según el contexto de la conversación determina qué camino debe seguir el flujo.

Posibles rutas:

- Información del negocio.
- Consulta de productos o servicios.
- Inicio o continuación de una transacción.

---

## Business Information

Gestiona consultas relacionadas con información institucional del negocio.

Ejemplos:

- Horarios.
- Dirección.
- Redes sociales.
- Métodos de contacto.
- Cobertura de domicilios.

Este nodo utiliza herramientas especializadas para consultar la información correspondiente.

---

## Product & Service Knowledge

Gestiona preguntas relacionadas con los productos o servicios ofrecidos por el negocio.

Ejemplos:

- Catálogo.
- Precios.
- Disponibilidad.
- Ingredientes.
- Características.
- Promociones.

La información es obtenida mediante herramientas configuradas para cada empresa.

---

## Handle Transaction

Gestiona conversaciones donde existe intención de compra.

Responsabilidades:

- Recopilar información del pedido.
- Solicitar datos faltantes.
- Validar información.
- Construir el pedido.

Este nodo representa el estado transaccional de la conversación.

---

## Finalize Transaction

Una vez recopilada toda la información necesaria:

- Genera un resumen del pedido.
- Permite al usuario confirmar o modificar información.
- Prepara la transferencia al asesor humano.

---

## Human Assistance

Último nodo del flujo.

Su responsabilidad es entregar al asesor humano toda la información recopilada durante la conversación para continuar el proceso comercial.

---

# State

El agente comparte un único estado durante toda la ejecución.

Cada nodo puede:

- Leer información existente.
- Actualizar información.
- Agregar nuevos datos.

La definición completa del estado se encuentra en:

```

docs/state.md

```

---

# Herramientas (Tools)

Las herramientas representan capacidades que el agente puede utilizar para interactuar con sistemas externos.

Ejemplos:

- Consultar catálogo.
- Consultar disponibilidad.
- Obtener información del negocio.
- Crear solicitudes.
- Guardar pedidos.

El agente nunca interactúa directamente con bases de datos o APIs.

Toda interacción se realiza mediante herramientas.

La documentación detallada se encuentra en:

```

docs/tools.md

```

---

# Principios de diseño

## Separación de responsabilidades

Cada nodo tiene una única responsabilidad claramente definida.

---

## Desacoplamiento

La lógica conversacional no depende del tipo de negocio.

El comportamiento del agente se adapta mediante la configuración de herramientas y fuentes de información.

---

## Escalabilidad

La arquitectura permite:

- agregar nuevos nodos;
- incorporar nuevas herramientas;
- integrar nuevos canales;
- soportar múltiples negocios.

Sin modificar el flujo principal del agente.

---

## Transferencia a humano

El agente no realiza pagos ni finaliza ventas.

Su responsabilidad es asistir durante la conversación y recopilar toda la información necesaria antes de transferir la interacción a un asesor humano.

---

# Evolución futura

La arquitectura permite incorporar funcionalidades adicionales como:

- Gestión completa de pedidos.
- Integración con inventarios.
- Agenda de entregas.
- Recomendación de productos.
- Memoria de largo plazo.
- Multiempresa.
- Panel administrativo.