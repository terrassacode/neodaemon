# Python Code Self Check Rule

## Propósito

Definir `SELF_CHECK_PYTHON` como regla obligatoria para que Neodaemon revise código Python antes de proponerlo o crearlo.

El objetivo es reducir errores evitables de sintaxis, indentación, imports, llamadas peligrosas y afirmaciones no verificadas sobre compilación o tests.

## Cuándo aplica

`SELF_CHECK_PYTHON` aplica antes de:

- proponer código Python;
- crear archivos `.py`;
- modificar archivos `.py`;
- proponer tests Python;
- crear tests Python;
- modificar tests Python;
- diseñar o cambiar runner/tests Python dentro de `automation/`.

Aplica especialmente a:

```text
projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py
projects/openclaw-knowledge-wiki/automation/tests/
```

## Checklist obligatoria

Antes de entregar código Python, Neodaemon debe revisar:

1. Sintaxis visual:
   - cada `def` tiene cuerpo indentado;
   - cada `class` tiene cuerpo indentado;
   - cada `if`, `for`, `while`, `with`, `try` tiene cuerpo indentado;
   - no hay líneas sueltas pegadas a margen incorrecto.

2. Imports:
   - imports necesarios presentes;
   - imports no usados revisados;
   - no se añaden imports peligrosos sin justificación.

3. Errores obvios:
   - no usar `isTrue`;
   - no usar `true`/`false` estilo JSON en código Python;
   - no dejar comillas sin cerrar;
   - no dejar paréntesis o bloques abiertos;
   - no dejar bloques mal indentados.

4. Llamadas peligrosas:
   - revisar `subprocess`;
   - revisar `os.system`;
   - revisar ejecución de comandos shell;
   - revisar llamadas a Git/GitHub;
   - revisar escritura fuera del proyecto;
   - revisar creación de estado runtime no autorizado.

## Formato obligatorio de salida

Cada vez que aplique, Neodaemon debe incluir:

```text
SELF_CHECK_PYTHON:
- syntax_visual: OK/ERROR
- indentation_blocks: OK/ERROR
- imports: OK/ERROR
- dangerous_calls: OK/ERROR
- py_compile: OK/NOT_RUN/ERROR
- tests: OK/NOT_RUN/ERROR
- result: PASS/BLOCK
```

## Si hay shell disponible

Cuando haya shell disponible y esté autorizado:

1. ejecutar:
   ```bash
   python3 -m py_compile <archivo>
   ```

2. si son tests, ejecutar:
   ```bash
   python3 <test_file>
   ```

3. reportar resultados reales.

No se debe afirmar éxito si la ejecución no se realizó.

## Si no hay shell disponible

Si no hay shell disponible:

- marcar `py_compile: NOT_RUN`;
- marcar `tests: NOT_RUN`;
- hacer revisión manual estructurada;
- no afirmar que compila;
- no afirmar que los tests pasan.

## Si falla la validación

Si falla cualquier punto:

1. devolver `ERROR`;
2. corregir el código;
3. volver a validar;
4. solo responder con propuesta final si el resultado es `PASS`.

Si no se puede corregir con seguridad:

```text
result: BLOCK
```

## Prohibición explícita

Neodaemon no debe afirmar:

```text
py_compile OK
tests OK
compila
tests pasan
```

si no ejecutó realmente `py_compile` o los tests correspondientes.

## Aplicación a automation

Para `github_pr_workflow_runner.py` y tests relacionados:

- mantener v0.1 read-only salvo autorización explícita;
- no introducir `subprocess` ni `os.system` sin autorización específica;
- no ejecutar Git desde tests;
- no crear `run_state`;
- no crear `approvals`;
- no tocar repo limpio;
- no crear ramas;
- no hacer copy, commit, push, PR ni merge.

## Límites

Esta regla no autoriza:

- ejecutar Git;
- instalar dependencias;
- tocar gateway, auth, tokens, systemd, `.env` ni logs crudos;
- tocar `raw/`;
- tocar `~/.openclaw/skills`;
- escribir fuera del proyecto;
- saltarse TASK_VALIDATOR o autorización explícita de Albert.

## Estado

Regla obligatoria para futuras propuestas y cambios Python.
