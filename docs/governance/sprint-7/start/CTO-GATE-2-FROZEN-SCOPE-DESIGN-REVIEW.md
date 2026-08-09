<!--
================================================================================
DEPOSIT METADATA — SPRINT 7 WU-0 START PACKAGE (CTO GATE 2 DEPOSIT)
Metadatos añadidos al depositar; el reporte original comienza tras el marcador.
Extraído programáticamente byte-verbatim del registro JSONL de la sesión CTO
(selección inequívoca: 1 candidato).
================================================================================
author: CTO (Chief Technology Officer, Project ARES — misma sesión de los
  depósitos CTO de docs/governance/sprint-7/ y docs/governance/phase-5/)
verdict: GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3
date_of_verdict: 2026-08-09
artifact_reviewed: alcance congelado Stage 1 (decisión L-1 de Luis) contra las
  fuentes canónicas en main = 8fc3de5434a19b4ae16fae8552c23b46ef370418 y el
  paquete r2 preservado (82bb6c52…11715d32); resuelve Q-CTO-1/3/4 y las
  obligaciones N-1 (confirmación formal) y N-2 (especificación NO MAPPING —
  FAIL CLOSED)
registry_location: docs/governance/sprint-7/start/ (per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL TEXT (verbatim, extracción programática de fuente primaria) -->

# CTO — SPRINT 7 GATE 2 · FROZEN-SCOPE DESIGN REVIEW

**Rol:** CTO (`technical_reviewer`) — revisión de diseño sobre el alcance congelado por tu decisión L-1 (Stage 1). Solo lectura: cero código, ramas, commits o PRs. Baseline verificado: `main = 8fc3de5434a19b4ae16fae8552c23b46ef370418` · `0.4.0` · framework byte-idéntico (`cac6ad75…711df9`) · research `BLOCKED` (0 archivos) · árbol limpio salvo H-8.

## 1. Completitud técnica del Stage 1 — CONFORME

D1→D2→D3→D4→D5→D6→D7→D8/D9→D10 forman un grafo acíclico completo: cada entregable consume solo predecesores; ninguno referencia componentes fuera del alcance; el plan WU-0…WU-9 con puntos de detención los cubre uno a uno; los criterios CA-1…CA-14 y la matriz T dan evidencia ejecutable a cada requisito. No falta ningún entregable para que Stage 1 sea internamente coherente, y no sobra ninguno.

## 2. Consistencia con la arquitectura aprobada — CONFORME (sin rediseño)

Diseño confirmado para implementación (resuelve las decisiones reservadas a este gate):

- **Q-CTO-3 (ubicación):** nuevo paquete **`ares/analysts/`** per arquitectura §C/§A/§D — sibling de `pipeline`, bajo `service`, sobre repositorios; imports solo descendentes; **nada** en `ares/models/` (dominio research intacto). Módulos: `lifecycle.py`, `authorities.py`, `transitions.py`, `roster.py`, `invariants.py`, `transition_log.py` (incluye el registro §5C). Tests en `tests/analysts/`.
- **Q-CTO-1 (cobertura de enums y forma del crosswalk):** **dos tipos distintos** — `RosterState` (roadmap §6: 10 lineales + 5 no lineales) y `ArchitectureState` (arquitectura §3: 9) — jamás un enum compartido; homónimos separados por tipo y con cita de procedencia por valor (T-1R verifica por documento, no por nombre). Crosswalk como **dato explícito** que codifica exclusivamente los cinco mapeos canónicos del roadmap §6.
- **Q-CTO-4 (PRs):** **PR único** con commits atómicos por WU (alcance pequeño; la revisión CRO se beneficia del diff completo), con opción de dividir solo si un gate lo exige.
- Precedentes obligatorios: `str, Enum` (patrón `enums.py`/ARES-015: "values frozen with the spec"), Pydantic v2 `frozen=True` + **`extra="forbid"` y validación estricta de enums** (cierra la ruta fail-open de coerción que dejé advertida), `SCHEMA_VERSION` propio (patrón `ifact.py`), JSON canónico, cero defaults en validadores, matriz como **whitelist** (nunca blacklist). El framework preservado no se toca (D9, T-14 en CI si se ejerce el MAY).

## 3. Separabilidad de Stage 1 — DEMOSTRADA

Ningún componente `EXCLUDED` es necesario: D1–D2 derivan solo de roadmap §6 + arquitectura §3 (§3.1 fuera; su único punto de contacto — `AssignmentRef` intake — ya está excluido y el análisis de separabilidad preservado no encontró dependencia inseparable); D3 no requiere loader ni IKP; D5 vive como modelos + fixtures **sin persistencia** (rige CR-4: GitHub sigue siendo el registro institucional; el código valida la disciplina, no la sustituye); D6 es un modelo tipado resoluble por id sin registry; D7 no necesita engine (los eventos de prueba se construyen directamente). La fila `RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS` exige "AssignmentRef emitido" **como evidencia declarada en la matriz** — representable como referencia opaca no resoluble en Stage 1 ⇒ esa transición **fallará cerrada por construcción** hasta que el intake exista (correcto: nadie puede avanzar a investigación en Stage 1 ni por accidente).

## 4. N-1 — CONFIRMACIÓN FORMAL DEL CTO (obligación G2)

**Confirmo: `candidate_status` es exclusivamente una proyección derivada del event log y nunca una segunda fuente de verdad.** Diseño: el estado vigente se computa del log (§5B.1); el campo `candidate_status` de `RosterSlot` existe solo para round-trip/serialización de los 15 slots canónicos y **se valida contra la derivación** (I-16; divergencia ⇒ manda el log + incidente, T-17); nunca se escribe de forma independiente. **No exige modificar el roadmap Active**: su §3 dice "Status changes follow the lifecycle in §6" — exactamente lo que la proyección implementa — y los cinco valores permitidos de §3 bastan para todo el roster actual (todos los slots son pre-gate-8, y en Stage 1 **ninguna** transición real puede ejecutarse: no hay research autorizado). Registro de disparador futuro: cuando algún slot avance más allá de los valores de §3 (imposible antes de un gate-8 tuyo), la lista de valores de §3 requerirá enmienda **§10 / L-2 en ese momento** — no ahora. **Sin STOP.** Pasa a ratificación CRO en Gate 3.

## 5. N-2 — ESPECIFICACIÓN FORMAL DEL CTO (obligación G2)

El crosswalk se implementa como mapeo total sobre `RosterState` cuyo codominio es `ArchitectureState | NO_MAPPING_FAIL_CLOSED`: **solo** los cinco mapeos canónicos (`PLANNED↔CANDIDATE`, `RESEARCH_AUTHORIZED↔AUTHORIZED`, `IKP_DRAFTED↔RESEARCHED→PACKAGED`, `VALIDATED↔CTO-IMPLEMENTATION-REVIEWED→CRO-VALIDATED→QUANT-VALIDATED`, `ACTIVE↔PRODUCTION`) portan valor; **todo lo demás** — incluidos `APPROVED`, `IMPLEMENTED`, `TBD`, `PROPOSED`, `RESEARCH_IN_PROGRESS` y los no lineales sin mapeo canónico (nota: ni siquiera `DEPRECATED↔DEPRECATED` se inventa por homonimia — sin cita canónica, `NO MAPPING`) — se representa explícitamente como **`NO MAPPING — FAIL CLOSED`**: consultarlo produce el sentinel/error explícito, jamás una correspondencia inventada ni un default. Verificación: T-1R (procedencia) + T-9 (round-trip del crosswalk con huecos preservados).

## 6. Tests y gates — CONFORMES

T-1R…T-23 cubren el alcance congelado con los cuatro controles críticos correctos: **T-20** (clausura exhaustiva del producto cartesiano contra la whitelist de 14 filas — cobertura incompleta = fallo del control), **T-21** (ablación por fila de cada elemento obligatorio, incl. §5C en `APPROVED→IMPLEMENTED`), **T-22/T-23** (preservación/identidad, ratificados por el CRO). Los 10 gates con cascada de invalidación corregida (G2→3–10) y doble autorización tuya (G4 inicio = L-3 pendiente; G10 cierre = L-8) permanecen como el marco de ejecución; ninguna WU precede G4.

## 7. L-2 — VERIFICACIÓN OBJETIVA: NO REQUERIDA

El encuadre "Stage 1 = primera etapa del mismo Sprint 7 cuyo objetivo final es Fase 6 completa" **no altera la secuencia canónica**: MASTER-ROADMAP §4 define Sprint 7 como la implementación del IKP Framework (Fase 6) — Stage 1 implementa parte de ella sin re-ordenar fases, sin redefinir el criterio de salida de Fase 6 ("Framework implemented and validated"), y sin que ningún milestone se declare satisfecho prematuramente (el DoD de Stage 1 no marca Fase 6 como done). Sin detección de alteración de secuencia ⇒ **sin STOP; enmienda no requerida.**

## 8. Sin activación / research / release — CONFIRMADO

Stage 1 no contiene ningún camino hacia: activación del framework (D9 + T-14 lo demuestran byte a byte; §3.1 excluido; L-4 intacta), research de candidato alguno (0 contenido; gate-8 imposible; la fila de intake falla cerrada por diseño — §3 supra), ni release (`v0.5.0` reservado a L-8/G10; versión permanece `0.4.0` durante todo Stage 1). La corrección de consistencia del MASTER-ROADMAP (MAY) queda acotada a §4/§6/README del roadmap, sin cambios sustantivos.

## Dictamen

# `GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3`

El diseño del alcance congelado es completo, consistente con la arquitectura aprobada (sin rediseño), separable, fail-closed de extremo a extremo, y con N-1 confirmada y N-2 especificada sin necesidad de enmienda del roadmap ni de L-2. Las decisiones de diseño reservadas a este gate (Q-CTO-1/3/4) quedan resueltas y registradas arriba como parte vinculante del diseño; los requisitos de implementación anti-fail-open (`extra="forbid"`, whitelist, sin defaults, referencia opaca no resoluble para el intake) son parte del diseño aprobado, no condiciones pendientes.

Este dictamen **no** resuelve L-3, **no** inicia Sprint 7 y **no** autoriza implementación. El siguiente relevo es el **Gate 3 — ratificación de riesgo del CRO** sobre este mismo alcance congelado y diseño (incluida la ratificación de N-1). Me detengo aquí y te devuelvo el control.

<!-- END ORIGINAL TEXT -->
