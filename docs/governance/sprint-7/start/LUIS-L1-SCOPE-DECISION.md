<!--
================================================================================
DEPOSIT METADATA — SPRINT 7 WU-0 START PACKAGE (LUIS L-1 DECISION)
Metadatos añadidos al depositar; el texto decisorio original de Luis comienza
tras el marcador. Extraído programáticamente byte-verbatim del registro JSONL
de la sesión CTO (mensaje de Luis, selección inequívoca: 1 candidato).
================================================================================
authority: Luis (approver — decisión reservada L-1)
decision: L-1 APPROVED — SPRINT 7 STAGED IMPLEMENTATION / STAGE 1 MINIMUM
  AUTHORIZED SCOPE (L-2 amendment NOT REQUIRED for this scope; L-4 §3.1
  remains EXCLUDED — NOT AUTHORIZED; L-5 already resolved via PR #12)
date: 2026-08-09 (recibida en la sesión CTO tras el Gate 0 Decision Brief)
baseline_at_decision: main = 8fc3de5434a19b4ae16fae8552c23b46ef370418
registry_location: docs/governance/sprint-7/start/ (per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL TEXT (verbatim, extracción programática de fuente primaria) -->

CTO — SPRINT 7 GATE 1 · LUIS L-1 SCOPE DECISION
DECISIÓN EXPRESA DE LUIS
Luis resuelve L-1 de la siguiente manera:
`L-1 APPROVED — SPRINT 7 STAGED IMPLEMENTATION / STAGE 1 MINIMUM AUTHORIZED SCOPE`
Sprint 7 seguirá siendo el sprint canónico de Phase 6.
Esta decisión NO divide ni reordena las fases del MASTER-ROADMAP.
Stage 1 es únicamente la primera etapa controlada de implementación dentro del mismo Sprint 7, cuyo objetivo final sigue siendo completar:
`Phase 6 — Plug-in Analyst Framework`
Por lo tanto:
`L-2 ROADMAP AMENDMENT = NOT REQUIRED FOR THIS SCOPE`
SALVO que CTO/CRO detecten objetivamente que este encuadre altera la secuencia canónica, en cuyo caso deben detenerse y devolver la cuestión a Luis.
SCOPE FROZEN — STAGE 1
MUST IMPLEMENT
D1 — lifecycle enums:

* fuentes exclusivamente roadmap §6 + arquitectura §3;
* Workflow Status §3.1 EXCLUDED;
* homónimos separados por procedencia/tipo.

D2 — transition matrix:

* 14 transiciones canónicas;
* whitelist estricta;
* todo par no autorizado = fail closed.

D3 — roster schema:

* 12 campos canónicos;
* `candidate_status` tratado como proyección derivada del event log conforme §5B.12;
* no segunda fuente de verdad.

D4 — invariantes I-1…I-17 + vocabulario de autoridades:

* roles;
* incompatibilidades;
* separación de funciones;
* identidad/autoridad verificable.

D5 — append-only event log:

* fuente de verdad institucional del estado;
* orden determinista;
* integridad referencial;
* idempotencia;
* duplicados;
* fuera-de-orden;
* revocaciones como eventos;
* reconciliación fail-closed;
* sin persistencia DB en esta etapa.

D6 — independent-verification record:

* conforme §5C;
* evidencia y autoridad separadas;
* verificación no equivale a transición.

D7 — test suite T-1R…T-23:

* incluyendo T-20 exhaustive ordered-pair closure;
* T-21 transition-row ablation;
* T-22/T-23 preservation/identity controls según diseño.

D8 — documentación mínima necesaria de implementación.
D9 — framework compatibility attestation:

* preservar identidad del framework aprobado;
* no rediseñar arquitectura.

D10 — institutional dossier/evidence package para gates posteriores.
MAY IMPLEMENT

* CI check para T-14 / hash del framework;
* fixtures/helpers internos estrictamente necesarios en `tests/analysts/`;
* corrección mínima de consistencia documental post-Phase-5 en:
   * MASTER-ROADMAP §4;
   * MASTER-ROADMAP §6;
   * roadmap README;
si se materializa junto al futuro PR de autorización/implementación.

EXCLUDED — NO AUTORIZADO EN STAGE 1

* Workflow Status §3.1;
* `InstitutionalKnowledgePackageValidator`;
* loader;
* AssignmentRef intake;
* deterministic engine;
* AnalystRegistry/discovery;
* AnalystService/API;
* assessment persistence;
* DB migration 0003;
* Quant harness;
* primitive vocabulary v1;
* research de cualquier analista;
* contenido IKP real;
* Benjamin Cowen research;
* cualquier gate-8 authorization;
* framework activation;
* `v0.5.0`;
* signals;
* operations;
* capital.

DEFERRED
Los componentes restantes necesarios para completar Phase 6 se ejecutarán en etapas posteriores del MISMO Sprint 7, cada una sujeta a una nueva autorización expresa de Luis y a sus gates correspondientes.
L-4
Workflow Status §3.1 permanece:
`EXCLUDED — NOT AUTHORIZED`
No se considera aprobado implícitamente.
L-5
Phase 5 ya está resuelta mediante cierre formal en PR #12.
L-6…L-10
Sin decisión bajo esta orden.
N-1 — OBLIGACIÓN G2/G3
CTO debe confirmar formalmente en Gate 2 que:
`candidate_status` es exclusivamente una proyección derivada del event log y nunca una segunda fuente de verdad.
CRO debe ratificarlo en Gate 3.
Si esto exige modificar el roadmap Active:
STOP.
Requerirá proceso de enmienda §10 y decisión L-2 de Luis.
N-2 — OBLIGACIÓN G2
CTO debe especificar que los huecos `APPROVED` / `IMPLEMENTED` del crosswalk se representarán explícitamente como:
`NO MAPPING — FAIL CLOSED`
Nunca debe inventarse una correspondencia.
MASTER-ROADMAP CONSISTENCY
La inconsistencia post-Phase-5 queda autorizada para corrección mínima en el PR que materialice la autorización de Sprint 7:

* §4 ya no debe decir `Resolve Phase 5`;
* §6 ya no debe decir Analyst Roadmap `Draft / Phase 5 pending`;
* roadmap README debe reflejar Phase 5 closed.

No aprovechar esta corrección para introducir cambios sustantivos o housekeeping no relacionado.
IMPORTANTE
ESTA ORDEN RESUELVE L-1.
NO RESUELVE L-3.
NO AUTORIZA AÚN EL INICIO DE SPRINT 7.
NO AUTORIZA IMPLEMENTACIÓN.
SIGUIENTE PASO
Ejecuta exclusivamente:
`SPRINT 7 GATE 2 — CTO FROZEN-SCOPE DESIGN REVIEW`
sobre el alcance anterior.
Debes verificar:

* completitud técnica;
* consistencia con arquitectura aprobada;
* separabilidad de Stage 1;
* N-1;
* N-2;
* tests/gates;
* que ningún componente EXCLUDED sea necesario para que Stage 1 sea coherente;
* que L-2 realmente no sea necesaria;
* que Stage 1 no implique activation/research/version release.

SOLO LECTURA.
NO código.
NO branch.
NO commit.
NO PR.
NO implementación.
Entrega:
CTO — SPRINT 7 GATE 2 · FROZEN-SCOPE DESIGN REVIEW
y uno de:
`GATE 2 PASS — STAGE 1 DESIGN READY FOR CRO GATE 3`
`GATE 2 CONDITIONAL PASS — NON-BLOCKING ITEMS REMAIN`
`GATE 2 FAIL — SCOPE OR DESIGN REMEDIATION REQUIRED`
Después detente y devuelve el control a Luis.

<!-- END ORIGINAL TEXT -->
