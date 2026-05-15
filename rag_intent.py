def detect_intent(question):
    q = question.lower()

    if any(x in q for x in ["vs", "diferencia", "diferencias", "comparar", "comparación", "cuando usar", "cuándo usar"]):
        return "comparison"

    if any(x in q for x in ["qué es", "que es", "definición", "define"]):
        return "definition"

    if any(x in q for x in ["cómo", "como", "pasos", "configurar", "crear"]):
        return "howto"

    return "default"
