# Obsidian Operating Rules

## Fuente

- `README.md`
- `NEODAEMON_WIKI.md`
- `wiki/log.md`
- `wiki/concepts/project-core-boundary.md`

## Propósito

Definir cómo usar Obsidian como visor/editor Markdown local de OpenClaw Knowledge Wiki sin romper aislamiento, trazabilidad ni seguridad.

## Vault oficial

La única vault autorizada para esta wiki es:

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki
```

No abrir como vault:

- /openclaw
- /openclaw/workspace/main
- /openclaw/workspace/main/projects

## Datos confirmados

- Obsidian es opcional.
- Obsidian puede usarse como visor/editor Markdown local.
- Obsidian no razona, no ingiere fuentes y no valida contenido.
- La generación y mantenimiento de la wiki corresponde a Neodaemon bajo autorización de Albert.
- `raw/` es inmutable.
- `wiki/log.md` es append-only.
- No se debe escribir fuera del proyecto.
- No se deben usar APIs externas desde este proyecto.
- No se deben instalar dependencias ni ejecutar scripts globales.

## Reglas operativas

1. Abrir únicamente la vault oficial.
2. No abrir `/openclaw` entero como vault.
3. No abrir `/openclaw/workspace/main` como vault.
4. No copiar la vault al móvil.
5. Acceso móvil recomendado: Tailscale + RDP a la VM.
6. No usar Obsidian Sync por ahora.
7. No instalar plugins por ahora.
8. No conectar gateway, auth, tokens ni servicios OpenClaw desde Obsidian.
9. No editar `raw/` salvo autorización explícita y proceso de ingest controlado.
10. No usar Obsidian para saltarse Neodaemon, TASK_VALIDATOR o Git.
11. Cambios importantes deben pasar por Neodaemon + Git.
12. `.obsidian/` no debe versionarse por ahora.

## Acceso móvil

El móvil Android no debe contener copia local de la vault.

Patrón recomendado:

```text
Android → Tailscale → RDP → sesión Ubuntu en bunker-ia → Obsidian local
```

Ventajas:

- la vault permanece dentro de la VM;
- no se duplican notas en el móvil;
- no se exponen rutas OpenClaw fuera de Tailscale;
- se mantiene control operacional centralizado.

## Cambios permitidos desde Obsidian

Cambios de bajo riesgo:

- editar notas Markdown dentro de `wiki/`;
- revisar enlaces internos;
- corregir texto menor;
- navegar la wiki;
- preparar borradores locales dentro del proyecto.

Cambios que requieren Neodaemon:

- crear nuevas notas conceptuales relevantes;
- modificar `wiki/index.md`;
- modificar `wiki/log.md`;
- tocar `raw/`;
- cambiar reglas operativas;
- añadir fuentes;
- preparar commits;
- cualquier cambio con impacto en seguridad o trazabilidad.

## `.obsidian/`

Por ahora:

- `.obsidian/` puede existir como configuración local del editor;
- no debe versionarse;
- no debe contener secretos;
- no debe usarse para automatización;
- no debe incluir plugins no autorizados.

Si en el futuro se decide versionar parte de `.obsidian/`, debe hacerse con revisión explícita de Albert.

## Inferencias

- Obsidian es interfaz, no autoridad operativa.
- Abrir una ruta demasiado amplia como vault aumenta riesgo de modificar core o archivos sensibles.
- Tailscale + RDP conserva mejor el aislamiento que sincronizar la vault al móvil.
- Git debe seguir siendo el mecanismo de trazabilidad para cambios importantes.

## Dudas o límites

- No se define todavía configuración exacta de RDP/Tailscale.
- No se define política final para `.obsidian/`.
- No se autoriza instalación de plugins.
- No se autoriza Obsidian Sync.
- Esta nota no sustituye TASK_VALIDATOR ni confirmación humana.

## Checklist rápida

Antes de usar Obsidian:

- ¿La vault abierta es exactamente `/openclaw/workspace/main/projects/openclaw-knowledge-wiki`?
- ¿No se está editando `raw/`?
- ¿No se está copiando la vault al móvil?
- ¿No hay plugins nuevos?
- ¿No se usa Obsidian Sync?
- ¿No se han conectado tokens, gateway, auth ni servicios?
- ¿Los cambios importantes pasarán por Neodaemon + Git?
