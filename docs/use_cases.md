# Casos de Uso

## Descripción

Este documento describe los principales casos de uso soportados por el agente conversacional.

Cada caso de uso representa una interacción entre un usuario y el sistema para alcanzar un objetivo específico.

---

# UC-01 - Consultar información del negocio

## Objetivo

Permitir que el cliente consulte información general del negocio.

## Actor principal

Cliente

## Precondiciones

- El agente está disponible.
- El negocio posee información configurada.

## Flujo principal

1. El cliente envía una consulta.
2. El agente identifica la intención.
3. El agente consulta la información del negocio.
4. El agente responde al cliente.

## Ejemplos

- ¿Dónde están ubicados?
- ¿Cuál es el horario?
- ¿Qué redes sociales tienen?
- ¿Hacen domicilios?

## Resultado esperado

El cliente obtiene la información solicitada.

---

# UC-02 - Consultar productos o servicios

## Objetivo

Permitir que el cliente consulte el catálogo del negocio.

## Actor principal

Cliente

## Precondiciones

- El catálogo está disponible.

## Flujo principal

1. El cliente realiza una consulta.
2. El agente identifica la intención.
3. El agente consulta el catálogo.
4. El agente responde utilizando la información encontrada.

## Ejemplos

- ¿Qué productos tienen?
- ¿Cuánto cuesta un pastel?
- ¿Qué sabores manejan?
- ¿Tienen disponibilidad para mañana?

## Resultado esperado

El cliente recibe información actualizada del catálogo.

---

# UC-03 - Iniciar una compra

## Objetivo

Comenzar el proceso de compra de un producto o servicio.

## Actor principal

Cliente

## Precondiciones

- Existe un producto o servicio disponible.

## Flujo principal

1. El cliente manifiesta intención de compra.
2. El agente inicia la recopilación de información.
3. El agente solicita los datos necesarios.
4. El agente construye el pedido.

## Resultado esperado

Se obtiene un pedido parcialmente o completamente construido.

---

# UC-04 - Modificar información del pedido

## Objetivo

Permitir al cliente cambiar información antes de finalizar el pedido.

## Actor principal

Cliente

## Precondiciones

- Existe un pedido en construcción.

## Flujo principal

1. El agente muestra el resumen del pedido.
2. El cliente solicita un cambio.
3. El agente actualiza la información.
4. El agente genera un nuevo resumen.

## Resultado esperado

El pedido queda actualizado.

---

# UC-05 - Confirmar pedido

## Objetivo

Confirmar la información recopilada antes de transferir la conversación.

## Actor principal

Cliente

## Precondiciones

- El pedido está completo.

## Flujo principal

1. El agente presenta un resumen.
2. El cliente confirma la información.
3. El agente marca el pedido como listo.

## Resultado esperado

El pedido queda preparado para atención humana.

---

# UC-06 - Transferir conversación a un asesor

## Objetivo

Entregar la conversación a un asesor humano para finalizar la venta.

## Actor principal

Agente

## Actor secundario

Asesor humano

## Precondiciones

- El pedido fue confirmado.

## Flujo principal

1. El agente recopila el contexto de la conversación.
2. El agente prepara el resumen del pedido.
3. El agente transfiere la conversación.
4. El cliente es informado de la transferencia.

## Resultado esperado

El asesor recibe toda la información necesaria para continuar el proceso.

---

# UC-07 - Mantener el contexto conversacional

## Objetivo

Permitir conversaciones naturales sin que el cliente repita información.

## Actor principal

Cliente

## Flujo principal

1. El cliente realiza varias consultas.
2. El agente conserva el contexto.
3. El agente utiliza información previamente recopilada.
4. La conversación continúa de forma natural.

## Ejemplo

Cliente:

> Quiero un pastel de chocolate.

Agente:

> ¿Para cuántas personas?

Cliente:

> Veinte.

Agente:

> Perfecto. ¿Para qué fecha lo necesitas?

## Resultado esperado

La conversación mantiene coherencia durante toda la interacción.

---

# UC-08 - Adaptarse a diferentes negocios

## Objetivo

Permitir que el mismo agente pueda trabajar para distintos tipos de negocio.

## Actor principal

Administrador del sistema

## Precondiciones

- El negocio posee una configuración válida.

## Flujo principal

1. El agente identifica el negocio asociado.
2. El agente utiliza las herramientas configuradas.
3. El agente responde utilizando la información correspondiente.

## Resultado esperado

El mismo flujo conversacional funciona para múltiples empresas.

---

# Casos de uso futuros

Los siguientes casos de uso no forman parte del MVP, pero podrán incorporarse en futuras versiones.

- Procesamiento de pagos.
- Facturación electrónica.
- Gestión de inventario.
- Programación de entregas.
- Recomendación inteligente de productos.
- Seguimiento de pedidos.
- Integración con CRM.
- Panel administrativo.