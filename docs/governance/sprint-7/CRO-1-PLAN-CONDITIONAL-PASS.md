<!--
================================================================================
DEPOSIT METADATA — DF-1 STEP 4B (CRO DEPOSIT)
Añadido en el momento del depósito. NO forma parte del texto original del
dictamen, que comienza después del marcador "BEGIN ORIGINAL DICTAMEN TEXT".
================================================================================
preserved_under: DF-1 STEP 4B — CRO DEPOSIT (autorización de Luis, 2026-08-08)
author: CRO (Chief Risk Officer, Project ARES)
verdict: CRO SPRINT 7 PLAN CONDITIONAL PASS
date_of_verdict: 2026-08-04 (fecha auténtica del registro institucional: el
  artefacto 0.4.1-draft, fechado 2026-08-04, ya incorpora las condiciones
  CR-1…CR-4 y las resoluciones Q-CRO-1/Q-CRO-2 de este dictamen)
artifact_reviewed: SPRINT-7-AUTHORIZATION-PACKAGE.md (paquete canónico 0.4.0,
  dictamen TPL "SPRINT 7 AUTHORIZATION PACKAGE READY FOR REVIEW")
artifact_sha256: e19245a4ed457c29f8ee77c330f00929f39eb8200d14226d1b0ef39b5c4147a1
sha256_provenance: DEPOSIT METADATA ONLY — este dictamen es anterior a la
  disciplina de identidad T-23; el hash NO aparece en el texto original y se
  añade aquí únicamente como metadato de depósito, recomputado por el CRO
  contra el archivo preservado intacto en el área de trabajo TPL.
conditions_issued: CR-1, CR-2, CR-3, CR-4 (+ resoluciones Q-CRO-1 y Q-CRO-2;
  ratificación de C-3, C-4, C-5, C-6 del CTO; C-7 satisfecha por la resolución
  de Q-CRO-1)
registry_location: docs/governance/sprint-7/ (registro institucional
  provisional per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL DICTAMEN TEXT (verbatim, sesión CRO) -->

He leído el paquete íntegro (16 secciones, 349 líneas) y verificado el baseline de forma independiente. Emito la revisión CRO (Gate 3 sobre el plan).

---

# CRO — REVISIÓN DE RIESGO DEL SPRINT 7 AUTHORIZATION PACKAGE

**Rol ejercido**: Chief Risk Officer — metodología, epistemología y riesgo institucional. Sin ejecución, sin modificación de archivos ni de GitHub, sin autorización de inicio. No acepté como sustituto ni el reporte del Technical Planning Lead ni el dictamen CTO: baseline y paquete verificados/leídos directamente.

## Dictamen

# `CRO SPRINT 7 PLAN CONDITIONAL PASS`

El paquete es epistemológicamente honesto, fail-closed por diseño y trazable. Puede presentarse a Luis **una vez cerradas las condiciones CR-1…CR-3** (correcciones al texto del paquete) junto con las C-1/C-5/C-6 del CTO, con las que concurro. **Q-CRO-1 queda resuelta en este dictamen** (satisface C-7 del CTO). Nada de esto inicia Sprint 7 ni sustituye las decisiones reservadas a Luis (Q-LUIS-1/2/3, D-1).

## 1. Baseline verificado independientemente

`main` = `566ab12` (dos padres: merge de PR #10 — coincide con H-5) · árbol limpio salvo el preexistente `sprint-1-pr1.diff` (H-8) · paquete `0.4.0` · tags solo v0.2.0/v0.3.0/v0.4.0 (sin `v0.5.0`) · framework preservado byte-idéntico: `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9` · Fase 5 `pending` (fila 5 del MASTER-ROADMAP) · Sprint 7 `not started` · `docs/analysts/` solo estructura. El paquete fue leído desde el scratchpad de la sesión del Technical Planning Lead (40,783 bytes) — correctamente **no** está en el repositorio: es propuesta, no canon.

## 2. Evaluación epistemológica del paquete

**Fortalezas (determinantes del pase):** el paquete aplica a la gobernanza la misma disciplina RULE 17 que exige al research — cada invariante y cada regla está clasificada como `CANONICAL`, `DERIVED FOR IMPLEMENTATION` u `OPEN DECISION`, con cita literal por base (verifiqué las citas contra los documentos canónicos: fieles). Declara sus propios supuestos («no existe cadencia canónica de sprint»), llama «analogía normativa» a lo que es analogía, admite que su preparación no satisface ningún punto de su propia DoD, y preserva los hallazgos H-1…H-8 sin reclasificarlos. La tabla §5.2 es fiel fila por fila al roadmap §6 (re-verificada).

**Defecto epistémico material (CR-1 ≡ C-1 del CTO, concurro):** §3 afirma que el paso 1 de arquitectura §K «contiene el objetivo provisional». Verificado contra §K/§C: es falso — los contract types de §K.1 son `AnalystInput`/`AnalystAssessment`/`AnalystContract`, no los enums de lifecycle/roster. Esto es exactamente el tipo de lavado que el sistema prohíbe: una interpretación derivada presentada con procedencia canónica. Riesgo: Luis autorizaría el subconjunto creyendo que es la descomposición canónicamente prescrita. Corrección mínima: re-anclar la trazabilidad en H-2 + compatibilidad con §K, dejando la delimitación como Q-LUIS-1. **CONDITION antes de presentar a Luis.**

## 3. Q-CRO-1 — RESUELTA: registro de verificación independiente `APPROVED → IMPLEMENTED`

**Quién puede firmar:** **Quant Research o Publishing Engineer** (uno basta; no exijo ambos — la revisión CRO de Gate 8 ya es una segunda capa; exigir dos firmantes añade proceso sin reducir riesgo). Restricciones estructurales innegociables: (a) el firmante no puede haber autorado **ningún** commit de la implementación verificada (autor ≠ verificador validado contra la lista de autores, no declarado por narrativa); (b) el **CTO nunca puede firmar** (es la autoridad de la transición per roadmap §6 — sería juez y parte); (c) preferencia de asignación: **Quant** cuando la implementación incluya semántica de reglas/cálculo (dominio de vectores dorados); **Publishing Engineer** para conformidad estructural/documental.

**Contenido mínimo del registro (todo resoluble por id, append-only, frozen):**
1. Id del registro + id de la transición y del slot/analista afectado.
2. Refs del artefacto verificado: SHAs de commits, PR, versión del paquete/IKP y su content hash.
3. Identidad y rol del verificador + lista de autores de la implementación + atestación estructural de no-solapamiento.
4. Método de verificación (corrida independiente de la suite / vectores dorados no autorados por el CTO / checklist de conformidad contra la tabla canónica) con refs de evidencia **resolubles** (espejo del patrón provenance del AssignmentRef §4.1 v1.4 — un registro completo pero nunca emitido no es válido).
5. Resultado PASS/FAIL con razones, fecha, y secuencia monótona en el log.
6. Vínculo bidireccional: el evento de transición referencia el registro; `validate_transition` **falla cerrado** si el registro falta, no resuelve, o hay solapamiento autor/verificador.

Con esto **C-7 del CTO queda satisfecha** (Q-CRO-1 resuelta antes de Gate 4); confirmación formal final del diseño materializado en Gate 3/8, como ya prevé D6.

## 4. Q-CRO-2 — RESUELTA: T-13 es necesaria pero NO suficiente

El fuzzing acotado **muestrea**; no demuestra clausura. Como evidencia de «ninguna transición puede omitir autoridades» exijo además (CR-3):

- **T-18 — Clausura exhaustiva**: el espacio de estados es finito y pequeño; el test debe enumerar **todos** los pares ordenados (estado, estado) y verificar que todo par fuera de la whitelist es rechazado. Esto es prueba completa, no muestreo.
- **T-19 — Ablación por fila**: para cada transición permitida, remover uno a uno cada elemento requerido (autoridad, cada pieza de evidencia, registro de verificación cuando aplique) debe producir rechazo. Demuestra que ningún requisito es decorativo.
- Más las **T-15…T-17 de C-6 del CTO** (evidencia duplicada/adulterada, orden temporal, consistencia declarado/derivado), con las que concurro desde el dominio de riesgo (parejas de I-14/I-15/I-16).

T-13 se conserva como defensa adicional, no como demostración.

## 5. Opiniones de riesgo solicitadas por el CTO

**C-2 (exclusión de §3.1 por defecto): CONCURRO Y LA ENDUREZCO (CR-2).** El texto del paquete (§3, REQUIRES SEPARATE AUTHORIZATION) dice que la aprobación del paquete por Luis «constituiría esa aprobación separada solo si el alcance final lo incluye expresamente». Eso es **aprobación por empaquetado** — el mismo defecto de ambigüedad que la ratificación del PR #8 evitó exigiendo constancia explícita. Posición CRO: la implementación del Workflow Status §3.1 requiere un **registro de decisión autónomo y expreso de Luis que nombre §3.1**, nunca una cláusula dentro de la aprobación general del paquete. La frase citada debe corregirse en la misma actualización que CR-1. Riesgo mitigado: autorización implícita de un componente que la arquitectura reserva con lenguaje absoluto («no implementation exists or may exist until separately approved»).

**C-4 (estado derivado vs declarado): CONCURRO SIN RESERVAS.** Dos fuentes de verdad para el estado es lavado de estado por construcción — la variante estructural de lavar opinión en hecho. El precedente canónico (arquitectura §13: estado derivado del event log, sin flag mutable) es la única forma compatible. Endoso I-16 + T-17 como pareja obligatoria, verificación CRO en Gate 8.

**C-3, C-5, C-6 del CTO:** concurro con las tres. Sobre C-3 añado la expectativa de diseño de que la identidad del actor quede **vinculada al registro de GitHub preservado** (el actor de un evento es el que consta en el PR/merge — no un string autodeclarado); la autenticación plena queda fuera de alcance, pero el registro debe anclar a la identidad preservada.

## 6. Hallazgo CRO adicional

**CR-4 (NON-BLOCKING, para D8):** la persistencia del transition log queda fuera del alcance inicial (modelos + fixtures hasta un sprint posterior). Riesgo: confundir el código con el sistema de registro institucional. La documentación D8 debe declarar explícitamente que, hasta que la persistencia aterrice, **GitHub sigue siendo el único registro institucional de transiciones** y el código es el validador de esa disciplina, no su sustituto. Sin esto, un evento «registrado» solo en memoria podría citarse como si fuera canon.

## 7. Entregables, invariantes, gates y riesgos — veredicto CRO

- **D1–D10**: sin objeción de riesgo adicional a las condiciones CTO; D6 queda gobernado por la resolución de Q-CRO-1 (§3 supra). D4/D5/D6 con aprobación conjunta CTO+CRO: correcto.
- **I-1…I-12**: clasificaciones confirmadas; la generalización DERIVED de I-3 e I-6 es exigencia de riesgo real, no invención. **I-14…I-17 (C-5)**: endosadas. I-13 = Q-CTO-2: acepto la recomendación CTO (un solo lifecycle; `candidate_status` como proyección derivada, jamás almacenada independientemente — coherente con I-16); si la resolución toca el texto del roadmap, requiere enmienda con secuencia post-Q-LUIS-3, como advirtió el CTO.
- **Gates 1–10**: la doble aprobación de Luis (4 y 10), la separación diseño/implementación/validación y el STOP de WU-0 son correctos. Confirmo desde riesgo: ningún WU precede Gate 4; el merge exige Gate 6; la activación no es consecuencia del merge.
- **Registro de riesgos R-1…R-10**: cobertura adecuada; el único residual Medio (R-3) está correctamente condicionado a Gate 2. Con CR-3, el control de detección de R-4 pasa de muestreo a demostración.
- **OUT OF SCOPE**: la preservación de H-1 (concurrencia), el bloqueo de investigación, la no-activación del framework y la reserva de `v0.5.0` a Gate 10 están correctamente blindadas.

## 8. Condiciones del CONDITIONAL PASS (CRO)

| ID | Condición | Cuándo |
|---|---|---|
| **CR-1** (≡ C-1 CTO) | Corregir en el paquete la sobre-afirmación «§K paso 1 contiene el objetivo provisional»; re-anclar en H-2 + Q-LUIS-1 | Antes de presentar a Luis |
| **CR-2** (endurece C-2 CTO) | §3.1 excluido por defecto; y corregir la cláusula de «aprobación separada por empaquetado»: la eventual inclusión de §3.1 exige registro de decisión autónomo de Luis que lo nombre | Antes de presentar a Luis |
| **CR-3** (extiende C-6 CTO) | Añadir T-18 (clausura exhaustiva de pares) y T-19 (ablación por fila) a la matriz de pruebas, junto con T-15…T-17 | En la actualización del paquete; demostradas en Gate 8 |
| **CR-4** | D8 debe declarar que GitHub sigue siendo el sistema de registro institucional hasta que la persistencia del log aterrice | Gate 2 (decisión de diseño) / Gate 9 (docs) |

Q-CRO-1: **resuelta** (§3). Q-CRO-2: **resuelta** (§4). C-7 del CTO: **satisfecha**.

## 9. Confirmaciones de gobernanza

- ✅ Solo operaciones de lectura; ningún archivo, commit, rama, PR, tag ni metadato modificado; HEAD sigue `566ab12`; árbol idéntico.
- ✅ Fase 5 sigue `pending`; Sprint 7 sigue `not started`; paquete `0.4.0`; `v0.5.0` inexistente.
- ✅ Framework preservado byte-idéntico y **no activado**; `docs/analysts/` solo estructura; ningún inversionista investigado ni autorizado; ningún IKP ni código creado.
- ✅ Este dictamen no constituye aprobación de Luis, autorización de inicio de Sprint 7, resolución de Q-LUIS-1/2/3, cierre de Fase 5, activación del framework ni autorización de capital.

**Siguiente relevo previsto**: el Technical Planning Lead actualiza el paquete cerrando CR-1/CR-2/CR-3 (+ C-1/C-5/C-6 del CTO en la misma edición); CTO y CRO confirman las condiciones sobre el paquete actualizado; después se presenta a Luis el dossier con las cuatro opciones de decisión de §16, con Q-LUIS-1/2/3 y D-1 como decisiones previas bloqueantes del inicio.

Me detengo aquí.

<!-- END ORIGINAL DICTAMEN TEXT -->
