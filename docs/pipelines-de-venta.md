# Pipelines de Venta

Este documento define el pipeline comercial para oportunidades de venta en nueva construcción, desde que existe intención real de compra hasta el cierre de la operación.

No es un pipeline de leads. Un contacto puede existir fuera de este pipeline mientras todavía se valida si realmente hay una oportunidad.

## Principio base

La oportunidad se crea solo cuando ya existe una intención real de compra.

Antes de ese momento, el contacto puede permanecer como `Nuevo Lead` fuera del pipeline mientras el chatbot, un agente o Sandra conversan con esa persona y validan si vale la pena abrir una oportunidad.

### Cuándo no crear la oportunidad todavía

* El contacto hizo una pregunta muy general.
* Solo pidió información básica y no mostró intención clara.
* No respondió después del primer intercambio.
* Todavía no hay contexto suficiente para saber si realmente quiere comprar.
* No hay siguiente paso comercial definido.

### Cuándo sí crear la oportunidad

* Expresa intención real de comprar.
* Acepta avanzar en una conversación comercial.
* Comparte contexto útil como presupuesto, zona, tiempo o tipo de compra.
* Pide llamada, cita, opciones o un siguiente paso concreto.
* Un chatbot o agente detecta interés real y lo valida.

## Cómo se debe leer este pipeline

Este pipeline separa dos cosas que no deben mezclarse:

* **Etapa:** indica en qué parte del proceso está la oportunidad mientras sigue abierta.
* **Estado:** indica si la oportunidad sigue abierta o ya terminó.

### Estado de la oportunidad

* `Open`: la oportunidad sigue activa dentro del pipeline.
* `Won`: la oportunidad se ganó y la compra se cerró.
* `Lost`: la oportunidad se perdió y ya no seguirá avanzando.
* `Abandon`: la oportunidad era real, pero quedó sin ejecución por falta de respuesta, enfriamiento o cambio de timing.

`Won`, `Lost` y `Abandon` no son etapas del pipeline. Son estados de salida de la oportunidad.

## Objetivo del pipeline

* Ordenar oportunidades reales de compra dentro de un flujo claro.
* Distinguir entre oportunidades activas y oportunidades reales que todavía no se ejecutan.
* Acompañar la selección de la propiedad específica.
* Reflejar claramente el momento en que la operación entra bajo contrato con el builder.
* Ordenar la parte financiera, contractual y de cierre dentro de un solo flujo.
* Facilitar seguimiento, reporting y automatizaciones sin inflar el pipeline con leads fríos.

## Etapas del pipeline

### Referencia Visual

![Pipeline de Ventas](assets/sales-pipeline.svg)

#### 1. Oportunidad Nueva

**Objetivo:** registrar y trabajar una oportunidad válida apenas se confirma que existe intención real.

* **Entrada a la etapa:** ya se decidió abrir la oportunidad porque el contacto mostró intención real de compra.
* **Acción principal:** registrar la oportunidad, documentar por qué existe y trabajarla mientras todavía está en fase comercial abierta.
* **Debe quedar claro al menos:** tipo de compra, rango de tiempo, presupuesto aproximado y motivo de interés.
* **Incluye normalmente:** conversaciones activas, validación de perfil, seguimiento comercial y preparación para revisar opciones concretas.
* **Mover a la siguiente etapa cuando:** la oportunidad debe quedar en `En espera` por timing futuro o ya está lista para pasar a selección de opciones.

#### 2. En espera

**Objetivo:** mantener abierta una oportunidad real cuyo momento de ejecución todavía no llegó.

* **Entrada a la etapa:** el cliente sí quiere comprar, pero no va a ejecutar ahora mismo.
* **Casos típicos:** compra en 3 a 6 meses, espera vender otra propiedad, espera fondos, viaje futuro, decisión familiar pendiente o visita próxima.
* **Acción principal:** dejar documentado por qué la oportunidad existe, por qué está pausada y cuándo se debe reactivar.
* **Campos mínimos recomendados:** motivo de espera, fecha estimada de reactivación, próxima tarea y notas de contexto.
* **Mover a la siguiente etapa cuando:** el cliente vuelve a activar la compra y la oportunidad regresa al trabajo comercial normal en `Oportunidad Nueva`.

#### 3. Seleccionando

**Objetivo:** acompañar la búsqueda de la propiedad específica hasta dejar una opción definida.

* **Entrada a la etapa:** la oportunidad ya está abierta, el cliente puede avanzar ahora y ya se están revisando opciones concretas contigo.
* **Acción principal:** revisar comunidades, modelos, inventarios o propiedades hasta definir la opción elegida.
* **Resultado esperado:** existe una propiedad seleccionada y el cliente está listo para entregar lo necesario para entrar bajo contrato.
* **Mover a la siguiente etapa cuando:** ya se inicia con el builder la entrega de documentos, depósito y datos necesarios para preparar el contrato.

#### 4. Bajo Contrato

**Objetivo:** formalizar la entrada de la operación con el builder para preparar el contrato de compraventa.

* **Entrada a la etapa:** ya existe una propiedad definida y se está ejecutando el paso formal para poner al cliente bajo contrato.
* **Acción principal:** coordinar la entrega de documentos, depósito, datos del comprador y cualquier requisito inicial que el builder necesita para preparar la firma del contrato de compraventa.
* **Resultado esperado:** el builder recibió lo necesario y la operación quedó encaminada como compra formal en proceso.
* **Mover a la siguiente etapa cuando:** la operación ya quedó bajo contrato y entra en la fase de requisitos financieros, documentales y de seguimiento post-contrato.

#### 5. Financiando

**Objetivo:** dejar al cliente listo para formalizar la compra.

* **Incluye:** pre-approval, lender, proof of funds, fondos adicionales, documentos personales, LLC si aplica y datos correctos del comprador.
* **Acción principal:** resolver requisitos financieros y documentales una vez que la operación ya está bajo contrato.
* **Notas:** esta etapa cubre tanto clientes financiados como cash, pero conviene identificar la ruta financiera de cada oportunidad.
* **Mover a la siguiente etapa cuando:** ya quedaron resueltos los requisitos principales y la operación entra en coordinación final para el cierre.

#### 6. Cerrando

**Objetivo:** llevar la operación hasta su cierre final en title company o notaría.

* **Entrada a la etapa:** la operación ya está bajo contrato, pasó por el seguimiento financiero y entra en su tramo final de cierre.
* **Incluye:** coordinación final, fondos de cierre, title, walkthrough, firma final y cierre oficial.
* **Acción principal:** asegurar que la transacción termine correctamente y sin pendientes mayores.
* **Resultado esperado:** la compra queda cerrada y lista para seguimiento post-venta.
* **Salida natural:** cambiar el estado de la oportunidad a `Won` cuando el cierre se complete.

## Reglas de movimiento

* Si un contacto no muestra intención real, no debe entrar a este pipeline.
* Si existe intención real, pero el momento de compra es futuro, la oportunidad puede entrar y quedar en `En espera`.
* `En espera` no significa duda general ni falta de trabajo; significa oportunidad real con ejecución futura.
* Toda oportunidad en `En espera` debe tener motivo de espera y fecha estimada de reactivación.
* Si una oportunidad sale de `En espera`, debe volver a `Oportunidad Nueva`.
* Si falta información crítica, la oportunidad debe quedarse en la etapa actual.
* Si el cliente ya puede avanzar ahora, no debe quedarse en `En espera`.
* Si el cliente cambia de propiedad, puede volver a trabajar opciones dentro de `Seleccionando` sin perder la lógica del proceso.
* `Bajo Contrato` representa el momento en que el builder recibe documentos, depósito y datos para preparar la firma del contrato de compraventa.
* `Financiando` debe cubrir tanto clientes financiados como cash.
* Después de `Financiando`, la oportunidad pasa directamente a `Cerrando`.
* Si el contrato se cae, conviene evaluar si vuelve a `Seleccionando`, si regresa a `En espera` o si termina en `Lost`, según el caso.

## Criterios para cambiar el estado de la oportunidad

### Cambiar a `Won`

* La compra cerró oficialmente.
* Ya no quedan acciones comerciales activas dentro del pipeline.

### Cambiar a `Lost`

* El cliente decidió no seguir.
* No calificó para continuar.
* Perdió la oportunidad frente a otra opción.
* La operación se cayó y no existe intención real de reactivarla.

Siempre conviene guardar un motivo claro de pérdida.

### Cambiar a `Abandon`

* La oportunidad era real, pero dejó de ejecutarse.
* El cliente dejó de responder por tiempo prolongado.
* El cliente sigue interesado, pero no hay fecha ni acción concreta para continuar.
* El proceso se enfrió sin un cierre formal.

`Abandon` es útil para diferenciar oportunidades reales que se congelaron de oportunidades realmente perdidas.

## Campos recomendados por oportunidad

* Presupuesto aproximado
* Zona o comunidad de interés
* Timeline estimado de compra
* Tipo de compra
* Cash o financing
* País o perfil del comprador
* Motivo de espera, si aplica
* Fecha de reactivación, si aplica
* Motivo de pérdida o abandono, si aplica

## Relación con el proceso post-contrato

Las etapas `Bajo Contrato`, `Financiando` y `Cerrando` conectan con el proceso operativo documentado en `docs/ventas.md`.

Ese documento profundiza en lo que ocurre después del contrato, incluyendo lender, appraisal, LLC, validación de correos, fondos y coordinación final hasta el cierre.
