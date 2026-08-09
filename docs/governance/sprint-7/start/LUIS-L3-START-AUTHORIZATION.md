<!--
================================================================================
DEPOSIT METADATA — SPRINT 7 WU-0 START PACKAGE (LUIS L-3 START AUTHORIZATION)
Metadatos añadidos al depositar; el texto decisorio original de Luis comienza
tras el marcador. Extraído programáticamente byte-verbatim del registro JSONL
de la sesión CTO (mensaje de Luis, selección inequívoca: 1 candidato).
================================================================================
authority: Luis (approver — decisión reservada L-3 / Gate 4)
decision: L-3 APPROVED — START SPRINT 7 / STAGE 1 UNDER FROZEN SCOPE
  (autoriza primero la materialización del Start Package / WU-0; la
  implementación funcional WU-1…WU-9 comienza solo tras el merge autorizado
  de WU-0)
basis: GATE 2 PASS (CTO) + GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS
  REMAIN (CRO; controles RG3-1…RG3-5 vinculantes)
date: 2026-08-09
baseline_at_decision: main = 8fc3de5434a19b4ae16fae8552c23b46ef370418
registry_location: docs/governance/sprint-7/start/ (per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL TEXT (verbatim, extracción programática de fuente primaria) -->

CTO — SPRINT 7 GATE 4 · LUIS L-3 START AUTHORIZATION & INSTITUTIONAL MATERIALIZATION
DECISIÓN EXPRESA DE LUIS
Luis resuelve L-3:
`L-3 APPROVED — START SPRINT 7 / STAGE 1 UNDER FROZEN SCOPE`
Esta autorización se basa en:
`GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3`
y:
`GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS REMAIN`
El Conditional Pass del CRO NO contiene blockers.
Los controles RG3-1…RG3-5 permanecen vinculantes según su gate.
IMPORTANTE — SIGNIFICADO DE L-3
Luis autoriza institucionalmente el INICIO de Sprint 7 bajo el alcance Stage 1 congelado.
Esta orden autoriza PRIMERO la MATERIALIZACIÓN DEL START PACKAGE.
NO autoriza todavía ejecutar WU-1…WU-9 ni escribir implementación funcional antes de que el Start Package sea revisado y merged.
WU-0 = Start Package / institutional materialization.
La implementación funcional comienza únicamente después del merge autorizado de WU-0.
BASELINE ESPERADO
`main = 8fc3de5434a19b4ae16fae8552c23b46ef370418`
Verifica antes de escribir:

* Phase 5 = done
* Phase 6 = pending
* Sprint 7 = not started
* canonical version = 0.4.0
* framework inactive
* research BLOCKED
* docs/analysts/ = 0 research content
* v0.5.0 nonexistent

Si existe drift material:
STOP.
Reporta:
`SPRINT 7 GATE 4 BLOCKED — START BASELINE DRIFT`
────────────────────

1. PRESERVATION
────────────────────

Preserva institucionalmente:
A. decisión L-1 de Luis;
B. CTO Gate 2:
`GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3`
C. CRO Gate 3:
`GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS REMAIN`
D. decisión L-3 de Luis contenida en esta orden.
Usa:
`docs/governance/sprint-7/start/`
Crea depósitos separados e índice README.
DISCIPLINA DE PRESERVACIÓN
Para reportes CTO/CRO:

* fuente primaria de sesión;
* extracción programática cuando sea posible;
* texto byte-verbatim;
* DEPOSIT METADATA separado;
* BEGIN/END ORIGINAL REPORT;
* SHA-256 completo.

Para decisiones de Luis:
preserva literalmente el texto decisorio correspondiente, sin reinterpretarlo.
No reconstruyas reportes manualmente.
Si una fuente primaria necesaria no puede recuperarse inequívocamente:
STOP.
`SPRINT 7 GATE 4 BLOCKED — PRESERVATION FAILURE`
────────────────────
2. T-24 — OBLIGATORIO
────────────────────
Incorpora formalmente al Start Package:
`T-24 — Stage 1 Research-Start Impossibility`
Objetivo:
demostrar que Stage 1 no puede iniciar research por construcción.
Debe verificar como mínimo:
A. ningún input construible mediante vías de producción de Stage 1 puede satisfacer:
`RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS`
B. ausencia de AssignmentRef intake/resolver ⇒ referencia no resoluble;
C. referencia no resoluble ⇒ transición rechazada fail-closed;
D. ningún mock/fixture de tests puede convertirse accidentalmente en autoridad de producción;
E. cualquier doble necesario para probar la fila de transición debe quedar confinado a tests;
F. el dossier debe demostrar esta separación.
T-24 pasa a formar parte vinculante de D7.
No implementes todavía el test.
Solo materializa su especificación contractual dentro del Start Package.
────────────────────
3. RG3 CONTROLS
────────────────────
Registra como controles vinculantes:
RG3-1 — INTERNAL GATE
Las filas:
`any → DEFERRED`
`any → REJECTED`
`any → SUSPENDED`
`any → SUPERSEDED`
deben expandirse explícita, determinista y finitamente antes de T-20.
Regla no expandida:
`NO TRANSITION PERMITTED`
Verificación G6/G7.
RG3-2 — INTERNAL GATE
T-24 obligatorio antes de G6.
CRO verifica en G8.
RG3-3 — CERRAR EN WU-0
Preservar L-1, Gate 2, Gate 3 y L-3.
RG3-4 — CERRAR EN WU-0
Reconciliación documental mínima post-Phase-5.
RG3-5 — DEFERRED / G9
D8 debe declarar:
`GitHub remains the institutional system of record.`
El event log de Stage 1 valida la disciplina pero NO sustituye el registro institucional.
────────────────────
4. MASTER-ROADMAP CONSISTENCY
────────────────────
Corrige únicamente el drift documental ya identificado.
MASTER-ROADMAP §4:
elimina la prioridad obsoleta:
`Resolve Phase 5`
y refleja que Phase 5 está cerrada y que Sprint 7 Stage 1 es la prioridad autorizada.
MASTER-ROADMAP §6:
elimina referencias obsoletas que describen Analyst Roadmap como Draft / Phase 5 pending.
Roadmap README:
actualiza el estado coherentemente.
NO alteres:

* secuencia de fases;
* criterio de salida de Phase 6;
* arquitectura;
* scope de Phase 6;
* gates posteriores.

Esto es reconciliación documental, NO amendment §10.
Aplica version bump documental únicamente si la política canónica vigente lo exige; reporta exactamente qué versión cambia y por qué.
────────────────────
5. SPRINT 7 STATUS
────────────────────
Materializa:
`Sprint 7: not started → started`
o el vocabulario canónico exacto equivalente ya definido en el repositorio.
NO marques:
Phase 6 = done.
Phase 6 debe permanecer:
`pending`
hasta completar y validar el framework íntegro.
Si el vocabulario canónico no admite `started`:
NO inventes un estado.
Usa el estado canónico aplicable y explica la representación.
────────────────────
6. FROZEN SCOPE
────────────────────
Registra el Stage 1 Frozen Scope exactamente como autorizado.
MUST IMPLEMENT:
D1 lifecycle enums
D2 transition matrix
D3 roster schema
D4 invariants + authority vocabulary
D5 append-only event log
D6 independent-verification record
D7 T-1R…T-24
D8 implementation documentation
D9 framework compatibility attestation
D10 institutional dossier
EXCLUDED:
Workflow Status §3.1
IKP validator
loader
AssignmentRef intake
deterministic engine
registry/discovery
service/API
DB persistence/migration
Quant harness
primitive vocabulary
analyst research
real IKPs
framework activation
v0.5.0
signals
operations
capital
DEFERRED:
todo componente restante de Phase 6 a etapas posteriores del mismo Sprint 7, sujeto a nuevas autorizaciones expresas de Luis.
────────────────────
7. NON-AUTHORIZATIONS
────────────────────
El Start Package debe declarar explícitamente:
L-3 DOES NOT AUTHORIZE:

* analyst research;
* Benjamin Cowen research;
* gate-8 for any candidate;
* IKP population;
* Workflow Status §3.1;
* framework activation;
* Phase 6 completion;
* v0.5.0;
* signals;
* operations;
* capital.

────────────────────
8. BRANCH / COMMIT / PR
────────────────────
Después de completar y verificar WU-0:
crea una rama inequívoca, preferida:
`governance/sprint-7-stage-1-start`
Stage exclusivamente archivos WU-0 autorizados.
Verifica diff completo.
Un solo commit de materialización:
`governance: authorize Sprint 7 Stage 1 start`
Sin amend.
Push normal.
No force.
Abre DRAFT PR hacia main.
Título:
`Sprint 7: Authorize Stage 1 start under frozen scope`
────────────────────
9. PR BODY
────────────────────
Debe contener:
Purpose
Materialize Luis's L-1 frozen-scope decision and L-3 authorization to start Sprint 7 Stage 1.
Evidence

* L-1 decision
* CTO Gate 2
* CRO Gate 3
* L-3 authorization
* hashes of preserved records

Authorized Stage 1
D1–D10
T-1R…T-24
Risk controls
RG3-1…RG3-5
State transition
Sprint 7:
`not started → started`
o vocabulario canónico equivalente.
Phase 6 remains pending.
Explicit exclusions
lista completa de EXCLUDED.
Non-authorizations
Research remains blocked.
Framework remains inactive.
No gate-8.
No real IKP.
No v0.5.0.
No signals.
No operations.
No capital.
────────────────────
10. POST-COMMIT / PR VERIFICATION
────────────────────
Confirma:

* main NO cambió;
* Draft PR open;
* exact files;
* hashes de depósitos;
* frozen scope intacto;
* T-24 incluido;
* RG3 controls incluidos;
* Phase 5 = done;
* Phase 6 = pending;
* Sprint 7 status únicamente cambia en la rama;
* framework inactive;
* research blocked;
* version correcta;
* v0.5.0 nonexistent;
* docs/analysts/ sin research content;
* ningún archivo funcional de implementación creado.

────────────────────
11. STOP
────────────────────
NO MERGE.
NO WU-1.
NO implementación funcional.
Entrega:
CTO — SPRINT 7 GATE 4 / WU-0 · START MATERIALIZATION REPORT
Incluye:

* baseline;
* preservation sources;
* paths;
* SHA-256;
* documentary reconciliation;
* exact state transition;
* frozen scope;
* T-24;
* RG3 controls;
* branch;
* commit SHA;
* exact files;
* Draft PR number/URL;
* main unchanged;
* barriers;
* confirmation that WU-1 has NOT started.

DICTAMEN:
`SPRINT 7 WU-0 PASS — START AUTHORIZATION PR READY FOR FINAL REVIEW`
o
`SPRINT 7 GATE 4 BLOCKED — START MATERIALIZATION ISSUE`
Después detente y devuelve el control a Luis.

<!-- END ORIGINAL TEXT -->
