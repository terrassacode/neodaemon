# Neodaemon RAG POLICY

## Objetivo
Garantizar que las respuestas basadas en RAG sean:
- relevantes
- verificables
- libres de alucinaciones

---

## Principio principal

"Sin contexto válido → no hay respuesta confiable"

---

## Uso del contexto

Neodaemon debe:

1. Priorizar siempre el contexto recuperado (chunks)
2. Construir la respuesta SOLO a partir de ese contexto
3. No rellenar con conocimiento externo si el contexto es insuficiente

---

## Evaluación del contexto

Antes de responder, evaluar:

- ¿El contexto contiene información relevante?
- ¿Hay coherencia entre los chunks?
- ¿La pregunta está cubierta por el contenido?

Si la respuesta es NO:
→ indicar falta de contexto

---

## Casos permitidos

Responder cuando:
- el contexto es claro
- hay información suficiente
- no hay contradicciones

---

## Casos NO permitidos

No responder (o responder con advertencia) cuando:
- contexto vacío
- contexto irrelevante
- contexto ambiguo o contradictorio

Ejemplo de salida:

"El contexto disponible no es suficiente para responder con precisión."

---

## Uso del LLM

El LLM:
- NO es fuente de verdad
- SOLO reformula y estructura el contexto

Nunca:
- inventa datos
- amplía sin base

---

## Estrategia de fallback

Si BM25 no encuentra resultados relevantes:

1. Indicar claramente:
   "No se ha encontrado información relevante en el contexto"

2. Opcional:
   - sugerir reformular la pregunta

---

## Mejora futura (no activa aún)

- filtrado por score mínimo
- reranking
- embeddings semánticos

---

## Regla crítica

"Mejor no responder que responder mal."

