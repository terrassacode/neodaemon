# 04_CURATION_CRITERIA

## Objetivo

Definir reglas estrictas para decidir qué información entra en el RAG y mantener un sistema limpio, útil y accionable.

## Criterio de entrada al RAG

Una fuente entra en el RAG solo si cumple todos los puntos:

1. Es técnica, no marketing.
2. Explica cómo implementar algo, no solo conceptos.
3. Es aplicable a streaming, KQL o análisis de series temporales.
4. Puede conectarse directamente con RD, variabilidad, robot, programa o detección de comportamiento.
5. Cambia o mejora una decisión en el sistema.

## Criterio de descarte

Se descarta si:

- Es contenido genérico o introductorio.
- No aporta implementación práctica.
- Es repetitivo respecto a lo ya guardado.
- No se puede aplicar al sistema en menos de 5 minutos de razonamiento.
- No tiene relación directa con el modelo HOT o análisis en tiempo real.

## Criterio parcial

Puede entrar parcialmente si:

- Contiene una idea útil mezclada con ruido.
- Solo se puede extraer una parte aplicable.

En ese caso se guarda solo la parte útil.

## Regla de oro

Si una fuente no cambia cómo se toman decisiones en el sistema, no entra en el RAG.

## Control de calidad

Cada entrada debe evaluarse como:

- ALTO: entra directo.
- MEDIO: entra parcial.
- BAJO: descartado.

## Validación post-ingesta

Después de añadir contenido:

1. Consultar al RAG con una pregunta real.
2. Verificar si la respuesta mejora.
3. Si no mejora, eliminar o archivar el contenido.

## Principio fundamental

El RAG no es un repositorio de información.

Es un sistema de conocimiento curado para tomar decisiones.
