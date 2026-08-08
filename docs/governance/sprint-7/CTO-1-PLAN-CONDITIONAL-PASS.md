<!--
================================================================================
DEPOSIT METADATA — DF-1 STEP 4A (CTO DEPOSIT)
Añadido en el momento del depósito. NO forma parte del texto original del
dictamen, que comienza después del marcador "BEGIN ORIGINAL DICTAMEN TEXT".
================================================================================
preserved_under: DF-1 STEP 4A — CTO DEPOSIT (autorización de Luis, 2026-08-08)
author: CTO (Chief Technology Officer, Project ARES)
verdict: CTO SPRINT 7 PLAN CONDITIONAL PASS
date_of_verdict: 2026-08-04 (fecha auténtica del registro institucional: el
  artefacto 0.4.1-draft, fechado 2026-08-04, ya incorpora las condiciones
  C-1…C-7 de este dictamen)
artifact_reviewed: SPRINT-7-AUTHORIZATION-PACKAGE.md (paquete canónico 0.4.0,
  dictamen TPL "SPRINT 7 AUTHORIZATION PACKAGE READY FOR REVIEW")
artifact_sha256: e19245a4ed457c29f8ee77c330f00929f39eb8200d14226d1b0ef39b5c4147a1
sha256_provenance: DEPOSIT METADATA ONLY — este dictamen es anterior a la
  disciplina de identidad T-23; el hash NO aparece en el texto original y se
  añade aquí únicamente como metadato de depósito, verificado por el CTO contra
  el archivo preservado intacto en el área de trabajo TPL.
conditions_issued: C-1, C-2, C-3, C-4, C-5, C-6, C-7
registry_location: docs/governance/sprint-7/ (registro institucional
  provisional per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL DICTAMEN TEXT (verbatim, sesión CTO) -->

# CTO — REVISIÓN INDEPENDIENTE DEL SPRINT 7 AUTHORIZATION PACKAGE

**Rol ejercido:** Chief Technology Officer de Project ARES. Mandato: evaluar suficiencia técnica del paquete para pasar a revisión CRO. Sin ejecución, sin modificación, sin autorización de inicio.

## Dictamen

# `CTO SPRINT 7 PLAN CONDITIONAL PASS`

El paquete es técnicamente sólido, honesto sobre sus propios límites y trazable a `main` @ `566ab12`. Puede pasar a revisión CRO **con las condiciones C-1…C-7 listadas abajo**, que deben cerrarse antes de que Luis autorice la ejecución. Ninguna condición requiere re-emitir el paquete antes de la revisión CRO.

---

## 1. Baseline e identidad (verificados directamente)

| Elemento | Verificado | Resultado |
|---|---|---|
| Ruta / origin | `Downloads/ares-core 2` · `luisuriostegui1987-sudo/project-ares.git` | ✅ |
| Rama / HEAD | `main` = `566ab12a0b7cbaafeeff5895866c74a996ce52e5` (`git rev-parse`) | ✅ |
| PR #10 | GitHub API: `merged: true`, 2026-08-04T02:39:52Z; `merge_commit_sha` = HEAD | ✅ |
| Fase 5 | MASTER-ROADMAP §5 fila 5: "⏳ pending"; roadmap header `Draft` | ✅ |
| Sprint 7 | MASTER-ROADMAP §4 y roadmap README: "not started" | ✅ |
| Paquete | `pyproject.toml` línea 7: `version = "0.4.0"` | ✅ |
| Tag `v0.5.0` | `git tag --list`: solo v0.2.0/v0.3.0/v0.4.0 | ✅ |
| SHA-256 framework | `shasum -a 256` sobre `docs/specifications/ARES-ANALYST-FRAMEWORK-001.md` = `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9` — idéntico byte a byte | ✅ |
| Framework | No activado; el PR #10 atestó "Research Draft — Pending Institutional Review" byte-idéntico (§11 del cuerpo del PR) | ✅ |
| Working tree | Solo el preexistente `sprint-1-pr1.diff` sin trackear (H-8, ya registrado en el paquete) | ✅ no material |

**El baseline no difiere materialmente → la revisión procede.** Nota de método: el paquete no existe como archivo del repositorio (correcto — es propuesta, no canon); fue localizado y leído íntegro desde el scratchpad de la sesión del Technical Planning Lead (`SPRINT-7-AUTHORIZATION-PACKAGE.md`, 16 secciones completas).

**Fuentes canónicas revisadas directamente:** ARES-ANALYST-ROADMAP-001.md (§§1–10 completos), MASTER-ROADMAP.md (§§1–10), roadmap README, ARES-ANALYST-001.md, ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md (§§0–K completos), research-governance.md, CONTRIBUTING.md, pyproject.toml, ares/models/enums.py, ares/models/ifact.py, ares/models/vocab.py, estructura de `ares/` y `tests/` (231 tests colectados — consistente con el baseline 201 passed + 30 skipped del PR #10), cuerpo del PR #10 (hallazgos preservados), header del framework preservado.

---

## 2. CTO-1 — Alcance técnico canónico de Sprint 7

**Determinación: interpretación 2, con una ambigüedad de descomposición correctamente escalada — y una sobre-afirmación del paquete que debe corregirse (C-1).**

Citas exactas:

- MASTER-ROADMAP §4: *"Sprint 7 — the implementation of the Institutional Knowledge Package Framework (Phase 6 below)"*.
- MASTER-ROADMAP §5 fila 6 (exit criterion): *"Framework implemented and validated (§7)"*.
- Roadmap §5 Cohorte A (capacidad previa): *"Executable IKP framework v0.5.0: loader, validator, AssignmentRef intake, deterministic engine"*.
- Arquitectura §K: plan post-aprobación en 5 pasos (contract types + primitives → loader/validator/registry → engine + persistencia → AnalystService + API → Quant harness), *"Each step lands as its own reviewed PR"*.

El repositorio define canónicamente Sprint 7 como **el framework IKP completo**. El objetivo del paquete (lifecycle + roster + invariantes) es un subconjunto que **no aparece como tal en ninguna descomposición canónica**: proviene del hallazgo preservado H-2, no del §K. Aquí está la sobre-afirmación: el paquete (§3) sostiene que el paso 1 de §K ("Freeze contract types + primitive vocabulary v1") *"contiene el objetivo provisional"*. Es incorrecto: los contract types de §K/§C son `AnalystInput`/`AnalystAssessment`/`AnalystContract` (§2, §C `contract.py`), no los enums de lifecycle/roster. El subconjunto propuesto es *compatible* con Sprint 7 y técnicamente prudente como primera fase, pero su encaje formal requiere exactamente lo que el paquete ya escala: la decisión de Luis (Q-LUIS-1) o una enmienda per §10. El CTO **recomienda** la opción (b) de Q-LUIS-1 (subconjunto primero, §K después en fases subsecuentes del mismo Sprint) por control de riesgo y revisabilidad incremental — pero no puede aprobar la delimitación: está reservada a Luis.

> **C-1** — Corregir en el paquete la trazabilidad "§K paso 1 ⊇ objetivo provisional": sustituir por trazabilidad a H-2 + compatibilidad con §K, dejando explícito que la delimitación es decisión de Luis.

---

## 3. CTO-2 — Mapa de lifecycles

| | Roster (roadmap §6) | Arquitectura (§3) | Workflow Status (§3.1) | Plugin/IKP (§E) + AssignmentRef (§4.1) |
|---|---|---|---|---|
| **Propósito** | Gestión institucional de los 15 slots | Ciclo de vida del analista como unidad arquitectónica | Estado de *cada output analítico material* (contrato §11.2) | Ciclo del artefacto paquete; sobre del encargo |
| **Entidad** | Slot de roster / candidato | Analista/IKP | Output analítico (assessment, informe) | Paquete registrado; assignment |
| **Estados** | `TBD→PROPOSED→PLANNED→RESEARCH_AUTHORIZED→RESEARCH_IN_PROGRESS→IKP_DRAFTED→VALIDATED→APPROVED→IMPLEMENTED→ACTIVE` + `DEFERRED/REJECTED/SUSPENDED/SUPERSEDED/DEPRECATED` | `CANDIDATE→AUTHORIZED→RESEARCHED→PACKAGED→CTO-IMPLEMENTATION-REVIEWED→CRO-VALIDATED→QUANT-VALIDATED→PRODUCTION→DEPRECATED` | `REQUESTED→RESEARCHING→UNDER_REVIEW→CRO_REVIEW→QUANT_REVIEW→APPROVED→PRODUCTION→SUPERSEDED` + `any→REJECTED/REVISION_REQUIRED` | `authored→packaged→validated→registered→resolvable→executable→deprecated` |
| **Transiciones/Autoridad/Evidencia** | Tabla exhaustiva de 14 filas con evidencia, autoridad y revisión por fila (verbatim en §5.2 del paquete — verifiqué fila por fila: **fiel**) | "Every state transition is a recorded event with actor and date"; sin tabla propia — la del roster la operacionaliza | Tabla de ownership por transición; "only Luis can set APPROVED"; "the engine itself NEVER advances a workflow status" | Registro append-only (§13); intake `(create)→REQUESTED` con provenance obligatoria (§4.1 v1.4) |
| **¿Implementable ahora?** | Sí (documentalmente canónico), tras Gates 1–4 del paquete | Sí, vía el crosswalk canónico del roadmap §6 | **No** — RESERVADO: "no implementation exists or may exist until separately approved" | No — pertenece a §K pasos 2+ (loader/registry/engine); fuera del subconjunto propuesto |
| **¿Reservado?** | No | No | **Sí — aprobación separada expresa de Luis** | Depende de Q-LUIS-1 |

**Crosswalk canónico** (roadmap §6, verbatim): `PLANNED↔CANDIDATE`; `RESEARCH_AUTHORIZED↔AUTHORIZED`; `IKP_DRAFTED` abarca `RESEARCHED→PACKAGED`; `VALIDATED` abarca `CTO-IMPLEMENTATION-REVIEWED→CRO-VALIDATED→QUANT-VALIDATED`; `ACTIVE↔PRODUCTION`.

**Superposiciones detectadas (no combinarlas):** (a) `APPROVED` e `IMPLEMENTED` del roster **no tienen contraparte** en el lifecycle de arquitectura §3 — el crosswalk canónico los deja sin mapear; cualquier crosswalk implementado debe representar ese hueco como hueco, no inventar el mapeo. (b) §3.1 comparte nombres de estado (`APPROVED`, `PRODUCTION`, `SUPERSEDED`) con los otros lifecycles aplicando a **otra entidad** — los enums implementados deben ser tipos distintos, nunca un enum compartido. El paquete no comete esta fusión; D1 la evita condicionando §3.1 a Q-LUIS-2. Correcto.

---

## 4. CTO-3 — `candidate_status`

La evidencia canónica es genuinamente insuficiente. Roadmap §3: valores permitidos `PLANNED, PROPOSED, TBD, REJECTED, DEFERRED` **y** *"Status changes follow the lifecycle in §6"* — pero el conjunto §3 es un subconjunto estricto de los estados §6 (faltan `RESEARCH_AUTHORIZED…ACTIVE`, `SUSPENDED`, `SUPERSEDED`, `DEPRECATED`). Dos lecturas compatibles con el texto: (a) `candidate_status` **es** la variable de lifecycle y §3 solo lista los valores válidos pre-gate-8 (todos los slots actuales lo están); (b) es una proyección separada de grano grueso. El documento no lo resuelve.

**Dictamen:** `OPEN DESIGN QUESTION — REQUIRES CTO/CRO DECISION` — confirmo la clasificación del paquete (Q-CTO-2/I-13/H-6). **Recomendación técnica del CTO** (para Gate 2, con acuerdo CRO): modelar **un solo** enum de lifecycle; `candidate_status` como proyección derivada (no almacenada independientemente), con el conjunto §3 como restricción de dominio vigente para slots no autorizados. No requiere migración (no existen instancias persistidas). **Advertencia:** si la resolución cambia el texto del roadmap, requiere enmienda a un artefacto que está `Draft`/Fase 5 `pending` — interactúa con D-1 y debe secuenciarse tras Q-LUIS-3.

---

## 5. CTO-4 — Workflow Status §3.1

Confirmado reservado, verbatim: *"RESERVED — documented only, not implemented; **no implementation exists or may exist until separately approved**"* (arquitectura §3.1).

- **Dependen de §3.1 en el paquete:** D1 (tercera familia de enums, condicionada) y **D2** — el paquete deriva la matriz "de la tabla del roadmap §6 **y de la tabla de ownership de §3.1**". Esto último es implementación parcial del workflow reservado.
- **Implementable sin §3.1:** todo lo demás (D1 sobre roster+arquitectura, D2 solo desde roadmap §6 — cuya tabla es autosuficiente: 14 filas con evidencia/autoridad/revisión —, D3–D10 íntegros).
- **Requiere autorización separada de Luis:** cualquier enum, matriz o validador que materialice estados o transiciones de §3.1.
- **Dictamen CTO:** el paquete ya declara que su aprobación general no constituye la aprobación separada (§3: "solo si el alcance final lo incluye expresamente") — correcto, pero insuficiente como default.

> **C-2** — El alcance inicial debe **excluir §3.1 por defecto**: D1 con dos familias de enums (roster, arquitectura); D2 derivada exclusivamente del roadmap §6. §3.1 entra únicamente con aprobación separada expresa de Luis (Q-LUIS-2 afirmativa y por escrito). El CTO no interpreta —ni puede interpretar— el paquete como autorización implícita.

---

## 6. CTO-5 — Arquitectura recomendada (sin crear archivos)

Recomendación para Gate 2, resolviendo Q-CTO-3 y Q-CTO-4:

| Ruta propuesta (futura) | Propósito | Dependencias (imports) | Interfaz pública prevista | Riesgo de acoplamiento | Evidencia exigida |
|---|---|---|---|---|---|
| `ares/analysts/lifecycle.py` | Enums `str, Enum` de estados (dos familias; tipos distintos) + crosswalk explícito con huecos representados | stdlib solamente | `RosterState`, `ArchitectureState`, `ROSTER_TO_ARCHITECTURE` | Bajo | Cita literal por valor (CA-1); T-1 |
| `ares/analysts/authorities.py` | Vocabulario cerrado de roles/autoridades (CKO, Publishing, CTO, CRO, Quant, Luis) — **hoy no existe en código** | stdlib | `Authority` enum | Bajo | Roadmap §7 / research-governance Roles |
| `ares/analysts/transitions.py` | Matriz cerrada como dato inmutable: `{(from,to): TransitionSpec(autoridad, evidencia, revisión)}`; whitelist estricta | lifecycle, authorities | `TRANSITION_MATRIX`, `validate_transition()` | Bajo | Biyección fila↔fila con roadmap §6 (CA-2); T-2/T-3 |
| `ares/analysts/roster.py` | Modelo Pydantic v2 frozen del slot (12 campos §3) | lifecycle, models/base | `RosterSlot` | Medio (Q-CTO-2) | Round-trip de los 15 slots reales; T-9 |
| `ares/analysts/invariants.py` | Validadores I-1…I-12 | todos los anteriores | `check_*() -> None \| raise` | Bajo | T-4…T-8, T-13 |
| `ares/analysts/transition_log.py` | Evento append-only frozen `(transición, actor, autoridad, evidencia, fecha, seq)` + registro de verificación independiente (D5+D6) | transitions, authorities | `TransitionEvent`, `VerificationRecord`, `reconstruct_history()` | Medio | T-10/T-11; patrón status-events de ifact |

Decisiones de diseño: **ubicación** en `ares/analysts/` per arquitectura §C/§A (sibling de `pipeline`, bajo `service`, sobre repos) — no en `ares/models/`, que es el dominio de research; imports solo descendentes (§D). **Autoridad y evidencia** como tipos, nunca strings libres. **Serialización** JSON canónico con `SCHEMA_VERSION` propio (patrón `ifact.py` `"ARES-FACT-001/1.0"`). **Versionado**: paquete permanece `0.4.0`; `v0.5.0` solo en Gate 10 por Luis. **Persistencia**: fuera de alcance inicial (sin instancias); el log vive como modelo + fixtures hasta que un sprint posterior lo persista con el patrón FactRepository. **Frontera dominio/validación**: invariantes puras sin I/O. **Q-CTO-4**: PR único con commits atómicos por WU (los 10 WU son pequeños; PRs separados fragmentarían la revisión CRO), con opción de dividir si WU-6 se retrasa por Q-CRO-1. **Verificación independiente**: registro tipado dentro de `transition_log.py`, resolvable por id (patrón provenance de §4.1 v1.4).

> **C-3** — Falta un entregable para el **vocabulario de autoridades/identidad de actores** (¿quién es "Luis" para el validador?). Sin él, I-3/I-12 y T-4/T-5 no son implementables de forma determinista. Añadirlo (puede absorberse en D1 o D2 como sub-entregable con su propia trazabilidad a roadmap §7).

> **C-4** — **Estado declarado vs estado calculado**: la arquitectura §13 establece el precedente *"Registry state is derived from its event log — no mutable 'current' flag stored"*. D3 (campo `candidate_status` en el slot) y D5 (log de eventos) crean dos fuentes de verdad potenciales. Condición de diseño para Gate 2: el estado vigente del slot debe **derivarse del log** (o el campo declarado debe validarse contra la derivación en I-nueva); nunca dos verdades independientes.

---

## 7. CTO-6 — Determinismo y fail-closed

El diseño propuesto satisface los nueve requisitos: estados desconocidos (I-9/T-8), transiciones desconocidas (whitelist I-2/T-3), evidencia incompleta (I-6/T-6), autoridad ausente/incorrecta (I-12/T-4), autoaprobación (I-3/T-5), sin fallback permisivo (T-13), reproducibilidad (T-9/T-10), errores explícitos (patrón de la suite existente), nada decidido por narrativa (I-7).

**Rutas que podrían fallar abiertas, a vigilar en implementación:** (1) coerción silenciosa de Pydantic — los modelos deben usar `extra="forbid"` y validación estricta de enums, o T-8 pasa en el test y falla en producción; (2) parámetros con default en validadores — prohibirlos; (3) implementar la matriz como blacklist en lugar de whitelist — CA-3 lo detectaría, pero debe ser requisito de diseño explícito en Gate 2, no solo de test; (4) el hueco del crosswalk (§3 supra) rellenado por conveniencia — debe fallar cerrado como "sin mapeo".

---

## 8. CTO-7 — Verificación independiente `APPROVED → IMPLEMENTED`

Determinación técnica: **artefacto** = registro de conformidad tipado, append-only, resolvable por id (D6), espejo del patrón provenance del AssignmentRef (§4.1 v1.4: un registro sintácticamente completo pero nunca emitido no es válido). **Identidad del verificador** = Quant Research o Publishing Engineer — roles con capacidad V en roadmap §7 que no son autor de la implementación (el CTO es la autoridad de esa transición per roadmap §6 y por tanto **no puede** ser el verificador; I-3 lo codifica). **Autor ≠ verificador** se rechaza estructuralmente (T-7). **Evidencia mínima**: id de transición, actor, verificador, fecha, resultado, refs de evidencia resolubles. **Integridad**: append-only + inmutabilidad frozen; trazabilidad por reconstrucción (T-10). **Rechazo**: `validate_transition` exige registro resoluble; su ausencia es error explícito. **La selección final de autoridad firmante y la suficiencia de riesgo pasan al CRO** (Q-CRO-1) — clasificación DERIVED del paquete confirmada; es requisito técnico (separación de funciones), no invento.

---

## 9. Entregables D1–D10

| ID | Veredicto | Justificación y condiciones |
|---|---|---|
| D1 | **ACCEPT WITH CONDITIONS** | Trazable a roadmap §6 + arquitectura §3. Condiciones: C-2 (excluir §3.1 por defecto), C-3 (autoridades), ubicación per §6 supra. Gate entrada G2 / salida G6 correctos. |
| D2 | **ACCEPT WITH CONDITIONS** | C-2: derivar **solo** del roadmap §6 (autosuficiente); la tabla de ownership §3.1 queda fuera salvo Q-LUIS-2. Whitelist estricta como requisito de diseño. |
| D3 | **ACCEPT WITH CONDITIONS** | 12 campos verificados contra roadmap §3. Condiciones: Q-CTO-2 resuelta en Gate 2 antes de codificar; C-4 (estado derivado). |
| D4 | **ACCEPT WITH CONDITIONS** | Condición: I-13 resuelta o excluida explícitamente del validador; añadir invariantes derivadas de §11 infra. |
| D5 | **ACCEPT** | Patrón Fact-store correcto; evidencia y gates adecuados. Absorber versionado de schema explícito (SCHEMA_VERSION). |
| D6 | **ACCEPT WITH CONDITIONS** | Bloqueado por Q-CRO-1 (el paquete ya lo declara); diseño per §8 supra. |
| D7 | **ACCEPT** | Baseline 201/30 verificado plausible (231 colectados hoy). Añadir tests de §11 infra (condición C-6). |
| D8 | **ACCEPT** | Preservación byte a byte exigida; revisor correcto (Publishing). |
| D9 | **ACCEPT** | SHA-256 antes/después + estado del header; ya verifiqué el hash hoy. |
| D10 | **ACCEPT** | Estructura de dossier correcta; Luis como aprobador final explícito. |

**Entregables ausentes evaluados** (sin agregarlos al alcance): loader, validator, `AssignmentRef` intake y deterministic engine **pertenecen al Sprint 7 canónico** (MASTER-ROADMAP §4; Cohorte A; §K pasos 1–5) y su inclusión u omisión en este paquete es exactamente Q-LUIS-1 — decisión de Luis, correctamente reservada. Versionado/migración: sin datos que migrar (verificado: no existen instancias persistidas de lifecycle); versionado de schema debe hacerse explícito en D3/D5. Audit log: cubierto (D5). Compatibilidad: cubierta (D9, T-9, T-12). Documentación: D8. Pruebas negativas/regresión: T-3…T-8, T-12, T-13.

---

## 10. Invariantes I-1…I-13

| ID | Clasificación CTO | Nota |
|---|---|---|
| I-1 | `DERIVED — TECHNICALLY REQUIRED` | Confirmo la clasificación del paquete |
| I-2 | `CANONICAL — ACCEPTED` | Roadmap §6: tabla cerrada; §1: "no state may bypass them" |
| I-3 | `CANONICAL — ACCEPTED` (principio) + derivación correcta | "no self-approval" es literal en roadmap §6; la generalización a toda transición es DERIVED y el paquete lo declara así — correcto |
| I-4 | `DERIVED — TECHNICALLY REQUIRED` | Requisito real de separación de funciones (el CTO es autoridad de esa transición y no puede autoverificarse); confirmación CRO pendiente (Q-CRO-1) — bien escalado |
| I-5 | `CANONICAL — ACCEPTED` | ARES-ANALYST-001 §1; MASTER-ROADMAP §8 |
| I-6 | `CANONICAL — ACCEPTED` (principio) + aplicación DERIVED | El paquete distingue ambos planos honestamente (§5.2: "analogía normativa") — correcto |
| I-7 | `CANONICAL — ACCEPTED` | Roadmap §7 leyenda, verbatim |
| I-8 | `CANONICAL — ACCEPTED` | MASTER-ROADMAP §2.1; Capital gate |
| I-9 | `DERIVED — TECHNICALLY REQUIRED` | Precedente enums.py/vocab.py ("Values are frozen with the spec") |
| I-10 | `CANONICAL — ACCEPTED` | Roadmap §6 + arquitectura §3, verbatim |
| I-11 | `CANONICAL — ACCEPTED` | Doble fuente literal (roadmap §6; arquitectura §3.1) |
| I-12 | `CANONICAL — ACCEPTED` | "Luis only" en roadmap §6 (VALIDATED→APPROVED) — canónico con independencia de §3.1 |
| I-13 | `OPEN CTO/CRO DECISION` | = Q-CTO-2; ver §4 supra |

**Omisiones detectadas** (ninguna presentada como canónica — todas `DERIVED — TECHNICALLY REQUIRED` salvo indicación):

> **C-5** — Añadir como invariantes derivadas: **I-14** integridad referencial (toda ref de evidencia/verificación debe resolver a un registro existente — espejo del patrón provenance §4.1 v1.4); **I-15** ordenamiento temporal y anti-duplicación (eventos por slot con secuencia monótona; evento duplicado rechazado o idempotente por hash de contenido, patrón registry §13); **I-16** estado calculado ≥ estado declarado (C-4); **I-17** versionado de schema en todo artefacto serializado. Idempotencia: precedente canónico en arquitectura §13 (re-registro same-content idempotente). Inmutabilidad histórica, revocación (vía SUSPENDED), compatibilidad, reproducibilidad e identidad de autoridades quedan cubiertas por I-10, la matriz, T-9/T-12 y C-3 respectivamente.

---

## 11. Pruebas T-1…T-14

Cobertura verificada contra la lista exigida: caminos permitidos (T-2), prohibidos (T-3), estados desconocidos (T-8), autoridad (T-4), autoaprobación (T-5), verificación independiente (T-7), serialización (T-9), compatibilidad/regresión (T-12), determinismo (T-9/T-13), auditabilidad (T-10), fail-closed integral (T-13), preservación (T-14). Datos legacy: N/A (sin instancias — verificado). Cada requisito tiene prueba, resultado verificable, evidencia y propietario; el revisor independiente es la corrida documentada del Gate 6.

> **C-6** — Cobertura insuficiente en tres puntos (condición, no bloqueador): (1) **evidencia alterada o duplicada** — T-6 solo cubre evidencia *ausente/incompleta*; falta test de evento duplicado y de ref adulterada/no resoluble (pareja de I-14/I-15); (2) **ordenamiento temporal** — sin test de eventos fuera de orden; (3) **consistencia estado declarado/derivado** (pareja de C-4). Extender la matriz T con T-15…T-17 antes del Gate 3.

---

## 12. Plan de trabajo (WU-0…WU-9)

Orden lógico correcto (enums → matriz → schema → invariantes → log → verificación → tests → docs → dossier); dependencias bien declaradas; cada WU con punto de detención revisable y commits atómicos revertibles; diseño (Gate 2) separado de implementación (WU-1…WU-6) y de validación (Gate 6). Revisión CTO en dos momentos correctos (Gate 2 diseño; Gate 7 código); CRO en Gates 3 y 8; Luis en Gates 4 y 10 — ningún trabajo precede Gate 4. WU-0 con STOP por baseline divergente es la práctica preservada correcta. **Ajuste recomendado (no bloqueante):** resolver Q-CRO-1 **antes de Gate 4** (el paquete ya lo recomienda) para que WU-6 no quede huérfana a mitad de sprint; si no se resuelve, dividir el PR en dos (WU-1…WU-5 / WU-6+) — cubierto por la recomendación Q-CTO-4 de §6.

---

## 13. Gates

| # | Gate | Clasificación CTO |
|---|---|---|
| 1 | Baseline reconfirmado | `REQUIRED DERIVATION` (práctica preservada en PRs #8/#10; elevarla de "propuesto") |
| 2 | Diseño CTO | `CANONICAL` (CONTRIBUTING §1) |
| 3 | Riesgo CRO | `CANONICAL` (CONTRIBUTING §1) |
| 4 | Autorización de Luis del plan | `CANONICAL` (MASTER-ROADMAP §10; research-governance) |
| 5 | Implementación completa | `PROPOSED` — aceptado |
| 6 | Validación técnica independiente | `REQUIRED DERIVATION` (separación de funciones) |
| 7 | Revisión CTO de código | `CANONICAL` (CONTRIBUTING §§1, 4–5) |
| 8 | Verificación CRO | `CANONICAL` |
| 9 | CI + documentación | `CANONICAL` (CONTRIBUTING §6) |
| 10 | Aprobación final de Luis | `CANONICAL` (Merge gate) |

Confirmaciones exigidas: ninguna implementación precede Gate 4 ✅; ningún merge precede Gate 6 ✅; ninguna activación es consecuencia del merge (OUT OF SCOPE + I-11 + D9) ✅; ningún cambio de versión prematuro (R-8; tag reservado a Gate 10) ✅; el CTO no es autor y verificador único (Gate 6 con verificador ≠ constructor; D6 diseñado-revisado por CRO) ✅; la revisión CRO es condición real con entregables propios (Gates 3 y 8, Q-CRO-1/2) ✅; la aprobación de Luis es explícita y doble (Gates 4 y 10) ✅.

---

## 14. Bloqueadores conocidos (1–10)

| # | Evidencia verificada | Impacto | Bloquea | Autoridad | Condición de cierre |
|---|---|---|---|---|---|
| 1. Alcance parcial vs completo | MASTER-ROADMAP §4; Cohorte A (§2 supra) | Define qué es "Sprint 7 completo" | **Autorización** (no esta revisión) | Luis (Q-LUIS-1) | Decisión de alcance escrita o enmienda §10 |
| 2. Fase 5 `pending` | MASTER-ROADMAP §5 fila 5 | Precondición canónica del inicio | **Autorización/ejecución** | Luis + revisiones CTO/CRO del roadmap | DoD ítems 11–14 del roadmap, o enmienda §10 (Q-LUIS-3) |
| 3. Header `Draft` del roadmap | Frontmatter del artefacto | Mismo hecho que #2 (dos síntomas, un bloqueador) | Ídem | Ídem | Draft→Active tras cierre de Fase 5 |
| 4. Sin cierre formal de Fase 5 en repo | Ausencia de registros CTO PASS/CRO PASS/aprobación para el roadmap | Ídem | Ídem | Ídem | Registros preservados en GitHub |
| 5. §3.1 reservado | Arquitectura §3.1 verbatim | Restringe D1/D2 | **Alcance** | Luis (Q-LUIS-2) | Exclusión por defecto (C-2) o aprobación separada expresa |
| 6. `candidate_status` vs lifecycle | Roadmap §3 vs §6 (§4 supra) | Diseño de D3 | **Diseño (Gate 2)** | CTO+CRO; enmienda si toca el texto canónico → Luis | Resolución Q-CTO-2 registrada |
| 7. Relación entre tres lifecycles | §3 supra | Diseño de D1; huecos del crosswalk | **Diseño (Gate 2)** | CTO (Q-CTO-1) | Tipos separados + crosswalk con huecos explícitos |
| 8. Autoridad de verificación | Roadmap §7 (roles V); H-3 | D6/WU-6 | **WU-6** | CRO (Q-CRO-1) | Dictamen CRO sobre firmante y contenido mínimo |
| 9. Posible enmienda §10 | MASTER-ROADMAP §10 | Ruta alternativa a #2 | Autorización | Luis con revisión CTO/CRO | Enmienda formal aprobada, si se elige esa ruta |
| 10. Merge práctica vs CONTRIBUTING §4 | Verificado: `566ab12` tiene dos padres (`31b0db2`, `996c400`); CONTRIBUTING §4 pide squash-merge | Housekeeping; no afecta integridad del baseline | **Nada** (no bloquea) | Luis (Q-LUIS-4) | Alinear práctica o enmendar CONTRIBUTING §4 |

Ninguno bloquea **esta revisión**; #1, #2/3/4 y #5 bloquean la **autorización de ejecución**; #6, #7, #8 bloquean **gates internos** ya secuenciados.

---

## 15. Preguntas para el CRO y decisiones reservadas a Luis

**Al CRO:** Q-CRO-1 (firmante y contenido mínimo del registro de verificación independiente — recomendado resolver antes de Gate 4); Q-CRO-2 (suficiencia de T-13 como demostración de no-bypass, ahora extendida con C-6); adicionalmente, opinión de riesgo sobre C-4 (estado derivado vs declarado) y sobre la exclusión por defecto de §3.1 (C-2).

**Reservadas a Luis (el CTO no las resuelve):** Q-LUIS-1 (alcance: §K completo vs subconjunto — recomendación CTO: subconjunto primero, sin efecto autoritativo); Q-LUIS-2 (§3.1); Q-LUIS-3 (ruta de cierre de Fase 5 o enmienda §10); Q-LUIS-4 (housekeeping: `sprint-1-pr1.diff`, H-4, H-5).

---

## 16. Condiciones del CONDITIONAL PASS (recapitulación)

- **C-1** — Corregir la trazabilidad del subconjunto a "§K paso 1" (sobre-afirmación); re-anclar en H-2 + Q-LUIS-1.
- **C-2** — Excluir Workflow Status §3.1 del alcance por defecto (D1 y D2 solo desde roadmap §6/arquitectura §3); inclusión solo con aprobación separada expresa de Luis.
- **C-3** — Añadir el vocabulario de autoridades/identidad de actores como entregable trazable (roadmap §7).
- **C-4** — Regla de diseño: estado vigente derivado del log de eventos (o validado contra él); nunca dos fuentes de verdad.
- **C-5** — Añadir invariantes derivadas I-14…I-17 (integridad referencial, orden/duplicación, estado derivado, versionado de schema).
- **C-6** — Extender la matriz de pruebas con T-15…T-17 (evidencia duplicada/adulterada, orden temporal, consistencia de estado) antes del Gate 3.
- **C-7** — Resolver Q-CRO-1 antes de Gate 4, o dividir el PR para aislar WU-6.

Cierres C-1, C-5, C-6: actualización del paquete antes de presentarlo a Luis. C-2, C-3, C-4: registrables como decisiones de Gate 2. C-7: secuenciación.

---

## 17. Confirmaciones de gobernanza

- ✅ **No se modificaron archivos ni GitHub**: solo operaciones de lectura (`git remote/branch/rev-parse/status/tag/log`, `shasum`, GitHub API GET, lectura de archivos). Working tree final idéntico al inicial (`?? sprint-1-pr1.diff` preexistente); HEAD sigue `566ab12a0b7cbaafeeff5895866c74a996ce52e5`.
- ✅ **Fase 5 sigue `pending`**; roadmap sigue `Draft`.
- ✅ **Sprint 7 sigue `not started`** — no se creó rama, commit, PR ni código.
- ✅ **Paquete sigue `0.4.0`**; **`v0.5.0` sigue inexistente**.
- ✅ **SHA-256 del framework** verificado hoy: `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9` — byte-idéntico; **no activado** (header "Research Draft — Pending Institutional Review" intacto).
- ✅ **No se investigaron inversionistas** ni candidatos; `docs/analysts/` sigue estructura-solo.
- ✅ **No se crearon IKPs, enums, schemas, validators, engines ni código.**
- ✅ **No se autorizó capital, señales ni operaciones.**
- ✅ Los hallazgos H-1…H-8 permanecen preservados sin eliminación ni reclasificación (H-4 y H-5 re-verificados directamente: la cita "§6.1" existe en roadmap §1 mientras MASTER-ROADMAP §6 es lista numerada sin subsección; el merge commit de PR #10 tiene dos padres contra la norma squash de CONTRIBUTING §4).

---

## Dictamen exacto

# `CTO SPRINT 7 PLAN CONDITIONAL PASS`

El paquete puede pasar a revisión del CRO con las condiciones C-1…C-7. Un CONDITIONAL PASS **no inicia Sprint 7**: el inicio sigue bloqueado por D-1 (Fase 5), Q-LUIS-1/2/3 y la aprobación explícita de Luis en Gate 4. Conforme al punto de detención del mandato, me detengo aquí: no actualizo el paquete, no ejecuto Sprint 7 y no realizo la revisión CRO. El siguiente relevo depende de este dictamen.

<!-- END ORIGINAL DICTAMEN TEXT -->
