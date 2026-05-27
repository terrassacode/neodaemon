# Source Note — OpenClaw Knowledge Wiki README

## Fuente

- `raw/notes/first-source-openclaw-knowledge-wiki-readme.md`

## Tipo

Fuente interna no sensible del propio proyecto.

## Resumen

El README define el propósito, límites y flujo manual de OpenClaw Knowledge Wiki.

El proyecto funciona como shell aislado para construir una wiki operativa local, inspirada en patrones LLM Wiki / Obsidian / Claude Code, pero adaptada a Neodaemon y sin automatización activa.

## Datos confirmados

- El proyecto es documental y local.
- `raw/` es inmutable.
- `wiki/` es generado por Neodaemon.
- `wiki/index.md` actúa como catálogo maestro.
- `wiki/log.md` es append-only.
- Cada ingest debe usar máximo 3 fuentes.
- Obsidian es opcional y no es dependencia obligatoria.
- No se deben usar APIs externas.
- No se deben instalar dependencias.
- No se deben ejecutar scripts globales.
- No se debe escribir fuera del proyecto.

## Inferencias

- El flujo está diseñado para priorizar trazabilidad antes que automatización.
- La separación `raw/` → `wiki/` busca preservar fuentes originales y permitir notas derivadas.
- `outputs/lint/` queda reservado para revisiones manuales de calidad documental.

## Dudas o límites

- Aún no hay fuentes externas autorizadas.
- Aún no hay taxonomía madura para `concepts/`, `entities/`, `sources/` y `comparisons/`.
- Aún no existe un proceso automatizado de lint, y no debe implementarse sin autorización futura.

## Conceptos relacionados

- wiki generada por Neodaemon
- raw inmutable
- ingest manual
- catálogo maestro
- log append-only
- aislamiento de proyecto

## Enlaces internos

- `wiki/index.md`
- `wiki/log.md`
- `NEODAEMON_WIKI.md`
