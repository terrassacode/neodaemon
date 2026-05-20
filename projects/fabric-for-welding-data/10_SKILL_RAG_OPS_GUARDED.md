# 10_SKILL_RAG_OPS_GUARDED

## Objetivo

Definir una skill operativa para Neodaemon con acceso limitado al host, diseñada para ejecutar tareas controladas del RAG local sin convertir a Neodaemon en un operador libre del sistema.

La skill debe reducir el trabajo manual de Albert sin perder seguridad.

---

## Nombre propuesto

```text
rag_ops_guarded
```

---

## Principio base

```text
Acceso mínimo, comandos cerrados, rutas permitidas, autorización humana para acciones de riesgo.
```

Neodaemon no debe recibir acceso general al host.

Debe recibir capacidad limitada para ejecutar flujos específicos, auditables y reversibles.

---

## Roles

| Rol | Responsabilidad |
|---|---|
| ChatGPT | Diseña estrategia, revisa decisiones, detecta riesgos |
| Neodaemon | Ejecuta operaciones controladas mediante skill |
| Albert | Autoriza acciones de escritura, reinicio o cambio operativo |
| GitHub | Registra estado, decisiones, validaciones y handoff |
| Host OpenClaw | Ejecuta comandos limitados |

---

## Rutas permitidas

### Lectura permitida

```text
/openclaw/api_rag_v2.py
/openclaw/rag_loader.py
/openclaw/rag_retriever.py
/openclaw/rag_filter.py
/openclaw/workspace/main/rag_store/chunks_v2/
/openclaw/workspace/main/context_repo/
/home/openclaw/.config/systemd/user/openclaw-rag-v2.service
```

### Escritura permitida con autorización explícita

```text
/openclaw/api_rag_v2.py
/openclaw/workspace/main/rag_store/chunks_v2/*.json
/openclaw/workspace/main/context_repo/projects/fabric-for-welding-data/*.md
```

### Escritura prohibida salvo autorización especial

```text
/home/openclaw/.openclaw/
/openclaw/.env
archivos de tokens
configuración gateway
configuración Telegram
systemd units no relacionados con RAG
```

---

## Comandos permitidos

### Lectura/inspección

```bash
grep
sed
cat
ls
find
systemctl --user status openclaw-rag-v2.service --no-pager
journalctl --user -u openclaw-rag-v2.service --since "N minutes ago" --no-pager
```

### Validación

```bash
python3 -m py_compile /openclaw/api_rag_v2.py
python3 -m json.tool <chunk_json>
```

### Pruebas controladas

```bash
/openclaw/venvs/litellm/bin/python - <<'PY'
# pruebas concretas permitidas
PY
```

### Servicio RAG

Permitido solo con autorización explícita:

```bash
systemctl --user restart openclaw-rag-v2.service
```

---

## Comandos prohibidos

```bash
sudo
rm -rf
chmod/chown sobre rutas sensibles
apt install
pip install sin autorización
curl externo no autorizado
wget externo no autorizado
systemctl restart de servicios no relacionados
lectura directa de secretos/tokens para mostrarlos
edición de gateway, Telegram o auth
```

---

## Política de autorización

| Acción | Requiere OK de Albert |
|---|---|
| Leer archivos permitidos | No, si está dentro de la skill |
| Crear backup | Sí, si acompaña escritura |
| Modificar `api_rag_v2.py` | Sí |
| Crear/modificar chunk JSON | Sí |
| Reiniciar `openclaw-rag-v2.service` | Sí |
| Consultar `/rag-ask` local | Sí si usa token |
| Tocar tokens/gateway/Telegram | Sí, autorización especial |

---

## Flujo estándar de parche

1. Inspección de archivo objetivo.
2. Propuesta de cambio mínimo.
3. TASK_VALIDATOR.
4. Autorización de Albert.
5. Backup timestamp.
6. Aplicación de parche.
7. Validación sintáctica.
8. Prueba artificial.
9. Reinicio solo si se autoriza.
10. Prueba funcional.
11. Documentación en GitHub.

---

## Formato obligatorio TASK_VALIDATOR

```json
{
  "action": "...",
  "type": "read|write|system",
  "risk_score": 0,
  "risk_level": "low|medium|high",
  "reasons": [],
  "affected_paths": [],
  "command_preview": "...",
  "rollback": "...",
  "validation": "...",
  "safe_to_execute": false
}
```

---

## Salida obligatoria tras ejecutar

```text
HECHO / BLOQUEADO / ERROR

Archivos tocados:
Backups creados:
Comandos ejecutados:
Validación:
Servicios reiniciados:
Errores:
Rollback disponible:
Siguiente acción recomendada:
```

---

## Modo seguro por defecto

La skill debe operar por defecto en modo:

```text
read-only / dry-run
```

Solo cambia a modo escritura cuando Albert autoriza explícitamente.

---

## Aplicación inmediata

Esta skill debe usarse antes de P2 para evitar que Albert actúe como copiador de comandos.

Objetivo inmediato:

```text
Cerrar P1/P2 con menos copia-pega manual y más ejecución guiada por Neodaemon.
```

---

## Criterio de cierre de esta skill

La skill se considera definida cuando:

1. Sus rutas permitidas están claras.
2. Sus comandos permitidos están claros.
3. Sus prohibiciones están claras.
4. Existe TASK_VALIDATOR obligatorio.
5. Existe flujo de rollback.
6. Se prueba primero en modo solo lectura.
