# 03_DAILY_RAG_FLOW

## Objetivo

Definir el flujo diario para alimentar el RAG con conocimiento curado sobre Microsoft Fabric aplicado a datos industriales de soldadura.

## Principio

Neodaemon busca y prefiltra.
Albert cura y decide.
Solo lo aprobado entra al RAG.

## Ciclo diario

1. Neodaemon busca 3 fuentes candidatas.
2. Neodaemon descarta contenido claramente genérico o marketing.
3. Neodaemon resume cada fuente en formato técnico.
4. Neodaemon propone aplicación concreta al sistema de soldadura.
5. Albert clasifica cada fuente:
   - entra
   - no entra
   - entra parcial
6. Solo las fuentes aprobadas se guardan como conocimiento.
7. Se actualiza el snapshot del proyecto.
8. Se valida el RAG con una pregunta real.

## Formato de propuesta diaria

Para cada fuente:

- titulo:
- url:
- tipo:
- calidad: alto / medio / bajo
- resumen tecnico:
- aplicacion al sistema:
- recomendacion: entra / no entra / parcial

## Limite diario

Maximo 3 fuentes candidatas por dia.
Maximo 1 o 2 entradas nuevas al RAG por dia.

## Criterio principal

Una fuente solo entra si mejora una decision tecnica o aporta un patron implementable.

## Validacion posterior

Pregunta minima de validacion:

Como ayuda este contenido a detectar inestabilidad en datos de soldadura en tiempo real?

Si la respuesta no mejora, el contenido se archiva o se descarta.

## Seguridad

No guardar secretos.
No guardar contenido completo con restricciones.
Guardar metadatos, resumen, aplicacion y enlace.

## Estado

Flujo definido.
Pendiente de automatizacion diaria.
