# LTU - Averías y soluciones

Registro personal de averías, equipos afectados, imágenes asociadas y soluciones aplicadas.

## Estándar operativo

Cada avería debe tener:

- 1 archivo `.md`
- 1 imagen asociada con el mismo ID

Estructura:

```text
LTU-0001.md
LTU-0001.jpg
```

Reglas:

- Un ID por avería: `LTU-0001`, `LTU-0002`, `LTU-0003`…
- Neodaemon asignará automáticamente el siguiente ID al añadir una nueva avería.
- El nombre de la imagen debe coincidir con el ID.
- Cada avería se documenta en su propio archivo `.md`.
- Si no existe ninguna avería previa, se empieza por `LTU-0001`.

## Plantilla

```markdown
## LTU-XXXX

nombre_avería:

equipo:

síntoma:

imagen:
![LTU-XXXX](LTU-XXXX.jpg)

causa probable:

solución aplicada:

resultado:

notas:
```

## Averías registradas

_Añadir cada avería en su propio archivo `.md` usando la plantilla anterior._
