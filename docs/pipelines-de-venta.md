# Pipeline de Oportunidades de Venta

Este documento define el pipeline comercial para oportunidades de venta en nueva construcción, desde que existe intención real de compra hasta el cierre de la operación.

No es un pipeline de leads. Un contacto puede existir fuera de este pipeline mientras todavía se valida si realmente hay una oportunidad.

## Principio base

La oportunidad se crea solo cuando ya existe una intención real de compra.

Antes de ese momento, el contacto puede permanecer como `Nuevo Lead` fuera del pipeline mientras el chatbot, un agente o Sandra conversan con esa persona y validan si vale la pena abrir una oportunidad.

### Cuándo no crear la oportunidad todavía

- El contacto hizo una pregunta muy general.
- Solo pidió información básica y no mostró intención clara.
- No respondió después del primer intercambio.
- Todavía no hay contexto suficiente para saber si realmente quiere comprar.
- No hay siguiente paso comercial definido.

### Cuándo sí crear la oportunidad

- Expresa intención real de comprar.
- Acepta avanzar en una conversación comercial.
- Comparte contexto útil como presupuesto, zona, tiempo o tipo de compra.
- Pide llamada, cita, opciones o un siguiente paso concreto.
- Un chatbot o agente detecta interés real y lo valida.

## Cómo se debe leer este pipeline

Este pipeline separa dos cosas que no deben mezclarse:

- **Etapa:** indica en qué parte del proceso está la oportunidad mientras sigue abierta.
- **Estado:** indica si la oportunidad sigue abierta o ya terminó.

### Estado de la oportunidad

- `Open`: la oportunidad sigue activa dentro del pipeline.
- `Won`: la oportunidad se ganó y la compra se cerró.
- `Lost`: la oportunidad se perdió y ya no seguirá avanzando.
- `Abandon`: la oportunidad era real, pero quedó sin ejecución por falta de respuesta, enfriamiento o cambio de timing.

`Won`, `Lost` y `Abandon` no son etapas del pipeline. Son estados de salida de la oportunidad.

## Objetivo del pipeline

- Ordenar oportunidades reales de compra dentro de un flujo claro.
- Distinguir entre oportunidades activas y oportunidades reales que todavía no se ejecutan.
- Acompañar la selección de la propiedad específica.
- Ordenar la parte financiera, contractual y de cierre dentro de un solo flujo.
- Facilitar seguimiento, reporting y automatizaciones sin inflar el pipeline con leads fríos.

## Etapas del pipeline

#### 1. Oportunidad Nueva

**Objetivo:** registrar una oportunidad válida apenas se confirma que existe intención real.

- **Entrada a la etapa:** ya se decidió abrir la oportunidad porque el contacto mostró intención real de compra.
- **Acción principal:** registrar la oportunidad, documentar por qué existe y capturar el contexto comercial inicial.
- **Debe quedar claro al menos:** tipo de compra, rango de tiempo, presupuesto aproximado y motivo de interés.
- **Mover a la siguiente etapa cuando:** ya se confirmó si la oportunidad debe activarse ahora o si realmente debe quedar en espera.

#### 2. En espera

**Objetivo:** mantener abierta una oportunidad real cuyo momento de ejecución todavía no llegó.

- **Entrada a la etapa:** el cliente sí quiere comprar, pero no va a ejecutar ahora mismo.
- **Casos típicos:** compra en 3 a 6 meses, espera vender otra propiedad, espera fondos, viaje futuro, decisión familiar pendiente o visita próxima.
- **Acción principal:** dejar documentado por qué la oportunidad existe, por qué está pausada y cuándo se debe reactivar.
- **Campos mínimos recomendados:** motivo de espera, fecha estimada de reactivación, próxima tarea y notas de contexto.
- **Mover a la siguiente etapa cuando:** el cliente vuelve a activar la búsqueda y ya está listo para trabajar opciones reales.

#### 3. Activa

**Objetivo:** trabajar comercialmente una oportunidad que ya puede avanzar en el presente.

- **Entrada a la etapa:** la oportunidad ya está abierta y el cliente puede avanzar ahora.
- **Acción principal:** conversar, confirmar perfil de compra, resolver dudas y validar que existe una base suficiente para pasar a selección.
- **Validaciones clave:** presupuesto, tipo de compra, forma de pago, país, plazo estimado y objetivo de compra.
- **Mover a la siguiente etapa cuando:** ya están revisando opciones concretas de compra.

#### 4. Seleccionando

**Objetivo:** acompañar la búsqueda de la propiedad específica hasta dejar una opción definida.

- **Entrada a la etapa:** el cliente ya está viendo opciones concretas contigo.
- **Acción principal:** revisar comunidades, modelos, inventarios o propiedades hasta definir la opción elegida.
- **Resultado esperado:** existe una propiedad seleccionada y la operación está encaminada para reserva, depósito o inicio formal de documentación.
- **Mover a la siguiente etapa cuando:** ya toca completar banco, fondos, documentos y requisitos previos a la firma.

#### 5. Financiando

**Objetivo:** dejar al cliente listo para formalizar la compra.

- **Incluye:** pre-approval, lender, proof of funds, fondos adicionales, documentos personales, LLC si aplica y datos correctos del comprador.
- **Acción principal:** resolver requisitos financieros y documentales sin sacar la oportunidad del flujo principal.
- **Notas:** esta etapa cubre tanto clientes financiados como cash, pero conviene identificar la ruta financiera de cada oportunidad.
- **Mover a la siguiente etapa cuando:** el cliente ya está listo para firmar o entrar en compromiso formal.

#### 6. Firmando

**Objetivo:** formalizar el compromiso contractual de la compra.

- **Entrada a la etapa:** ya existe decisión firme de compra y se está coordinando firma, depósito o contrato.
- **Acción principal:** coordinar firma, depósito, documentos contractuales y arranque formal de la operación.
- **Resultado esperado:** contrato firmado y operación formalmente en marcha.
- **Mover a la siguiente etapa cuando:** la operación entra en tramo final hacia el cierre.

#### 7. Cerrando

**Objetivo:** llevar la operación hasta su finalización.

- **Incluye:** coordinación final, fondos de cierre, title, walkthrough, firma final y cierre oficial.
- **Acción principal:** asegurar que la transacción termine correctamente y sin pendientes mayores.
- **Resultado esperado:** la compra queda cerrada y lista para seguimiento post-venta.
- **Salida natural:** cambiar el estado de la oportunidad a `Won` cuando el cierre se complete.

## Reglas de movimiento

- Si un contacto no muestra intención real, no debe entrar a este pipeline.
- Si existe intención real, pero el momento de compra es futuro, la oportunidad puede entrar y quedar en `En espera`.
- `En espera` no significa duda general ni falta de trabajo; significa oportunidad real con ejecución futura.
- Toda oportunidad en `En espera` debe tener motivo de espera y fecha estimada de reactivación.
- Si falta información crítica, la oportunidad debe quedarse en la etapa actual.
- Si el cliente ya puede avanzar ahora, no debe quedarse en `En espera`.
- Si el cliente cambia de propiedad, puede volver a trabajar opciones dentro de `Seleccionando` sin perder la lógica del proceso.
- `Financiando` debe cubrir tanto clientes financiados como cash.
- Si el contrato se cae, conviene evaluar si vuelve a `Seleccionando`, si regresa a `En espera` o si termina en `Lost`, según el caso.

## Criterios para cambiar el estado de la oportunidad

### Cambiar a `Won`

- La compra cerró oficialmente.
- Ya no quedan acciones comerciales activas dentro del pipeline.

### Cambiar a `Lost`

- El cliente decidió no seguir.
- No calificó para continuar.
- Perdió la oportunidad frente a otra opción.
- La operación se cayó y no existe intención real de reactivarla.

Siempre conviene guardar un motivo claro de pérdida.

### Cambiar a `Abandon`

- La oportunidad era real, pero dejó de ejecutarse.
- El cliente dejó de responder por tiempo prolongado.
- El cliente sigue interesado, pero no hay fecha ni acción concreta para continuar.
- El proceso se enfrió sin un cierre formal.

`Abandon` es útil para diferenciar oportunidades reales que se congelaron de oportunidades realmente perdidas.

## Campos recomendados por oportunidad

- Presupuesto aproximado
- Zona o comunidad de interés
- Timeline estimado de compra
- Tipo de compra
- Cash o financing
- País o perfil del comprador
- Motivo de espera, si aplica
- Fecha de reactivación, si aplica
- Motivo de pérdida o abandono, si aplica

## Relación con el proceso post-contrato

Las etapas `Firmando` y `Cerrando` conectan con el proceso operativo documentado en `docs/ventas.md`.

Ese documento profundiza en lo que ocurre después del contrato, incluyendo lender, appraisal, LLC, validación de correos, fondos y coordinación final hasta el cierre.

