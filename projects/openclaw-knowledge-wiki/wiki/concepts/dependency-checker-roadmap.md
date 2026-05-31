# DEPENDENCY_CHECKER roadmap

## Estado

Roadmap creado.

## Propósito

`DEPENDENCY_CHECKER` debe convertirse en el componente de análisis de impacto de Neodaemon.

Su función principal es responder:

Si modifico X, ¿qué podría romper?

No debe limitarse a buscar texto en el repositorio.

Debe ayudar a `TASK_VALIDATOR` a decidir si una acción puede avanzar, debe revisarse o debe bloquearse.

## Principio central

`DEPENDENCY_CHECKER` debe analizar impacto, no producir dumps masivos de grep.

Debe ser barato por defecto y profundo solo cuando el riesgo lo exige.

## Relación con TASK_VALIDATOR

`DEPENDENCY_CHECK


## Relación con repo hygiene

`DEPENDENCY_CHECKER` también debe apoyar la profesionalización del repositorio.

Antes de mover, borrar o reorganizar archivos, debe ayudar a identificar:

- rutas absolutas;
- servicios afectados;
- imports;
- scripts operativos;
- bots;
- referencias documentales;
- referencias históricas;
- archivos raíz sensibles.

## Fuera de alcance

`DEPENDENCY_CHECKER` no debe:

- ejecutar acciones;
- modificar archivos;
- decidir `safe_to_execute`;
- hacer commit;
- hacer push;
- crear PR;
- hacer merge;
- rotar secretos;
- tocar `.env`;
- tocar systemd;
- sustituir a `TASK_VALIDATOR`.

## Modos de funcionamiento

### TARGET

Modo por defecto.

Analiza un archivo, ruta o componente concreto.

Pregunta principal:

Si toco este target, ¿qué podría romper?

Debe usarse en validaciones normales.

### MAP

Modo excepcional.

Crea o actualiza inventarios amplios del repositorio.

Debe usarse solo cuando se necesite:

- mapa de rutas absolutas;
- mapa de servicios;
- mapa de scripts activos;
- mapa de archivos raíz sensibles;
- mapa de imports críticos.

No debe ejecutarse en cada validación.

## Niveles de análisis

`DEPENDENCY_CHECKER` debe comenzar siempre en el nivel más bajo posible.

Solo debe escalar si encuentra señales de riesgo o incertidumbre.

### D0 — Reference sniff

Objetivo:

Detectar rápidamente si existen referencias relevantes al target.

Pregunta principal:

¿Hay señales de que este archivo o componente es utilizado por otros elementos?

Fuentes típicas:

- systemd;
- scripts;
- bots;
- documentación relevante;
- configuraciones conocidas.

Características:

- muy bajo consumo de contexto;
- análisis rápido;
- sin razonamiento profundo.

Resultado esperado:

- número aproximado de referencias;
- indicio inicial de riesgo.

### D1 — Local impact

Objetivo:

Analizar dependencias cercanas al target.

Pregunta principal:

¿Qué depende localmente de este archivo?

Fuentes típicas:

- imports;
- tests;
- scripts relacionados;
- documentación asociada.

Características:

- bajo consumo de contexto;
- limitado al entorno inmediato del target.

Resultado esperado:

- dependencias locales;
- impacto probable;
- nivel de confianza.

### D2 — Operational impact

Objetivo:

Determinar impacto operativo.

Pregunta principal:

¿Modificar este target puede afectar componentes en ejecución?

Fuentes típicas:

- systemd;
- bots;
- wrappers;
- scripts operativos;
- rutas absolutas;
- servicios activos.

Características:

- análisis operativo;
- consumo medio de contexto;
- foco en ejecución real.

Resultado esperado:

- dependencias operativas;
- riesgo operativo;
- componentes afectados.

### D3 — Critical impact

Objetivo:

Analizar componentes críticos o sensibles.

Pregunta principal:

¿Existe riesgo de seguridad, pérdida irreversible o interrupción grave?

Fuentes típicas:

- `.env`;
- OAuth;
- gateway;
- auth;
- secretos;
- systemd crítico;
- borrados;
- archivos raíz sensibles.

Características:

- análisis profundo;
- consumo elevado de contexto;
- bloqueante por defecto.

Resultado esperado:

- impacto crítico;
- incertidumbres;
- recomendación conservadora.

## Estrategia de consumo de tokens

`DEPENDENCY_CHECKER` debe minimizar el uso de contexto.

Principios:

- empezar siempre en D0;
- escalar solo si hay evidencia suficiente;
- no analizar el repositorio completo por defecto;
- usar herramientas de búsqueda antes que razonamiento extenso;
- resumir antes de razonar.

Flujo recomendado:

```text
búsqueda local
        ↓
resumen compacto
        ↓
análisis de impacto
```

Flujo no recomendado:

```text
leer repositorio completo
        ↓
razonar sobre todo
```

## Presupuesto orientativo

### D0

Uso esperado:

- mínimo.

Objetivo:

- clasificación rápida.

### D1

Uso esperado:

- bajo.

Objetivo:

- impacto local.

### D2

Uso esperado:

- medio.

Objetivo:

- impacto operativo.

### D3

Uso esperado:

- alto.

Objetivo:

- impacto crítico.

Solo debe activarse cuando exista justificación clara.

## Formato obligatorio de salida

Toda ejecución de `DEPENDENCY_CHECKER` debe devolver una salida compacta.

Formato recomendado:

```text
DEPENDENCY_CHECKER:
- mode: TARGET/MAP
- target: <target>
- level: D0/D1/D2/D3
- direct_refs: <n>
- runtime_refs: YES/NO
- doc_refs: YES/NO
- historical_refs: YES/NO/UNKNOWN
- unknowns: YES/NO
- confidence: LOW/MEDIUM/HIGH
- impact_summary: <resumen>
- recommended_validator_level: L0/L1/L2/L3
- result: PASS/REVIEW/BLOCK
```

## Clasificación de referencias

`DEPENDENCY_CHECKER` debe distinguir entre tipos de referencia.

### Runtime

Dependencias utilizadas en ejecución.

Ejemplos:

- systemd;
- bots;
- scripts activos;
- wrappers;
- servicios;
- imports utilizados.

### Documentation

Referencias documentales.

Ejemplos:

- wiki;
- roadmap;
- notas técnicas;
- documentación histórica.

### Historical

Referencias heredadas o de contexto.

Ejemplos:

- backups;
- snapshots;
- documentación archivada;
- ejemplos antiguos.

Estas referencias no deben considerarse automáticamente dependencias activas.

## Gestión de incertidumbre

Cuando no pueda determinar la naturaleza de una referencia debe marcar:

```text
unknowns: YES
```

La incertidumbre debe ser explícita.

No debe asumir dependencias inexistentes.

No debe asumir ausencia de dependencias.

## Límite de referencias

`DEPENDENCY_CHECKER` no debe devolver listados masivos.

Regla general:

- mostrar máximo 10 referencias relevantes;
- resumir el resto.

Ejemplo:

```text
direct_refs:
- openclaw-api.service
- rag_query_local.sh
- LOCAL_ENVIRONMENT.md

additional_refs: 17
```

## Criterios de revisión

Debe devolver:

```text
result: REVIEW
```

cuando:

- existan dependencias operativas;
- existan referencias desconocidas;
- exista incertidumbre relevante;
- el impacto potencial no pueda determinarse con confianza.

## Criterios de bloqueo

Debe recomendar:

```text
result: BLOCK
```

cuando:

- se detecten dependencias críticas;
- existan referencias sensibles no clasificadas;
- el target afecte componentes de seguridad;
- exista riesgo elevado de interrupción operativa;
- el análisis requiera revisión humana obligatoria.

La decisión final sigue correspondiendo a `TASK_VALIDATOR`.

## Roadmap de implementación

### v0.1 — Roadmap documental

- definir propósito;
- definir niveles D0-D3;
- definir formato de salida;
- definir estrategia de tokens.

### v0.2 — Procedimiento manual

- aplicar análisis de impacto manual;
- documentar resultados;
- registrar casos reales.

### v0.3 — Checker asistido

- detección automática de referencias;
- clasificación inicial;
- generación de resumen compacto.

### v1.0 — Integración operativa

- integración con `TASK_VALIDATOR`;
- integración con GitHub runner;
- soporte para análisis de impacto antes de acciones sensibles.

## Riesgos

### Riesgo 1 — Convertirse en un grep glorificado

Mitigación:

- priorizar impacto sobre coincidencias de texto.

### Riesgo 2 — Consumo excesivo de contexto

Mitigación:

- comenzar siempre en D0;
- escalar solo cuando sea necesario.

### Riesgo 3 — Falsos positivos

Mitigación:

- distinguir runtime, documentation e historical.

### Riesgo 4 — Falsa sensación de seguridad

Mitigación:

- declarar incertidumbre;
- usar `unknowns`;
- recomendar revisión cuando corresponda.

## Decisión estratégica

`DEPENDENCY_CHECKER` debe ser un analizador de impacto con presupuesto de contexto.

No debe convertirse en un buscador global del repositorio.

## Próximo paso recomendado

Tras consolidar este roadmap, el siguiente paso es definir la especificación operativa de `DEPENDENCY_CHECKER` v0.1 y su integración futura con `TASK_VALIDATOR`.


