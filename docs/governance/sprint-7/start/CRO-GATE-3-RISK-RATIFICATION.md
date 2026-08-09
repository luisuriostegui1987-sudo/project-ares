<!--
================================================================================
DEPOSIT METADATA — SPRINT 7 WU-0 START PACKAGE (CRO GATE 3 DEPOSIT)
Añadido en el momento del depósito por el ejecutor de WU-0 mediante extracción
PROGRAMÁTICA byte-verbatim desde la fuente primaria (registro JSONL de la
sesión CRO original, selección inequívoca: 1 único candidato). NO forma parte
del texto original, que comienza tras el marcador "BEGIN ORIGINAL REPORT".
================================================================================
preserved_under: SPRINT 7 GATE 4 / WU-0 — START PACKAGE (autorización L-3 de
  Luis, 2026-08-09; control RG3-3)
author: CRO (Chief Risk Officer, Project ARES)
source_identity: registro JSONL original de la sesión CRO (la misma sesión de
  los depósitos CRO-1…CRO-4 de docs/governance/sprint-7/ y del depósito CRO de
  docs/governance/phase-5/); extracción programática, sin transcripción manual
verdict: GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS REMAIN
controls_issued: RG3-1, RG3-2, RG3-3, RG3-4, RG3-5 (vinculantes por gate)
artifact_reviewed: alcance congelado Stage 1 (decisión L-1 de Luis) + diseño
  CTO Gate 2 (GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3), contrastados
  contra las fuentes canónicas en main = 8fc3de5434a19b4ae16fae8552c23b46ef370418
  y el paquete r2 preservado (82bb6c525dd8d8b2aca74595ef0558149db0b4535649b78727ec161a11715d32)
registry_location: docs/governance/sprint-7/start/ (registro institucional
  per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL REPORT (verbatim, fuente primaria JSONL sesión CRO) -->

Baseline y estado verificados; el diseño Gate 2 y la decisión L-1 no están aún preservados como artefactos (los contrasto contra las fuentes canónicas y el paquete r2 preservado, cuya identidad conozco por hash). Emito el reporte Gate 3.

---

# CRO — SPRINT 7 GATE 3 · FROZEN-SCOPE RISK & METHODOLOGY RATIFICATION

**Rol e independencia:** revisión de solo lectura; el `GATE 2 PASS` del CTO fue evidencia de entrada, no conclusión adoptada — cada determinación de abajo se contrastó contra el roadmap Active, la arquitectura v1.4, el contrato preservado, research-governance y el paquete r2 (`82bb6c52…`, cuyos controles §5A/§5B/§5C y T-1R…T-23 ya audité y ratifiqué pieza por pieza en este ciclo).

## A. Baseline

`HEAD/main` = **`8fc3de5434a19b4ae16fae8552c23b46ef370418`** ✅ (PR #12 = cierre de Fase 5). **Fase 5 = done** ✅ (fila 5: aprobación explícita de Luis 2026-08-08, reviews preservadas en `docs/governance/phase-5/`, con la salvaguarda «Approval authorizes no research, no Sprint 7 start and no framework activation»; header del roadmap ahora `Active` con el registro de aprobación) · **Fase 6 = pending** ✅ · Sprint 7 `not started` ✅ · `0.4.0` ✅ · `v0.5.0` inexistente ✅ · framework inactivo, hash intacto ✅ · research bloqueado, `docs/analysts/` = 0 archivos ✅ · L-3 `OPEN` — no existe autorización de implementación ✅. **El alcance congelado coincide exactamente** con lo propuesto/excluido en r2 §3.2/§4.2 que Luis aprobó vía L-1: D1–D10 dentro; §3.1, loader, validator, AssignmentRef intake, engine, registry, service/API, persistencia, Quant harness, primitive vocabulary, research, IKPs, activación, v0.5.0, señales, operaciones y capital fuera.

## B. N-1 — Ratificación

**`N-1 RATIFIED`.** Confirmado punto por punto contra §5B (ratificado) y el diseño Gate 2: el event log es la única fuente de verdad (§5B.1); `candidate_status` es proyección **derivada, no mutable independientemente** (no existe vía de escritura propia — I-16); divergencia proyección↔log ⇒ manda el log + incidente registrado con severidad ALTA y congelamiento del slot (T-17/T-19, mi resolución Q-CRO-3); ningún estado materializado sustituye historial (§5B.8); y no se introduce segunda autoridad (un solo lifecycle; I-14). Es la misma resolución que ratifiqué en I-13/§5B.12 y en la revisión final de Fase 5 — ahora con encoding confirmado.

## C. N-2 — Crosswalk

**CONFORME.** `NO_MAPPING_FAIL_CLOSED` es la materialización correcta de mi exigencia de era-arquitectura («el hueco se representa como hueco, jamás se inventa»): sin mapping por similitud nominal (disciplina de homónimos-por-procedencia de T-1R, r2 §3.3.3); los huecos (`APPROVED`, `IMPLEMENTED`, y correctamente extendido a `TBD`, `PROPOSED`, `RESEARCH_IN_PROGRESS`, que el crosswalk canónico del roadmap §6 tampoco mapea) permanecen huecos con **sentinel explícito**, no default; `extra="forbid"` + enums estrictos impiden que un default cree correspondencia; T-1R (cita literal por valor — un mapeo inventado no puede citar fuente) y T-9 (round-trip canónico) detectan violaciones.

## D. Transition matrix (D2)

**CONFORME.** Whitelist estricta = exactamente las 14 filas canónicas; todo otro par rechazado; sin transiciones implícitas, ordinales (la cadena de flechas del §6 no es fuente — solo la tabla) ni inferidas por LLM (prohibición canónica #4). **T-20 y T-21 son suficientes** — ya verifiqué sus ocho y diez elementos respectivamente en r2. **Precisión exigible en gates internos (RG3-1):** las filas cuantificadas («any → DEFERRED/REJECTED/SUSPENDED/SUPERSEDED») deben expandirse a pares concretos de forma **explícita, determinista y finita** antes de computar la clausura T-20; una regla sin expandir = ninguna transición (fail-closed). Verificación en G6/G7 con la evidencia de T-20.

## E. Event log (D5)

**CONFORME.** Los diez atributos exigidos están cubiertos por las 12 reglas de §5B ya ratificadas (append-only absoluto, orden total determinista, idempotencia por identidad de contenido, duplicados sin segundo efecto, out-of-order rechazado sin reordenamiento silencioso, revocación como evento nuevo, reconciliación donde **el log manda** + incidente, reproducibilidad bit a bit). **La ausencia de persistencia DB en Stage 1 no crea pretensión de producción** siempre que se cumpla mi CR-4 vigente: D8 debe declarar que **GitHub sigue siendo el registro institucional** y que el log en memoria es el validador de la disciplina, no el sistema de registro — verificable en G9 (registrado como RG3-5, DEFERRED).

## F. Authority model (D4/D6)

**CONFORME.** Todas las separaciones exigidas están codificadas en §5A/§5C ya ratificados: autor ≠ único verificador (I-3/I-14, «el único autor jamás puede ser el único verificador»); implementer ≠ approver; CTO ≠ CRO ≠ Quant, cada gate propio; PASS técnico ≠ activación (§10.2.4-5); activación ≠ capital (I-8; `capital_authority` = solo Luis, «ningún estado técnico la concede»); confianza AI ≠ aprobación institucional (I-7); excepciones solo con autorización explícita y registrada de Luis (L-6); autoridad revocada/no verificable ⇒ rechazo (I-14, T-15, R-13).

## G. AssignmentRef boundary

**CONFORME — con un control interno explícito.** La referencia opaca **no resoluble** en Stage 1, combinada con la integridad referencial de §5B.3 (referencia irresoluble ⇒ evento inválido ⇒ rechazo), hace que `RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS` sea **estructuralmente imposible en Stage 1**: sin intake no hay transición, por construcción y no por disciplina. No se introduce mock con potencial de autoridad *siempre que* ningún constructor de producción pueda fabricar una referencia resoluble en Stage 1. **Exijo (RG3-2)** una prueba explícita — propongo **T-24, «Stage 1 research-start impossibility»** — que demuestre: (a) ningún input construible por vías de producción satisface la fila 4; (b) todo intento rechaza fail-closed; (c) los dobles de prueba usados para T-2/T-21 en esa fila son no-construibles fuera del ámbito de tests y así consta en el dossier. Es la única prueba adicional imprescindible que identifico — protege exactamente la frontera que L-1 congeló.

## H. Fail-open / input controls

**SUFICIENTES.** `frozen=True` + `extra="forbid"` + enums estrictos (sin coerción de tipo) + prohibición de defaults en validadores + JSON canónico (precedente `ifact.py`) + whitelist-only, respaldados por T-8 (valor desconocido ⇒ error, jamás coerción), T-9 (round-trip bit a bit con schema versionado, I-17) y T-13 (fuzzing como defensa adicional). Esto neutraliza las cuatro rutas fail-open que el ciclo identificó (coerción silenciosa, defaults, blacklist-en-vez-de-whitelist, relleno de huecos del crosswalk).

## I. Test suite (T-1R…T-23)

Las diez pruebas señaladas ya fueron auditadas individualmente y ratificadas en r2 (T-20/T-21 con todos sus elementos; T-22/T-23 ratificadas sin condición; T-1R con chequeo estático de §3.1; T-14 con hash completo per T-23). **Única adición imprescindible antes del start: T-24** (sección G) — riesgo material no cubierto: la suite actual prueba transiciones prohibidas (T-3) y ablación de filas válidas (T-21), pero no demuestra la **imposibilidad de construcción en producción** de la evidencia de la fila 4 en Stage 1. Ninguna otra prueba se añade — el resto sería perfeccionismo.

## J. L-2

**`L-2 NOT REQUIRED — RATIFIED`.** Fundamento independiente: MASTER-ROADMAP §10 exige enmienda para desviaciones **de secuencia**; Stage 1 es una etapa interna de la Fase 6 dentro del mismo Sprint 7 — ninguna fase se salta, reordena ni redefine; el criterio de salida de la Fase 6 («Framework implemented and validated») permanece intacto y **Stage 1 no lo satisface** (r2 §3.1, consecuencia 1, preservado). El propio plan canónico §K prescribe ejecución por pasos dentro del Sprint. **Salvaguarda de la ratificación:** esta determinación es válida solo mientras (a) la Fase 6 no se declare completa antes del framework íntegro, y (b) todo Stage posterior permanezca dentro de la Fase 6; presentar Stage 1 como cumplimiento del gate 7 sí exigiría corrección.

## K. MASTER-ROADMAP consistency

**Incluirla en el futuro PR de autorización/Stage 1: SÍ.** Verificado en HEAD: §4 («Current priority: Resolve Phase 5…») quedó obsoleto tras el PR #12; el blockquote de §6 conserva «Draft… Phase 5 remains pending»; el README del roadmap conserva el estado previo. La corrección mínima **mejora la gobernanza** (elimina dos verdades sobre el estado de Fase 5), **no altera alcance**, y **no es enmienda §10** — es reconciliación de estado registrado, clase idéntica al precedente del PR #8. Expectativa CRO: con bump de versión por documento tocado (doctrina de versionado establecida en el ciclo del PR #10).

## L. Risk register (solo residuales materiales)

| ID | Clase | Riesgo | Control | Gate | Responsable | Condición fail-closed |
|---|---|---|---|---|---|---|
| RG3-1 | INTERNAL-GATE | Expansión de filas «any→X» implícita o incompleta | Expansión explícita, determinista y finita como insumo de T-20 | G6/G7 | implementer + CTO | Regla sin expandir = ninguna transición permitida |
| RG3-2 | INTERNAL-GATE | Stage 1 pudiera iniciar research vía evidencia fabricada de fila 4 | **T-24** en la matriz de pruebas del paquete de start; dobles de prueba no-construibles en producción | Antes de G6; verificación CRO en G8 | implementer + CRO | Referencia irresoluble ⇒ rechazo (§5B.3) |
| RG3-3 | NON-BLOCKING | El registro Gate 2, la decisión L-1 y este Gate 3 no están preservados como artefactos (disciplina T-22) | Depósito en el PR de autorización/start (formato DF-1/Fase 5) | Paquete L-3 | Autores + Publishing + Luis (merge) | Per T-22: dictamen no preservado no habilita gates una vez implementado |
| RG3-4 | NON-BLOCKING | Doble verdad documental sobre el estado de Fase 5 | Reconciliación mínima §4/§6/README con bumps de versión, en el mismo PR | Paquete L-3 | CKO/Publishing + revisiones + Luis | — |
| RG3-5 | DEFERRED | Log en memoria confundido con sistema de registro | CR-4 vigente: D8 declara GitHub como registro institucional | G9 | implementer + Publishing; CRO verifica | Evento solo-en-memoria no es canon |

**Ninguno BLOCKING.**

## M. START readiness

Desde metodología y riesgo: **sí — tras este Gate 3, L-3 puede presentarse a Luis**, siempre que el paquete de start incorpore RG3-2 (T-24 en la matriz), RG3-3 (preservación de Gate 2, L-1 y este reporte) y RG3-4 (reconciliación del roadmap). **No autorizo L-3** — esa decisión es exclusivamente de Luis, junto con las que permanecen abiertas (L-4 §3.1, gate-8 por candidato, naming TBD, L-7, L-9, L-10).

## Dictamen

# `GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS REMAIN`

N-1 **RATIFIED** · N-2 **conforme** · L-2 **NOT REQUIRED — RATIFIED** · matriz, event log, modelo de autoridad, frontera AssignmentRef y controles anti-fail-open **conformes** · una sola prueba adicional exigida (T-24) y tres ítems no bloqueantes anclados al paquete L-3 y a gates internos. Nada impide presentar la decisión de start a Luis. Este dictamen **no** resuelve L-3, **no** inicia Sprint 7, **no** implementa, **no** activa el framework y **no** autoriza research ni capital.

No modifiqué archivos; sin branch/commit/PR; baseline final idéntico al de la sección A.

Me detengo aquí y te devuelvo el control, Luis.

<!-- END ORIGINAL REPORT -->
