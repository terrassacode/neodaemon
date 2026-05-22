# 27_DASHBOARD_V2_STATE.md

Status: dashboard-v2 saneado localmente  
Scope: documentación de estado, sin versionar artefacto HTML todavía  
Última actualización: 2026-05-22

---

## 1. Estado general

`dashboard-v2` está actualmente en estado local saneado.

No está versionado todavía como artefacto propio.

Decisión vigente:

```text
No usar git add . en /openclaw/workspace/main
```

Motivo:

- `/openclaw/workspace/main` contiene muchos archivos no trackeados;
- versionar todo el workspace mezclaria datos, logs, scripts, documentación y artefactos locales;
- `dashboard-v2` aún debe estabilizarse antes de decidir estrategia Git propia.

---

## 2. Estado visual y funcional del dashboard

### 2.1 Acciones rápidas MAIN

El bloque `Acciones rápidas MAIN` está situado arriba del dashboard, justo después del header.

Función:

- accesos seguros;
- sin acciones runtime;
- sin reinicios;
- sin RAG;
- sin controles peligrosos.

### 2.2 Resource Usage

`Resource Usage` es el único enlace real principal desde `Acciones rápidas MAIN`.

Enlace esperado:

```html
href="tools/resource-usage.html"
```

Regla vigente:

- no duplicar botones/enlaces Resource Usage en otros bloques;
- sí se permite mencionarlo como fuente.

Fuente viva principal del dashboard:

```text
Resource Usage
```

### 2.3 API obsoleta eliminada

Se eliminaron del dashboard principal:

```text
API_TOKEN
API_BASE_URL
apiCall
```

Objetivo:

- evitar exposición de tokens;
- eliminar lógica API obsoleta;
- mantener el dashboard sin llamadas runtime peligrosas.

### 2.4 RAG eliminado del dashboard principal

Se eliminaron controles visibles y lógica asociada a:

```text
/rag-ask
/rag-search
RAG ask
RAG search
formularios RAG
botones RAG
```

Estado permitido:

- RAG puede aparecer solo como estado `PAUSADO` o referencia documental futura;
- no debe haber controles RAG activos en el dashboard principal.

### 2.5 Header corregido

El header ya no debe mostrar etiquetas obsoletas como:

```text
sin servidor
sin JS dinámico
```

Etiquetas actuales esperadas:

```text
1 métrica real
servido localmente
JS ligero
sin runtime en dashboard
```

### 2.6 Resumen diario

El bloque `Resumen diario` está alineado con la nueva estructura de:

```text
dashboard-v2/data/daily_summary.json
```

Estructura esperada:

```text
date
day_assessment
summary[]
activity.improvements
activity.validations
activity.blocked
system_health.status
system_health.restarts
system_health.errors
```

Si no hay datos, debe mostrar:

```text
Sin resumen diario disponible
```

### 2.7 Mapa documental

`Mapa documental MAIN` sigue presente como sección.

El acceso rápido `Mapa documental` ya no debe usar:

```html
href="#"
```

Debe ser texto no clicable o badge visual hasta que exista destino real.

### 2.8 LTU Averías

`LTU Averías` sigue pendiente de vista.

Estado esperado:

```text
LTU Averías · pendiente de vista
```

Regla vigente:

- no enlazar a `personal/index.html` si no existe vista específica de LTU Averías;
- no crear página LTU todavía sin autorización separada.

---

## 3. Política de versionado actual

Estado:

```text
dashboard-v2 local, no versionado todavía
```

Reglas:

- no hacer `git add .` en `/openclaw/workspace/main`;
- no hacer commit/push todavía;
- no versionar logs o JSON generados sin política explícita;
- documentar estado y decisiones en `context_repo` mientras se decide la estrategia definitiva.

---

## 4. Pendiente futuro

Decisión pendiente:

```text
Decidir si dashboard-v2 tendrá repo propio.
```

Opciones futuras:

1. mantener local y documentado;
2. versionar selectivamente con `.gitignore` estricto;
3. crear repo separado para `dashboard-v2`;
4. consolidar solo documentación en `context_repo`.

Recomendación actual:

```text
Mantener dashboard-v2 local y documentar estado en context_repo hasta estabilizarlo.
```

---

## 5. No tocar sin autorización explícita

No tocar como parte de este estado:

- runtime;
- servicios;
- gateway;
- routing;
- RAG runtime;
- modelos;
- tokens;
- dashboard HTML salvo petición específica;
- scripts salvo petición específica;
- Git commit/push.
