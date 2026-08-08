<!--
================================================================================
DEPOSIT METADATA — DF-1 STEP 4A (CTO DEPOSIT)
Añadido en el momento del depósito. NO forma parte del texto original del
dictamen, que comienza después del marcador "BEGIN ORIGINAL DICTAMEN TEXT".
================================================================================
preserved_under: DF-1 STEP 4A — CTO DEPOSIT (autorización de Luis, 2026-08-08)
author: CTO (Chief Technology Officer, Project ARES)
verdict: CTO SPRINT 7 SECOND LIMITED REMEDIATION RE-VERIFICATION PASS
date_of_verdict: 2026-08-08 (fecha de emisión en el registro de la sesión CTO;
  posterior a la creación de r2 el 2026-08-05 19:06 y al dictamen CRO
  REQUIRES REVISION del 2026-08-05)
artifact_reviewed: SPRINT-7-AUTHORIZATION-PACKAGE-0.4.1-draft-remediated-r2.md
  (0.4.1-draft r2, segunda remediación)
artifact_sha256: 82bb6c525dd8d8b2aca74595ef0558149db0b4535649b78727ec161a11715d32
sha256_provenance: registrado DENTRO del texto original del dictamen (§1 del
  reporte), recomputado por el CTO en el momento de la revisión; se repite aquí
  como metadato de depósito.
conditions_issued: ninguna condición CTO nueva; DF-1 permanece abierto como
  obligación de autoridad antes del Gate 4 (tratamiento expreso en §5 del
  reporte)
registry_location: docs/governance/sprint-7/ (registro institucional
  provisional per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL DICTAMEN TEXT (verbatim, sesión CTO) -->

# CTO — SECOND LIMITED REMEDIATION RE-VERIFICATION · SPRINT 7 `0.4.1-draft` r2

**Rol ejercido:** CTO — re-verificación independiente, limitada, de solo lectura. Nada modificado, nada depositado, DF-1 no cerrado por mi cuenta.

## Dictamen

# `CTO SPRINT 7 SECOND LIMITED REMEDIATION RE-VERIFICATION PASS`

La segunda remediación implementa fielmente y sin expansión lo ordenado: T-20/T-21 restaurados a la sustancia F-1 del CRO, controles de preservación reasignados íntegros a T-22/T-23, referencias actualizadas, R-14 re-calificado, DF-1 honesto y abierto, y **cero regresión** en CTO-F1…F4. DF-1 permanece abierto como obligación de autoridad (no defecto de r2).

---

## 1. Identidades y linaje (recomputados directamente)

| Artefacto | SHA-256 recomputado | Esperado |
|---|---|---|
| **r2** (`…-remediated-r2.md`, 2026-08-05 19:06) | `82bb6c525dd8d8b2aca74595ef0558149db0b4535649b78727ec161a11715d32` | ✅ idéntico |
| Entrada (`…-remediated.md`) | `ee1759c59f1e01d3d27c94725da39eee29bb9d36aa24c5b50d84625df995f943` | ✅ **byte-idéntico, preservado intacto** |
| (Control) pre-remediación / canónico `0.4.0` / framework | `d6e11b7f…ee91` / `e19245a4…47a1` / `cac6ad75…711df9` | ✅ intactos y mutuamente distintos |

**Control del diff:** recalculé el diff completo entrada → r2 y **coincide línea a línea** con el `SPRINT-7-PACKAGE-SECOND-REMEDIATION.diff` entregado (96 líneas cambiadas, auditadas una a una). Cada hunk pertenece exclusivamente a: restauración F-1 de T-20/T-21 (§9.3, D2, G6/G8/G9, DoD), renumeración T-22/T-23 con nota de trazabilidad (§9.3, §0.1), actualización de referencias estrictamente necesaria (rangos → T-1…T-23 en resumen/§3.2/D7/WU-7; nota de T-14 → T-23; DF-1/H-9 → T-22/T-23), re-calificación de R-14, registro §0.2 y cabecera/dictamen TPL. **Ninguna expansión material no autorizada.**

## 2. Verificación principal

**A. T-20 — CONFORME.** Representa exclusivamente la clausura exhaustiva de pares: enumeración programática de **todos** los pares ordenados (producto cartesiano completo), whitelist = **exactamente las 14 transiciones de §5.2**, positivos por cada par autorizado con autoridad y evidencia válidas, rechazo fail-closed de **todo el complemento** ("par fuera de whitelist que transicione = fallo del control; cobertura incompleta = fallo del control"), vínculo expreso a **I-2**, requisito de **G6 y G8** (exigido además en las filas G6/G8 de §10.1), y declaración explícita de que **T-13/fuzzing no lo sustituye**. Coincide con la especificación autocontenida del punto 8 del dictamen CRO de registro.

**B. T-21 — CONFORME.** Representa exclusivamente la ablación por fila: para **cada una de las 14 transiciones**, evento válido de control + variantes eliminando **individualmente** cada elemento obligatorio (la autoridad; **cada** pieza de evidencia de la fila; el registro **§5C** en `APPROVED → IMPLEMENTED`), rechazo de toda variante incompleta ("ningún elemento obligatorio puede resultar opcional en la práctica"), determinista/reproducible (matriz fila × elemento-eliminado), vínculos a **I-6, I-14 e I-4** cuando aplica, requisito de **G6/G8**, y fuzzing declarado no equivalente. Fiel a la especificación CRO.

**C. T-22 — CONFORME.** El control de preservación/resolución de reportes citados conserva su sustancia **sin cambio material**: cotejé campo por campo contra la tabla de la primera remediación — idénticos salvo la renumeración, el énfasis tipográfico y la simplificación del gate ("tras ratificación CRO en G3" retirado), que es consistente con el registro: el CRO otorgó la ratificación de sustancia **condicionada precisamente a esta renumeración** (RF-3 de su dictamen `REQUIRES REVISION`, verificado contra el reporte CRO original, no contra la transcripción). La afirmación "sustancia ratificada por CRO" es por tanto exacta, no una auto-certificación.

**D. T-23 — CONFORME.** Identidad por SHA-256 completo de 64 caracteres, recomputable, fail-closed (hash abreviado, ausente o no coincidente al recomputar ⇒ la revisión no habilita nada); sustancia idéntica al ex-T-21 de preservación, sin cambio material.

**E. Unicidad — CONFORME.** Grep exhaustivo sobre r2: **cero** rangos residuales `T-1…T-19`/`T-1R…T-19` (todos actualizados a T-23); **todas** las ocurrencias de T-20/T-21 llevan la semántica F-1 (clausura/ablación) o son notas de trazabilidad que documentan expresamente la colisión histórica; la regla de hashes abreviados de la nota de T-14 apunta ahora a **T-23** (cero referencias residuales a T-21 en ese rol); T-20/T-21/T-22/T-23 tienen identidades únicas, semánticas disjuntas y referencias correctas en §0.1, §0.2, §3.2, D2, D7, WU-7, §9.3, G6/G8/G9, DoD, DF-1, H-9 y R-14. La nota de trazabilidad de §9.3 declara además que ninguno de los cuatro controles se perdió ni sobrescribió — verificado: la sustancia de los cuatro está íntegra en el documento.

**F. R-14 / DF-1 — CONFORME.** DF-1 continúa **ABIERTO** (`UNRESOLVED — REQUIRES AUTHORITY REVIEW`, declarado en cabecera §0.1, §0.2, §7, §15 y el dictamen TPL); no existe auto-certificación — el TPL amplió incluso su descargo ("no puede crear, reconstruir, atribuir, **depositar ni auto-certificar**"); R-14 re-calificado a probabilidad **Media / impacto Alto** con residual "**Elevado mientras DF-1 permanezca abierto**", conforme al dictamen CRO; y nada en r2 implica que el depósito ocurrió — la única mención de "depositados" es la condición futura de rebaja del riesgo.

## 3. Control de regresión CTO-F1…F4 — SIN REGRESIÓN

Prueba por construcción: el artefacto de entrada `ee1759c5…` (donde verifiqué el cierre de las cuatro en mi re-verificación anterior) permanece byte-idéntico, y el diff recalculado **no toca** la fila G2 de §10.1 (sigue invalidando 3–10, con G3 exigiendo "Dictamen G2 vigente"), ni el ¶1 de §3.1 (sin ancla a §K; primitive vocabulary fuera de alcance), ni los valores de hash completos de §2/D9/T-14 (solo la referencia cruzada T-21→T-23 en la nota de T-14, que es la corrección ordenada), ni la nota de §5.2 (`REVISION_REQUIRED` confinado a §3.1, excluido). Las cuatro permanecen cerradas; ninguna se reabre.

## 4. Baseline (reconfirmado antes y después — solo lecturas intermedias)

`HEAD` = `566ab12a0b7cbaafeeff5895866c74a996ce52e5` ✅ · Fase 5 `pending` ✅ · Sprint 7 `not started` ✅ · software y paquete canónico `0.4.0` ✅ · **r2 no canónico** (así se autodeclara, igual que su entrada) ✅ · `v0.5.0` inexistente ✅ · framework byte-idéntico y no activado ✅ · §3.1 excluido/no autorizado (refuerzos intactos: §3.3, T-1R, CA-13) ✅ · sin implementación, sin IKP/`AssignmentRef`, sin nuevos analistas (`docs/analysts/` = 0 archivos no-README), sin señales/operaciones, sin activación, sin capital ✅ · árbol de trabajo: solo el preexistente `sprint-1-pr1.diff` (H-8) ✅.

## 5. Tratamiento expreso de lo pendiente

- **T-20/T-21/T-22/T-23:** verificados conformes desde la autoridad CTO; la **ratificación final sobre r2 corresponde al CRO** en su propia re-verificación (RF-1 quedó implementada según su especificación literal, pero el CRO no está vinculado por mi conclusión).
- **DF-1 (único pendiente institucional):** permanece abierto **por diseño correcto** — su cierre exige el depósito de cada reporte por su autor (los tres CTO, los tres CRO, más las re-verificaciones sobre r2) con el hash del artefacto revisado, vía PR autorizado por orden separada de Luis, **antes del Gate 4**. R-14 permanece elevado hasta entonces.

Este PASS no autoriza Sprint 7, canonización, implementación, merge, activación, operaciones ni capital, y no ejecuta ninguna decisión L-1…L-10. El siguiente relevo es la re-verificación CRO de r2 (`82bb6c52…5d32`).

Me detengo aquí.

<!-- END ORIGINAL DICTAMEN TEXT -->
