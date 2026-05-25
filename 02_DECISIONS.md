# 🧠 OpenClaw – Decisiones clave

## 1. Uso de interaction_id

Decisión:
Todo evento funcional debe estar asociado a un interaction_id.

Implementación:
- Se crea scripts/ru_interaction.sh
- Genera interaction_id automáticamente
- Llama a ru_event.sh

Motivo:
Permitir trazabilidad real del consumo por interacción.

---

## 2. Wrapper obligatorio

Decisión:
Usar ru_interaction.sh como interfaz principal.

Evitar uso directo de:
scripts/ru_event.sh

Excepciones:
- logs técnicos internos
- health checks

Motivo:
Reducir eventos sin interacción.

---

## 3. Métrica principal de calidad

Decisión:
Medir calidad del sistema con:

events_without_interaction_id_count / actions_count

Regla:
- >30% → requiere atención
- ≤30% → aceptable

Motivo:
Indica si el sistema es analizable o no.

---

## 4. Tokens estimados (no reales)

Decisión:
Los tokens se estiman como:

input_chars / 4
output_chars / 4

Motivo:
No hay acceso a métricas reales del modelo.

Importante:
No usar para facturación.

---

## 5. Dashboard sin librerías externas

Decisión:
No usar:
- Chart.js
- librerías externas
- canvas

Solo:
- HTML
- CSS
- JS simple

Motivo:
Simplicidad, control y estabilidad.

---

## 6. Nueva vista independiente

Decisión:
Crear:
dashboard-v2/tools/token-overview.html

No sobrecargar:
resource-usage.html

Motivo:
Separación de responsabilidades.

---

## 7. Logs como fuente de verdad

Decisión:
Fuente única:

logs/resource_usage.jsonl

Motivo:
Evitar duplicidad y inconsistencias.

---

## 8. No automatizar de más

Decisión:
No crear nuevos timers ni servicios.

Motivo:
Control manual y evitar complejidad innecesaria.

---

## 9. Prioridad actual

Decisión:
No desarrollar más infraestructura.

Enfocar en:
- calidad de datos
- uso correcto del sistema

Motivo:
El sistema ya es suficiente.

---

## 🧠 Conclusión

El sistema está técnicamente completo.

El valor depende del uso correcto de interaction_id.
