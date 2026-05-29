# Root API backup files security review

## Estado

Revisión pendiente.

## Contexto

La raíz del repositorio contiene archivos heredados relacionados con versiones anteriores de la API local:

- `api.py.backup-token`
- `api.py.save`
- `api.py.stable`
- `api_broken.py`

Estos archivos están versionados en Git y proceden de commits históricos de estabilización RAG.

## Hallazgos iniciales

La auditoría local mostró que:

- no hay referencias activas a estos archivos fuera del mapa de riesgos documental;
- varios archivos contienen referencias a `API_TOKEN`;
- no son duplicados triviales de `api.py`;
- algunos son versiones mucho más grandes que la API actual;
- borrarlos del árbol actual no eliminaría posibles secretos del historial Git.

## Evidencia local observada

Conteo de líneas:

- `api.py`: 54 líneas
- `api.py.backup-token`: 49 líneas
- `api.py.stable`: 83 líneas
- `api.py.save`: 311 líneas
- `api_broken.py`: 316 líneas

Comparación contra `api.py`:

- `api.py.backup-token`: 37 inserciones, 42 eliminaciones
- `api.py.stable`: 75 inserciones, 46 eliminaciones
- `api.py.save`: 300 inserciones, 43 eliminaciones
- `api_broken.py`: 306 inserciones, 43 eliminaciones

## Riesgos

### Riesgo de mantenerlos

- Debilitan la higiene del repositorio.
- Pueden confundir cuál es la API activa.
- Contienen referencias a token hardcodeado.
- Aumentan el ruido en la raíz del repositorio.

### Riesgo de borrarlos sin revisión

- Pueden contener contexto histórico útil.
- Si contienen secretos reales, borrarlos no soluciona la exposición en historial.
- Podría asumirse falsamente que el riesgo queda resuelto tras eliminarlos.

## Regla de seguridad

Eliminar archivos del árbol actual no elimina secretos del historial Git.

Si el token hardcodeado sigue siendo válido, la acción correcta no es solo borrar archivos, sino rotar y externalizar el token.

Borrar estos archivos del árbol actual no elimina posibles secretos del historial Git.

## Fuera de alcance

Esta revisión no:

- borra archivos;
- mueve archivos;
- modifica código;
- modifica `api.py`;
- modifica `api_rag_v2.py`;
- modifica systemd;
- modifica `.env`;
- modifica tokens;
- reescribe historial Git;
- cambia servicios activos.

## Decisiones pendientes

Antes de cualquier limpieza real hay que decidir:

1. Si los tokens hardcodeados siguen siendo válidos.
2. Si el token debe rotarse.
3. Si el token debe externalizarse fuera del código.
4. Si estos archivos deben eliminarse del árbol actual.
5. Si alguno debe conservarse como documentación histórica saneada.
6. Si merece la pena reescribir historial Git, o si el riesgo no lo justifica.

## Próximo paso recomendado

Abrir una tarea de seguridad separada para:

- revisar validez del token;
- planificar rotación;
- externalizar configuración sensible;
- decidir eliminación controlada de los archivos obsoletos.

No ejecutar ninguna limpieza hasta cerrar esa decisión.


