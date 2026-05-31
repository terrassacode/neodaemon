# Repo root inventory and risk map

## Estado

Mapa de riesgo creado.

## Propósito

Este documento registra el estado actual de la raíz del repositorio `terrassacode/neodaemon` y los riesgos de reorganizar archivos sin romper servicios existentes.

No es un plan de limpieza inmediata.

## Problema observado

La raíz del repositorio contiene documentación, scripts, backups lógicos, versiones antiguas y código activo mezclado.

Esto reduce claridad, pero mover archivos sin análisis puede romper OpenClaw.

## Evidencia crítica

Hay referencias directas por rutas absolutas a archivos de raíz:

- `/openclaw/api_rag_v2.py`
- `/openclaw/api.py`
- `/openclaw/rag_loader.py`
- `/openclaw/rag_retriever.py`

Además, systemd usa directamente:

- `/openclaw/api_rag_v2.py`
- `/openclaw/api.py`
- `/openclaw/bots/telegram_rag_bot.py`
- `/openclaw/.env`

## Dependencias confirmadas

Las siguientes dependencias han sido verificadas durante la auditoría:

### systemd

- openclaw-rag-v2.service -> /openclaw/api_rag_v2.py
- openclaw-api.service -> /openclaw/api.py
- telegram-rag.service -> /openclaw/bots/telegram_rag_bot.py

### Configuración

- telegram_rag_bot.py -> ~/.openclaw/openclaw.json

### Scripts operativos

- scripts/rag_ops/rag_query_local.sh -> /openclaw/api_rag_v2.py
- scripts/rag_ops/rag_py_compile.sh -> /openclaw/api_rag_v2.py
- scripts/rag_ops/rag_test_bm25.sh -> rag_loader.py
- scripts/rag_ops/rag_test_bm25.sh -> rag_retriever.py

Estas dependencias deben considerarse activas hasta demostrar lo contrario.


## Riesgo principal

Mover, borrar o renombrar archivos raíz puede romper:

- servicios systemd;
- scripts de validación RAG;
- imports Python;
- documentación operativa;
- Telegram RAG bot;
- arranque de OpenClaw.

## Archivos raíz que requieren revisión especial

- `api.py`
- `api_rag_v2.py`
- `rag_loader.py`
- `rag_retriever.py`
- `api.py.backup-token`
- `api.py.save`
- `api.py.stable`
- `api_broken.py`
- `openclaw.json`

## Regla operativa

No mover, borrar ni renombrar archivos raíz usados por rutas absolutas hasta completar una fase previa de trazado de dependencias.

## Fuera de alcance

Este documento no:

- mueve archivos;
- borra archivos;
- modifica código;
- modifica systemd;
- modifica `.env`;
- modifica tokens;
- modifica configuración;
- cambia rutas de servicios;
- limpia backups;
- reorganiza carpetas.

## Criterios de bloqueo para una limpieza futura

Una limpieza futura debe bloquearse si:

- no se han revisado referencias systemd;
- no se han revisado imports Python;
- no se han revisado scripts;
- no se ha definido rollback;
- no se ha validado `py_compile`;
- no se ha comprobado arranque de servicios;
- no se ha comprobado Telegram;
- no se ha comprobado RAG.

## Próximos pasos seguros

Antes de cualquier reestructuración real:

1. Crear inventario completo de referencias.
2. Separar archivos activos de históricos.
3. Definir wrappers o rutas compatibles.
4. Probar cambios en rama.
5. Validar servicios.
6. Solo después considerar movimientos o limpieza.

