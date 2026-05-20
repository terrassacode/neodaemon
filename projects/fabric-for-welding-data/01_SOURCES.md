# 01_SOURCES

## Objetivo
Registrar fuentes relevantes para Microsoft Fabric aplicadas a soldadura.

## Formato
- nombre:
- tipo: doc / blog / pdf / video / repo
- url:
- prioridad: alta / media / baja
- estado: pendiente / analizado / curado / descartado
- fecha:
- notas:

---

## S-001 — Microsoft Real-Time Intelligence Operations Solution Accelerator

- nombre: Real-Time Intelligence for Operations Solution Accelerator
- tipo: repo oficial
- url: https://github.com/microsoft/real-time-intelligence-operations-solution-accelerator
- prioridad: alta
- estado: curado
- fecha: 2026-05-20
- calidad: alta

### Motivo de entrada
Fuente oficial de Microsoft con arquitectura y solución funcional para Real-Time Intelligence aplicada a operaciones de fabricación.

### Qué aporta
- Arquitectura de referencia para operaciones en tiempo real.
- Dashboard de operaciones en tiempo real.
- Detección de anomalías y notificaciones.
- Uso de EventHouse, KQL, dashboard y Activator.
- Ejemplo extensible a manufactura e IoT industrial.

### Aplicación al sistema de soldadura
Se puede usar como referencia para diseñar el modelo HOT:

```text
soldadura individual -> evento -> Eventstream -> Eventhouse -> KQL -> alerta / dashboard
```

Aplicación concreta:
- entrada: eventos de soldadura por punto;
- señales: RD, corriente, esfuerzo, tiempos, robot, programa;
- lógica: variabilidad e inestabilidad del proceso;
- salida: alertas y dashboard operativo.

### Decisión técnica
Entra al RAG como fuente de arquitectura HOT.

No entra como fuente de lógica de soldadura; la lógica de variabilidad RD debe definirse internamente con conocimiento de proceso.

### Riesgos / límites
- Es una solución genérica de operaciones, no específica de soldadura.
- Usa datos sintéticos en el ejemplo.
- No debe copiarse tal cual; debe adaptarse al proceso real.

### Clasificación RAG
- arquitectura: sí
- KQL patterns: parcial
- lógica soldadura: no
- aplicabilidad industrial: alta
