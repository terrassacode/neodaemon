def filter_results(results):
    cleaned = []

    for r in results:
        text = r.get("text", "")
        block_type = r.get("block_type", "")

        # eliminar list_items pobres
        if block_type == "list_item" and len(text) < 200:
            continue

        # eliminar textos demasiado cortos
        if len(text.strip()) < 80:
            continue

        cleaned.append(r)

    return cleaned
