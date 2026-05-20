# 16_RAG_OPS_WRAPPER_CONTRACT

Ruta oficial actual:
/openclaw/workspace/main/context_repo/scripts/rag_ops/

Wrappers disponibles:
- rag_status_readonly.sh
- rag_count_chunks.sh
- rag_py_compile.sh
- rag_test_bm25.sh
- rag_query_local.sh

Contrato:
- Usar siempre la ruta oficial actual.
- Interpretar el ultimo STATUS como estado final.
- Leer RESULT como resultado principal.
- No pedir comandos directos si existe wrapper oficial.
- rag_query_local.sh requiere autorizacion explicita.
- Si no existe wrapper autorizado, responder BLOQUEADO.
