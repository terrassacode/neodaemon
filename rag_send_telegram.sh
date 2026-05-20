#!/bin/bash

DIR="/openclaw/workspace/main/rag_input/candidate"

for file in "$DIR"/*.json; do
  [ -e "$file" ] || exit 0

  TITLE=$(jq -r '.title' "$file")
  URL=$(jq -r '.url' "$file")
  SOURCE=$(jq -r '.source' "$file")

  MESSAGE="📄 *Nuevo candidato RAG*
  
*Fuente:* $SOURCE
*Título:* $TITLE

$URL

¿Aprobar o rechazar?"

  /openclaw/utils/send_telegram.sh "$MESSAGE" "$file"
done
