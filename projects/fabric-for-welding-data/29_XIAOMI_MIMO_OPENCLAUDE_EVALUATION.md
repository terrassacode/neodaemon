# 29_XIAOMI_MIMO_OPENCLAUDE_EVALUATION.md

Status: experimental_only evaluation  
Scope: Xiaomi MiMo vía OpenClaude/OpenGateway como modelo experimental LOW_SCOPE, no secondary  
Version: v1.1  
Última actualización: 2026-05-22

---

## 1. Objetivo

Evaluar si Xiaomi MiMo podría usarse como modelo experimental barato o gratuito para tareas no críticas dentro de OpenClaw.

El objetivo actual es observar comportamiento real antes de considerar cualquier integración en routing.

Esta evaluación no autoriza implementación.

No se debe tocar:

- gateway real;
- routing;
- modelos activos;
- configuración sensible;
- tokens;
- runtime;
- servicios.

---

## 2. Regla principal

Xiaomi MiMo, si se prueba en el futuro, debe tratarse como modelo experimental y limitado.

Estado operativo actual:

```text
experimental_only
```

Reglas obligatorias:

```text
No usar como modelo principal.
No usar como modelo secundario todavía.
No usar como fallback automático.
No usar con secretos.
No usar con datos sensibles.
No usar en producción.
No usar para decisiones críticas.
No usar para acciones irreversibles.
No modificar modelo principal.
No activar routing.
No modificar gateway todavía.
No modificar configuración todavía.
```

---

## 3. Posible rol operativo

Uso candidato actual:

```text
modelo experimental LOW_SCOPE
```

No es todavía un modelo secundario.

No es fallback.

No forma parte de producción.

Tareas potencialmente aceptables:

- reformulación de texto no sensible;
- borradores de documentación genérica;
- clasificación simple de tareas;
- resúmenes de información ya pública o no sensible;
- generación de ejemplos sintéticos;
- checks de estilo;
- traducción no sensible;
- lluvia de ideas no operativa.

Tareas no aceptables:

- gestión de OpenClaw MAIN;
- edición de configuración;
- decisiones TASK_VALIDATOR;
- análisis con secretos;
- RAG con contenido privado;
- código que vaya directo a producción;
- acciones sobre servicios;
- routing;
- gateway;
- operaciones con tokens;
- análisis de datos industriales sensibles;
- fallback automático;
- rutas productivas;
- sustitución o degradación del modelo principal.

---

## 4. Evaluación de seguridad

Riesgo estimado: medio.

Motivos:

- modelo externo o experimental;
- garantías de aislamiento no verificadas desde este documento;
- posible logging por proveedor/intermediario;
- posible comportamiento inconsistente;
- no existe contrato operativo validado dentro de OpenClaw;
- no hay pruebas locales de refusal, privacidad ni estabilidad.

Condición mínima para pruebas futuras:

```text
Solo prompts sintéticos, no sensibles y explícitamente marcados como TEST.
```

---

## 5. Evaluación de privacidad

Riesgo estimado: medio-alto si se usa con datos reales.

No debe recibir:

- tokens;
- `.env`;
- `openclaw.json`;
- rutas privadas con contenido sensible;
- datos personales de Albert;
- memoria privada;
- logs con información operativa sensible;
- datos industriales reales;
- contenido RAG privado;
- detalles de infraestructura interna.

Uso aceptable futuro:

```text
contenido sintético, anonimizado o público
```

Si hay duda, no enviar.

---

## 6. Evaluación de estabilidad

Riesgo estimado: desconocido/medio.

Aspectos no verificados:

- latencia;
- tasa de errores;
- límites de uso;
- disponibilidad;
- consistencia de formato;
- compatibilidad con OpenClaude/OpenGateway;
- coste real;
- política de rate limit;
- manejo de streaming;
- timeouts.

Implicación:

```text
No debe formar parte de rutas críticas ni automatismos.
```

Validación futura mínima:

- estabilidad comprobada;
- comportamiento consistente;
- baja tasa de errores;
- latencia aceptable para pruebas manuales;
- bajo riesgo de alucinación observado.

---

## 7. Calidad en español

Estado: no verificado.

Criterios de evaluación futura:

- comprensión de instrucciones en español;
- tono natural y técnico;
- obediencia a restricciones;
- tendencia a inventar;
- calidad de resúmenes;
- capacidad de mantener formato exacto;
- manejo de terminología OpenClaw/Neodaemon;
- claridad para usuario no técnico.

Pruebas recomendadas futuras:

1. resumen de texto sintético;
2. reformulación breve;
3. clasificación low_scope/no_low_scope con ejemplos inventados;
4. extracción de bullets sin inferir;
5. respuesta en JSON estricto con datos ficticios.

---

## 8. Utilidad para LOW_SCOPE

Potencial utilidad: moderada, si supera pruebas.

Casos donde podría ayudar:

- reducir coste de tareas triviales;
- descargar tareas de redacción simple;
- generar borradores que MAIN revise;
- revisar lenguaje para usuario no técnico;
- clasificar incidencias no críticas.

Condición operativa:

```text
Todo output de MiMo debe ser revisado por MAIN antes de usarse.
```

Modo permitido actual:

```text
pruebas manuales controladas
comparación con modelo principal
tareas LOW_SCOPE únicamente
```

No debe tener capacidad autónoma.

No debe ejecutar herramientas.

No debe decidir acciones.

No debe tener integración automática con routing.

---

## 9. Riesgo de alucinación

Riesgo estimado: desconocido/medio-alto hasta prueba.

Riesgos concretos:

- inventar estado del sistema;
- asumir disponibilidad de servicios;
- rellenar datos inexistentes;
- crear comandos no verificados;
- simplificar demasiado políticas de seguridad;
- producir JSON inválido;
- ignorar límites de privacidad.

Mitigación mínima:

- prompts cortos;
- datos sintéticos;
- instrucciones explícitas de no inferir;
- salida validada por MAIN;
- no usar para diagnóstico operativo real;
- no conectar a acciones.

---

## 10. Límites operativos obligatorios

Si en el futuro se autoriza una prueba, debe cumplir:

```text
Modo: experimental_only
Scope: LOW_SCOPE
Datos: sintéticos/no sensibles
Herramientas: ninguna
Autonomía: ninguna
Persistencia: ninguna
Routing: no activo
Fallback automático: no activo
Producción: no activo
Gateway real: no tocar sin autorización explícita
```

No puede:

- llamar herramientas;
- escribir archivos;
- leer logs privados;
- acceder a memoria;
- acceder a RAG;
- recibir secretos;
- modificar configuración;
- participar en decisiones críticas;
- actuar como secondary;
- actuar como fallback automático.

---

## 11. Criterios de aceptación futura

Antes de considerarlo usable como auxiliar LOW_SCOPE, debería superar una batería mínima:

- responde en español claro;
- no inventa cuando falta información;
- respeta formato solicitado;
- rechaza o evita datos sensibles;
- no propone tocar gateway/runtime sin permiso;
- mantiene respuestas breves;
- puede clasificar tareas simples;
- no degrada seguridad de MAIN;
- coste/latencia justifican su uso.

Resultado esperado de una prueba:

```text
APTO_LOW_SCOPE_EXPERIMENTAL
NO_APTO
PENDIENTE_MAS_PRUEBAS
```

Solo si supera validación futura podrá abrirse una evaluación separada para posible integración como `secondary`.

Esa evaluación posterior requeriría autorización explícita y análisis de riesgo nuevo.

---

## 12. Recomendación

Recomendación actual:

```text
PENDIENTE_MAS_PRUEBAS
```

No implementar todavía.

No tocar gateway.

No modificar configuración.

No activar routing.

No usar con datos reales.

No usar como fallback automático.

No considerarlo `secondary` todavía.

Siguiente paso seguro, si Albert lo autoriza:

```text
Diseñar batería de prompts sintéticos para evaluación manual controlada.
```

---

## 13. Decisión actual

Estado operativo:

```text
EVALUADO SOLO EN PAPEL
EXPERIMENTAL_ONLY
NO IMPLEMENTADO
NO AUTORIZADO EN GATEWAY
NO CONFIGURADO
NO ROUTING
NO FALLBACK
NO SECONDARY
NO VERSIONADO
```

---

## 14. Ruta hacia posible secondary

Xiaomi MiMo no debe evaluarse como `secondary` hasta completar pruebas manuales controladas.

Condiciones previas obligatorias:

- estabilidad comprobada;
- comportamiento consistente;
- bajo riesgo de alucinación;
- calidad suficiente en español;
- obediencia fiable a restricciones;
- ausencia de datos sensibles en pruebas;
- revisión humana de resultados;
- autorización explícita de Albert para una fase nueva.

Solo entonces podrá plantearse:

```text
evaluar integración como secondary
```

Esa fase futura no queda autorizada por este documento.
