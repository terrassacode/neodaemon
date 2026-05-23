# Neodaemon web search enablement

## Purpose

Document the steps and findings required to expose internet read-only search to Neodaemon/MAIN in OpenClaw without enabling fetch, exec, browser automation, or broader runtime access.

## Final result

Web search is now visible to the MAIN agent as:

```text
web_search
```

The agent-reported tools after the fix were:

```text
read
write
apply_patch
memory_get
web_search
multi_tool_use.parallel
```

## Key lesson

Global web configuration is not enough. OpenClaw requires the tool to be allowed at the agent level.

```text
tools.web.search.enabled = true
```

is necessary but not sufficient if the agent has its own restricted `tools.allow` list.

## Confirmed working components

### Global web search configuration

The global config had web search enabled with DuckDuckGo and fetch disabled:

```json
"tools": {
  "profile": "coding",
  "web": {
    "search": {
      "enabled": true,
      "provider": "duckduckgo"
    },
    "fetch": {
      "enabled": false
    }
  },
  "alsoAllow": [
    "web_search"
  ]
}
```

### Plugin state

`duckduckgo` and `firecrawl` were confirmed loaded after activation:

```text
duckduckgo: loaded, capability web-search: duckduckgo
firecrawl: loaded, capability web-search: firecrawl
```

`openclaw infer web search --query "faster-whisper documentation"` worked locally and returned results via DuckDuckGo.

This proved that OpenClaw itself had internet search available.

## Actual blocker

The MAIN agent had a per-agent allowlist:

```json
"tools": {
  "allow": [
    "read",
    "write",
    "memory_get"
  ]
}
```

Because of this, the agent reported:

```text
capabilities=none
```

and did not receive `web_search`, even though the gateway and plugins were correctly configured.

## Final required change

Add `web_search` to the MAIN agent tool allowlist:

```json
"tools": {
  "allow": [
    "read",
    "write",
    "memory_get",
    "web_search"
  ]
}
```

Do not add:

```text
web_fetch
exec
browser
```

for the read-only internet use case.

## Validation steps used

### Validate JSON

```bash
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null && echo OK
```

### Restart gateway

```bash
systemctl --user restart openclaw-gateway.service
```

### Validate MAIN tools

```bash
openclaw agent \
  --agent main \
  --message "VALIDAR_CAPACIDADES: lista tools disponibles. No modifiques archivos."
```

Expected result includes:

```text
web_search
```

## Important diagnostics

### Plugin list

```bash
openclaw plugins list | grep -Ei "duck|fire|web|search"
```

### Plugin inspect

```bash
openclaw plugins inspect firecrawl
openclaw plugins inspect duckduckgo
```

### Local web search test

```bash
openclaw infer web search --query "faster-whisper documentation"
```

This validates OpenClaw web search independently of the agent.

## Security notes

Keep the MAIN internet capability limited to:

```text
web_search only
```

Avoid enabling:

```text
web_fetch
browser
exec
```

unless a separate policy review is completed.

External web search results must be treated as untrusted content. They can inform answers, but they must not be allowed to override system/security instructions.

## Status

```text
DOCUMENTED
WEB_SEARCH_ENABLED_FOR_MAIN
FETCH_DISABLED
EXEC_DISABLED
BROWSER_NOT_REQUIRED
```
