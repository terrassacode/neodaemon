# 36_OPENCLAW_BASE_ADDONS_ARCHITECTURE.md

Status: DESIGN_ONLY  
Scope: arquitectura segura BASE + ADDONS para OpenClaw  
Última actualización: 2026-05-23

---

## 1. Objetivo

Definir una arquitectura de evolución segura para OpenClaw donde la base estable se mantiene intacta y los nuevos módulos se desarrollan como addons aislados, reversibles y promocionables solo tras validación.

Este documento es solo diseño.

No autoriza:

- crear carpetas todavía;
- modificar configuración real;
- tocar gateway;
- tocar runtime;
- tocar servicios;
- activar automatizaciones;
- integrar addons en MAIN.

---

## 2. Principio central

```text
BASE = no tocar
ADDONS = aislados, reversibles y promocionables solo tras validación
```

Interpretación:

- `BASE` contiene el sistema estable y operativo.
- `ADDONS` contiene experimentos, integraciones nuevas y módulos en sandbox.
- Nada experimental debe acoplarse directamente a MAIN.
- Un addon no se convierte en parte del sistema estable hasta superar validación, rollback y autorización explícita de Albert.

---

## 3. BASE

Ruta base actual:

```text
/openclaw/workspace/main
```

Reglas para BASE:

- no tocar para experimentos;
- no mezclar credenciales experimentales;
- no activar servicios nuevos directamente;
- no introducir dependencias no validadas;
- no usar como zona de pruebas runtime;
- documentar diseños y decisiones, pero no ejecutar integraciones sin confirmación.

BASE conserva:

- identidad Neodaemon/MAIN;
- memoria operativa;
- documentación controlada;
- políticas;
- runbooks;
- dashboard estable;
- coordinación principal.

---

## 4. ADDONS

Ruta propuesta futura:

```text
/openclaw/workspace/addons
```

Cada addon debe ser autocontenido, aislado y auditable.

Estructura propuesta:

```text
/openclaw/workspace/main
/openclaw/workspace/addons
/openclaw/workspace/addons/gmail-readonly
/openclaw/workspace/addons/mimo-voice
/openclaw/workspace/addons/web-search-tests
```

Estado actual:

```text
NO_CREAR_CARPETAS_TODAVÍA
SOLO_DOCUMENTADO
```

---

## 5. Requisitos mínimos por addon

Cada addon debe contener como mínimo:

```text
README.md
STATUS.md
ROLLBACK.md
.env.example
.venv/
logs/
tests/
```

### 5.1 README.md

Debe explicar:

- objetivo del addon;
- límites;
- dependencias;
- cómo probarlo;
- qué NO hace;
- relación con MAIN.

### 5.2 STATUS.md

Debe indicar:

- estado actual;
- última validación;
- riesgos conocidos;
- permisos usados;
- si está conectado o no;
- si tiene automatización o no.

### 5.3 ROLLBACK.md

Debe incluir:

- cómo desactivar el addon;
- cómo revocar credenciales;
- cómo eliminar tokens locales;
- cómo parar procesos si existieran;
- cómo confirmar que no queda integrado en MAIN.

### 5.4 .env.example

Debe incluir solo nombres de variables, nunca valores reales.

Permitido:

```text
GMAIL_CLIENT_SECRET_PATH=
GMAIL_TOKEN_PATH=
```

Prohibido:

```text
TOKEN_REAL=...
CLIENT_SECRET_REAL=...
```

### 5.5 .venv/

Cada addon debe tener entorno aislado si necesita dependencias Python/Node.

Reglas:

- no instalar dependencias en BASE;
- no compartir venv con MAIN;
- documentar paquetes mínimos;
- reproducibilidad antes de integración.

### 5.6 logs/

Logs locales del addon.

Reglas:

- sin secretos;
- sin tokens;
- sin cuerpos completos sensibles;
- rotación o limpieza definida si crece;
- nunca usar logs como memoria operativa.

### 5.7 tests/

Debe contener pruebas mínimas:

- test de importación;
- test de configuración incompleta;
- test de modo dry-run;
- test de rollback si aplica;
- test de no exposición de secretos si es viable.

---

## 6. Reglas globales para addons

Reglas obligatorias:

- no tocar MAIN;
- no tocar gateway;
- no tocar runtime;
- no tocar servicios;
- no compartir secretos;
- no usar puertos sin declarar;
- no automatizar sin revisión;
- no instalar dependencias globales;
- no modificar routing;
- no cambiar modelos activos;
- no asumir permisos de producción;
- no escribir fuera de su carpeta salvo autorización explícita;
- no usar datos sensibles salvo fase autorizada y documentada.

---

## 7. Puertos, procesos y automatización

Un addon no debe abrir puertos ni procesos persistentes sin declarar:

```text
puerto:
proceso:
comando de arranque:
comando de parada:
logs:
riesgo:
rollback:
```

Automatización prohibida por defecto.

Para activar automatización futura se requiere:

1. diseño;
2. análisis de riesgo;
3. rollback;
4. validación manual;
5. autorización explícita de Albert;
6. documentación de estado.

---

## 8. Secretos y credenciales

Reglas:

- secretos fuera de repo;
- `.env.example` sí, `.env` real no versionado;
- tokens fuera de Git;
- recovery codes fuera de workspace;
- no imprimir secretos;
- no copiar secretos a logs;
- no compartir credenciales entre addons salvo decisión explícita.

Cada addon debe documentar:

```text
secretos requeridos:
ruta segura recomendada:
scopes/permisos:
revocación:
```

---

## 9. Criterio de promoción

Un addon solo puede promocionarse hacia integración con BASE si cumple:

- test OK;
- rollback definido;
- sin secretos en repo;
- permisos mínimos;
- riesgo bajo;
- logs seguros;
- dependencias documentadas;
- sin puertos no declarados;
- sin automatización oculta;
- estado actualizado en `STATUS.md`;
- autorización explícita de Albert.

Promoción significa:

```text
pasar de sandbox aislado a integración controlada
```

No significa producción automática.

---

## 10. Estados posibles de un addon

```text
DESIGN_ONLY
SANDBOX
LOCAL_TESTED
READY_FOR_REVIEW
APPROVED_FOR_LIMITED_INTEGRATION
INTEGRATED_CONTROLLED
PAUSED
REVOKED
```

Definiciones:

- `DESIGN_ONLY`: solo documentación.
- `SANDBOX`: existe carpeta aislada, sin integración MAIN.
- `LOCAL_TESTED`: pruebas locales OK.
- `READY_FOR_REVIEW`: preparado para revisión humana.
- `APPROVED_FOR_LIMITED_INTEGRATION`: Albert autorizó integración limitada.
- `INTEGRATED_CONTROLLED`: integrado con límites y rollback.
- `PAUSED`: detenido sin eliminar.
- `REVOKED`: acceso/credenciales revocados.

---

## 11. Aplicación inmediata: addon gmail-readonly

Addon propuesto:

```text
gmail-readonly
```

Path futuro:

```text
/openclaw/workspace/addons/gmail-readonly
```

Estado:

```text
sandbox
```

Scope objetivo:

```text
https://www.googleapis.com/auth/gmail.readonly
```

Reglas inmediatas:

- sin servicio;
- sin automatización;
- sin integración MAIN todavía;
- sin envío;
- sin modificación de buzón;
- sin descarga automática de adjuntos;
- sin credenciales en repo;
- credenciales fuera de `/openclaw/workspace/main`;
- rollback definido antes de OAuth real.

Estructura futura esperada:

```text
/openclaw/workspace/addons/gmail-readonly/
  README.md
  STATUS.md
  ROLLBACK.md
  .env.example
  .venv/
  logs/
  tests/
```

Estado actual real:

```text
NO_CREADO
SOLO_DOCUMENTADO
```

---

## 12. Relación con Neodaemon/MAIN

Neodaemon/MAIN sigue siendo coordinador.

Los addons no sustituyen a MAIN.

Flujo correcto:

```text
Albert → Neodaemon/MAIN → revisión/diseño addon → validación → autorización → integración limitada si procede
```

Flujo prohibido:

```text
addon experimental → modifica MAIN directamente
addon experimental → toca gateway
addon experimental → activa servicio sin revisión
addon experimental → usa secretos compartidos
```

---

## 13. Checklist antes de crear un addon

Antes de crear una carpeta en `/openclaw/workspace/addons`, confirmar:

- nombre del addon;
- objetivo;
- permisos mínimos;
- ubicación de secretos;
- dependencias;
- si requiere red;
- si requiere puerto;
- si requiere servicio;
- rollback;
- prueba mínima;
- autorización de Albert.

---

## 14. Estado actual de esta arquitectura

```text
BASE_ADDONS_ARCHITECTURE_DESIGN_CREATED
NO_ADDONS_FOLDER_CREATED
NO_CONFIG_CHANGED
NO_GATEWAY_CHANGED
NO_RUNTIME_CHANGED
NO_SERVICES_CHANGED
NO_AUTOMATION_ENABLED
```

---

## 15. Próximo paso seguro

Si Albert autoriza avanzar:

1. crear `/openclaw/workspace/addons/gmail-readonly`;
2. crear archivos mínimos del addon;
3. mantenerlo sin servicio y sin automatización;
4. documentar credenciales esperadas sin valores reales;
5. preparar prueba local read-only aislada;
6. revisar antes de cualquier OAuth real.

Hasta entonces:

```text
SOLO_DOCUMENTAR
```
