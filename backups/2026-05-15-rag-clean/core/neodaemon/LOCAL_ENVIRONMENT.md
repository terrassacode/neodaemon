# Neodaemon LOCAL ENVIRONMENT

## Infraestructura

Entorno:
- local (máquina virtual Ubuntu)
- red privada vía Tailscale
- acceso desde móvil mediante IP Tailscale

---

## Red

- IP Tailscale: 100.117.135.114
- Puerto API: 5000
- Puerto Dashboard: 8000

Endpoints principales:

- http://100.117.135.114:5000/health
- http://100.117.135.114:5000/rag-ask
- http://100.117.135.114:8000/

---

## Servicios activos

### API

- Servicio: openclaw-api.service
- Ruta: /openclaw/api.py
- Ejecuta:
  /openclaw/venvs/api/bin/python

Funciones:
- RAG (/rag-ask)
- control sistema (/summary, /last-events, restart)

---

### Dashboard

- Tipo: estático (http.server)
- Ruta:
  /openclaw/workspace/main/dashboard-v2
- Puerto: 8000

---

### LLM (Ollama)

- Host: local (127.0.0.1)
- Puerto: 11434
- Modelo activo:
  llama3.2:3b

Uso:
- vía API HTTP (/api/generate)

---

## RAG

- Motor: BM25
- Ruta chunks:
  /openclaw/workspace/main/rag_store/chunks

- Script búsqueda:
  search_bm25.py

---

## Tokens

- API_TOKEN:
  neodaemon-secure-token

Uso:
- autenticación en endpoints API

---

## Rutas críticas

- API:
  /openclaw/api.py

- Dashboard:
  /openclaw/workspace/main/dashboard-v2/index.html

- Logs:
  /openclaw/logs/

- Snapshots:
  /openclaw/snapshots/

---

## Riesgos conocidos

1. Dependencia de Tailscale
→ sin VPN, no hay acceso externo

2. API caída
→ rompe dashboard (Failed to fetch)

3. Cambios en api.py
→ pueden romper endpoints existentes

4. Modelo LLM limitado (3B)
→ menor calidad, depende de RAG

---

## Principio operativo

"Si algo falla, primero verificar:
1. servicio API activo
2. endpoint /health
3. red (Tailscale)
4. logs del sistema"

