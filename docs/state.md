# Agent State

## Descripción

El **Agent State** representa toda la información compartida entre los nodos durante la ejecución del agente.

Cada nodo puede:

- Leer información existente.
- Agregar nueva información.
- Actualizar información previamente almacenada.

El estado viaja durante toda la conversación y constituye la única fuente de verdad del agente.

---

# Estructura del State

## messages

### Descripción

Historial completo de la conversación entre el usuario y el agente.

Permite mantener el contexto y generar respuestas coherentes.

### Tipo

Lista de mensajes.

### Ejemplo

- Usuario: Hola.
- Agente: ¡Hola! ¿En qué puedo ayudarte?
- Usuario: ¿Qué productos tienen?

---

## business_id

### Descripción

Identificador del negocio al que pertenece la conversación.

Permite que un mismo agente pueda trabajar para múltiples empresas.

### Tipo

String

### Ejemplo

```
pasteleria-san-jose
```

---

## customer_information

### Descripción

Información recopilada del cliente durante la conversación.

No toda la información estará disponible desde el inicio.

Se irá completando progresivamente.

### Posibles campos

- Nombre
- Teléfono
- Dirección
- Correo electrónico

---

## detected_intent

### Descripción

Última intención detectada por el agente.

Es utilizada para decidir el siguiente nodo del flujo.

### Ejemplos

- business_information
- product_information
- create_order

---

## current_order

### Descripción

Representa el pedido que se está construyendo durante la conversación.

Su contenido evoluciona a medida que el agente recopila información.

### Posibles campos

- Producto
- Cantidad
- Tamaño
- Personalización
- Fecha
- Hora
- Dirección
- Observaciones

---

## products_found

### Descripción

Resultado de la última consulta realizada sobre el catálogo.

Permite reutilizar la información sin realizar nuevamente la consulta.

### Tipo

Lista de productos.

---

## conversation_status

### Descripción

Estado actual de la conversación.

Permite conocer en qué etapa se encuentra el proceso.

### Posibles valores

- collecting_information
- answering_questions
- creating_order
- waiting_confirmation
- transferred_to_human
- finished

---

## requires_human

### Descripción

Indica si la conversación requiere intervención humana.

### Tipo

Boolean

### Ejemplo

```
true
```

---

## response

### Descripción

Respuesta generada por el agente para ser enviada al usuario.

Este campo representa el resultado final producido por el flujo.

---

# Flujo del State

El estado es compartido por todos los nodos del agente.

```
Receive User Message

        │

        ▼

    AgentState

        │

        ▼

Handle Intent

        │

        ▼

Product Knowledge

        │

        ▼

Handle Transaction

        │

        ▼

Finalize Transaction

        │

        ▼

Human Assistance
```

Cada nodo puede leer y modificar únicamente la información necesaria para cumplir su responsabilidad.

---

# Principios de diseño

## Fuente única de verdad

Toda la información necesaria para la conversación debe encontrarse dentro del estado.

---

## Compartido

Todos los nodos trabajan sobre el mismo estado.

---

## Evolutivo

El estado se construye progresivamente durante la conversación.

No toda la información está disponible desde el inicio.

---

## Desacoplado

Los nodos no comparten información directamente entre sí.

La comunicación siempre ocurre mediante el Agent State.

---

# Implementación

La implementación concreta del estado será realizada mediante un `TypedDict`, siguiendo las recomendaciones de LangGraph.

La estructura podrá evolucionar conforme aumenten las funcionalidades del agente.