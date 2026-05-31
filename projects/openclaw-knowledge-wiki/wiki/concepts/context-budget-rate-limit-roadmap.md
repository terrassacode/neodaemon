# Context Budget & Rate Limit Roadmap

## Estado

Roadmap creado.

## Propósito

Definir una estrategia formal para controlar el consumo de contexto, tokens, peticiones y recursos de razonamiento en Neodaemon.

El objetivo es reducir el riesgo de bloqueos por rate limit, mejorar la eficiencia operativa y evitar que el crecimiento de la documentación provoque degradación progresiva del sistema.

## Problema que resuelve

A medida que Neodaemon incorpora nuevas capacidades aparecen varios riesgos:

- aumento continuo del contexto cargado;
- reutilización de documentación extensa;
- razonamientos innecesariamente profundos;
- llamadas repetidas al modelo;
- reintentos automáticos costosos;
- duplicación de información;
- crecimiento de la wiki operativa.

Estos factores pueden provocar:

- mayor consumo de tokens;
- aumento de latencia;
- reducción de capacidad operativa;
- aparición de rate limits;
- degradación del razonamiento;
- incremento del coste operativo.

## Principio central

Neodaemon debe consumir la mínima cantidad de contexto necesaria para tomar una decisión fiable.

La prioridad no es maximizar razonamiento.

La prioridad es maximizar eficiencia operativa.

## Hipótesis de trabajo

Hasta disponer de métricas reales, se considerará posible que los bloqueos observados estén relacionados con una combinación de:

- tamaño de contexto;
- frecuencia de peticiones;
- reintentos;
- acumulación de memoria contextual;
- uso ineficiente del razonamiento.

Estas hipótesis deben verificarse mediante observabilidad.

No deben asumirse como hechos demostrados.

## Principios estratégicos

### Medir antes de optimizar

No deben realizarse optimizaciones basadas únicamente en intuiciones.

Toda decisión debe apoyarse en evidencia observable.

### Context engineering antes que reasoning

Siempre que sea posible debe reducirse contexto antes de aumentar razonamiento.

### Presupuesto antes de ejecución

Antes de cargar contexto debe evaluarse cuánto contexto es realmente necesario.

### Escalado progresivo

Toda validación debe comenzar con el nivel mínimo de contexto posible.

Solo debe escalar si existe evidencia que lo justifique.

### Compresión antes que expansión

Si existe información equivalente en formato resumido, debe priorizarse el resumen.

### Observabilidad antes que automatización

No deben automatizarse decisiones cuyo consumo operativo no pueda medirse.

## Objetivos

### Objetivo 1

Reducir consumo innecesario de tokens.

### Objetivo 2

Reducir frecuencia de bloqueos por rate limit.

### Objetivo 3

Evitar razonamiento profundo para tareas simples.

### Objetivo 4

Definir presupuestos operativos verificables.

### Objetivo 5

Mantener escalabilidad a medida que crezca la wiki de Neodaemon.

## Fuera de alcance

Este roadmap no implementa:

- cambios en modelos;
- cambios de proveedor;
- cambios de gateway;
- cambios de autenticación;
- cambios de OAuth;
- cambios de infraestructura;
- cambios de systemd.

Su alcance es exclusivamente documental y estratégico.

## Métricas de observabilidad

Antes de optimizar consumo, Neodaemon debe ser capaz de medirlo.

La observabilidad debe distinguir entre diferentes categorías de consumo.

### Tokens

Métricas:

- tokens de entrada;
- tokens de salida;
- tokens totales;
- tokens por tarea;
- tokens por componente.

### Peticiones

Métricas:

- peticiones por hora;
- peticiones por sesión;
- peticiones por workflow;
- peticiones fallidas;
- peticiones reintentadas.

### Contexto

Métricas:

- tamaño de contexto cargado;
- documentos utilizados;
- fragmentos utilizados;
- contexto descartado;
- contexto reutilizado.

### Herramientas

Métricas:

- tool calls por tarea;
- tool calls por workflow;
- herramientas más utilizadas;
- herramientas con mayor coste operativo.

### Recuperación

Métricas:

- retries;
- fallos recuperados;
- llamadas repetidas;
- llamadas redundantes.

## Categorías de consumo

No todo el consumo tiene el mismo valor.

Neodaemon debe diferenciar:

### Consumo útil

Contexto utilizado directamente para tomar decisiones.

Ejemplos:

- reglas relevantes;
- dependencias relevantes;
- documentación necesaria.

### Consumo redundante

Información cargada pero no utilizada.

Ejemplos:

- documentos completos innecesarios;
- logs irrelevantes;
- contexto histórico no consultado.

### Consumo recuperativo

Consumo generado por errores.

Ejemplos:

- retries;
- llamadas duplicadas;
- revalidaciones innecesarias.

### Consumo estructural

Consumo necesario para operar.

Ejemplos:

- system prompts;
- políticas;
- contexto mínimo obligatorio.

## Presupuesto de contexto

Toda tarea debe tener un presupuesto orientativo.

### Nivel bajo

Ejemplos:

- documentación;
- wiki;
- notas;
- validaciones simples.

Regla:

- usar resúmenes;
- evitar documentos completos.

### Nivel medio

Ejemplos:

- revisión técnica;
- análisis local;
- cambios documentales complejos.

Regla:

- cargar únicamente dependencias relevantes.

### Nivel alto

Ejemplos:

- cambios operativos;
- servicios;
- automatización.

Regla:

- justificar escalado.

### Nivel crítico

Ejemplos:

- seguridad;
- OAuth;
- gateway;
- systemd;
- secretos.

Regla:

- consumo alto permitido únicamente con justificación explícita.

## Presupuesto de peticiones

Neodaemon debe minimizar llamadas innecesarias.

Principios:

- una llamada buena es mejor que varias llamadas redundantes;
- evitar reconsultas idénticas;
- reutilizar resultados recientes cuando sea seguro hacerlo.

## Presupuesto de retries

Los retries deben considerarse consumo de riesgo.

Reglas:

- registrar cada retry;
- registrar causa;
- registrar resultado.

Objetivo:

- identificar bucles de recuperación costosos.

## Model Invocation Budget

No todas las tareas requieren razonamiento del modelo.

### Shell First

Prioridad:

```text
grep
find
wc
git
systemctl
```

Antes de invocar razonamiento.

### Summary First

Prioridad:

```text
resumen
↓
razonamiento
```

No:

```text
documento completo
↓
razonamiento
```

### Reasoning On Demand

El razonamiento profundo debe activarse únicamente cuando:

- exista incertidumbre;
- exista riesgo;
- exista necesidad de decisión.

## Regla de escalado

Flujo recomendado:

```text
datos mínimos
        ↓
resumen
        ↓
validación
        ↓
escalado opcional
```

Flujo no recomendado:

```text
cargar todo
        ↓
razonar sobre todo
```

## Context Compaction

A medida que la documentación crezca, Neodaemon debe evitar cargar documentos completos por defecto.

La estrategia recomendada es utilizar compresión progresiva de contexto.

### Canonical Summary

Todo componente estratégico debe disponer de:

- resumen canónico;
- documento completo;
- referencia de versión.

Ejemplo:

```text
TASK_VALIDATOR
    ├─ summary
    └─ full document
```

Por defecto debe cargarse únicamente el resumen.

### Full Context Escalation

El documento completo solo debe cargarse cuando:

- el resumen sea insuficiente;
- exista conflicto;
- exista incertidumbre significativa;
- exista impacto crítico.

### Context Deduplication

Neodaemon debe evitar cargar múltiples documentos que describan la misma información.

Regla:

```text
1 concepto
↓
1 resumen principal
```

No:

```text
1 concepto
↓
5 documentos similares
```

## Rate Limit Diagnosis

Los bloqueos deben clasificarse antes de actuar.

No todos los rate limits tienen la misma causa.

### Posibles causas

#### Context overload

Síntomas:

- contexto creciente;
- respuestas lentas;
- uso elevado de tokens.

#### Request overload

Síntomas:

- demasiadas peticiones por unidad de tiempo;
- respuestas cortas;
- contexto pequeño.

#### Retry loops

Síntomas:

- reintentos frecuentes;
- mismas operaciones repetidas.

#### Tool amplification

Síntomas:

- demasiadas herramientas por workflow;
- llamadas encadenadas.

### Clasificación obligatoria

Antes de proponer optimizaciones debe intentarse clasificar:

```text
CONTEXT
REQUEST
RETRY
TOOL
UNKNOWN
```

## Indicadores operativos

Neodaemon debe disponer de indicadores simples.

### Indicador de eficiencia

```text
useful_context
÷
loaded_context
```

Objetivo:

Maximizar contexto útil.

### Indicador de reutilización

```text
reused_context
÷
loaded_context
```

Objetivo:

Evitar recargas innecesarias.

### Indicador de retries

```text
retries
÷
requests
```

Objetivo:

Detectar bucles de recuperación.

### Indicador de expansión

```text
full_documents
÷
summaries
```

Objetivo:

Detectar exceso de carga documental.

## Relación con TASK_VALIDATOR

`TASK_VALIDATOR` debe respetar presupuestos de contexto.

Ejemplos:

### L0

- resumen únicamente;
- sin documentos completos.

### L1

- resumen;
- dependencias directas.

### L2

- contexto ampliado;
- dependencias relevantes.

### L3

- contexto completo permitido;
- justificación obligatoria.

## Relación con DEPENDENCY_CHECKER

`DEPENDENCY_CHECKER` debe aplicar:

### D0

- búsqueda mínima.

### D1

- impacto local.

### D2

- impacto operativo.

### D3

- impacto crítico.

Cada nivel debe consumir únicamente el contexto necesario.

## Roadmap de implementación

### v0.1 — Observabilidad documental

- definir métricas;
- definir presupuestos;
- definir clasificación de consumo.

### v0.2 — Registro manual

- recopilar casos reales;
- documentar patrones de consumo.

### v0.3 — Observabilidad asistida

- generar métricas automáticamente;
- detectar excesos de contexto.

### v1.0 — Budget Enforcement

- aplicar presupuestos operativos;
- bloquear escalados injustificados;
- recomendar compresión automática.

## Riesgos

### Riesgo 1 — Medir sin actuar

Mitigación:

- asociar métricas a decisiones operativas.

### Riesgo 2 — Optimizar la métrica equivocada

Mitigación:

- medir tokens, peticiones, retries y herramientas por separado.

### Riesgo 3 — Exceso de compresión

Mitigación:

- permitir escalado controlado al documento completo.

### Riesgo 4 — Complejidad excesiva

Mitigación:

- comenzar con métricas simples.

## Decisión estratégica

Neodaemon debe gestionar contexto como un recurso limitado.

El crecimiento de la wiki no debe traducirse automáticamente en crecimiento del contexto cargado.

## Próximo paso recomendado

Tras consolidar este roadmap, el siguiente paso es definir el flujo de decisión completo de Neodaemon y cómo interactúan:

```text
DESIGN_DOC_CHECK
        ↓
DEPENDENCY_CHECKER
        ↓
TASK_VALIDATOR
        ↓
RUNNER
```

respetando los presupuestos definidos en este documento.

## Casos de uso de referencia

### Caso 1 — Consulta documental simple

Solicitud:

```text
¿Existe una regla para DESIGN_DOC_CHECK?
```

Flujo esperado:

```text
summary
↓
respuesta
```

No debe cargar:

- roadmap completos;
- logs históricos;
- documentación no relacionada.

Nivel esperado:

```text
LOW
```

### Caso 2 — Cambio documental

Solicitud:

```text
Añadir una regla a TASK_VALIDATOR.
```

Flujo esperado:

```text
summary TASK_VALIDATOR
↓
validación
↓
respuesta
```

No debe cargar:

- wiki completa;
- roadmaps no relacionados.

Nivel esperado:

```text
MEDIUM
```

### Caso 3 — Cambio operativo

Solicitud:

```text
Modificar un servicio systemd.
```

Flujo esperado:

```text
DEPENDENCY_CHECKER
↓
TASK_VALIDATOR
↓
escalado
```

Nivel esperado:

```text
HIGH
```

### Caso 4 — Cambio crítico

Solicitud:

```text
Modificar OAuth o gateway.
```

Flujo esperado:

```text
DEPENDENCY_CHECKER D3
↓
TASK_VALIDATOR L3
↓
revisión obligatoria
```

Nivel esperado:

```text
CRITICAL
```

## Reglas de truncado

Cuando el contexto exceda el presupuesto previsto, Neodaemon debe aplicar truncado controlado.

Orden recomendado:

1. eliminar duplicados;
2. sustituir documentos por resúmenes;
3. limitar referencias históricas;
4. limitar logs antiguos;
5. escalar únicamente si sigue siendo necesario.

No debe:

```text
cargar todo
y decidir después
```

Debe:

```text
decidir primero
qué necesita cargar
```

## Reglas de caché conceptual

Neodaemon debe favorecer reutilización controlada.

Elementos candidatos:

- resúmenes canónicos;
- mapas de dependencias;
- inventarios de repositorio;
- reglas estables.

Objetivo:

Reducir consultas repetitivas.

## Señales de alerta

Se considera señal de alerta cuando se detecte:

- mismo documento cargado repetidamente;
- múltiples retries consecutivos;
- expansión frecuente a documentos completos;
- crecimiento continuo de contexto por tarea;
- workflows con demasiadas herramientas.

Estas señales deben investigarse antes de aumentar presupuestos.

## Tests futuros

### Test 1 — Minimal Context

Verificar que una tarea documental simple no carga documentación irrelevante.

Resultado esperado:

```text
PASS
```

### Test 2 — Summary First

Verificar que se utiliza resumen antes que documento completo.

Resultado esperado:

```text
PASS
```

### Test 3 — Escalado Justificado

Verificar que el contexto solo aumenta cuando existe evidencia.

Resultado esperado:

```text
PASS
```

### Test 4 — Retry Detection

Verificar que los retries quedan registrados.

Resultado esperado:

```text
PASS
```

### Test 5 — Rate Limit Classification

Verificar que los bloqueos se clasifican como:

```text
CONTEXT
REQUEST
RETRY
TOOL
UNKNOWN
```

Resultado esperado:

```text
PASS
```

## Criterios de éxito

El roadmap se considerará exitoso cuando:

- el contexto medio por tarea disminuya;
- aumente la reutilización de resúmenes;
- disminuyan los retries innecesarios;
- disminuyan las cargas documentales redundantes;
- exista capacidad para diagnosticar rate limits.

## Nota estratégica

La observabilidad no es el objetivo final.

El objetivo final es permitir que Neodaemon escale en capacidades sin que el consumo de contexto crezca al mismo ritmo.

La eficiencia operativa debe convertirse en una restricción arquitectónica permanente.


