<!--
================================================================================
DEPOSIT METADATA — DF-1 STEP 4B (CRO DEPOSIT)
Añadido en el momento del depósito. NO forma parte del texto original del
dictamen, que comienza después del marcador "BEGIN ORIGINAL DICTAMEN TEXT".
================================================================================
preserved_under: DF-1 STEP 4B — CRO DEPOSIT (autorización de Luis, 2026-08-08)
author: CRO (Chief Risk Officer, Project ARES)
verdict: CRO SPRINT 7 0.4.1-DRAFT REMEDIATION REQUIRES REVISION
date_of_verdict: 2026-08-05 (fecha auténtica acotada por el registro
  institucional, no inferida: posterior al artefacto remediado revisado —
  creado 2026-08-05 09:43 — y anterior a la segunda remediación r2 de
  2026-08-05 19:06, que implementa la determinación de numeración de este
  dictamen)
artifact_reviewed: SPRINT-7-AUTHORIZATION-PACKAGE-0.4.1-draft-remediated.md
  (primera remediación limitada del TPL)
artifact_sha256: ee1759c59f1e01d3d27c94725da39eee29bb9d36aa24c5b50d84625df995f943
sha256_provenance: ORIGINAL TEXT — el hash completo del artefacto auditado
  consta en la tabla de identidades del texto original (recomputado por el
  CRO durante la auditoría).
conditions_issued: RF-1 (MATERIAL — impide PASS), RF-2 (CONDITION),
  RF-3 (ratificación de T-22/T-23 condicionada a renumeración);
  adjudicación de la colisión T-20/T-21 y especificación autocontenida de
  restauración
registry_location: docs/governance/sprint-7/ (registro institucional
  provisional per CR-4)
================================================================================
-->

<!-- BEGIN ORIGINAL DICTAMEN TEXT (verbatim, sesión CRO) -->

La re-verificación está completa: identidades recomputadas sin confusión, diff de remediación recalculado independientemente (coincide con el entregado), y el contenido auditado línea por línea contra mis condiciones originales. Emito el reporte.

---

# CRO — LIMITED REMEDIATION RE-VERIFICATION · SPRINT 7 AUTHORIZATION PACKAGE `0.4.1-draft`

**1. Rol ejercido:** Chief Risk Officer — re-verificación limitada, independiente y de solo lectura. No vinculado por TPL ni CTO.

**2. Baseline reconfirmado (antes y después — solo lecturas intermedias):** `HEAD` = `566ab12a…ce52e5` · árbol limpio (solo `sprint-1-pr1.diff`, H-8) · software y paquete canónico `0.4.0` · tags v0.2.0/v0.3.0/v0.4.0 (`v0.5.0` inexistente) · framework byte-idéntico `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9`, no activado · Fase 5 `pending` · Sprint 7 `not started` · §3.1 excluido · sin IKP, sin AssignmentRef, sin nuevos analistas, sin señales, sin activación, sin capital.

**3–4. Fuentes e identidades (recomputadas por mí, sin confusión ni intercambio):**

| Artefacto | SHA-256 recomputado | Coincide |
|---|---|---|
| Remediado (`…-remediated.md`, 75,512 bytes) | `ee1759c59f1e01d3d27c94725da39eee29bb9d36aa24c5b50d84625df995f943` | ✅ |
| Pre-remediación (preservado intacto) | `d6e11b7f7bdd13271818d4dd818ea3986cbadd4fa58affbb8a1ecb06c5b3ee91` | ✅ |
| Paquete canónico `0.4.0` | `e19245a4…5c4147a1` | ✅ |
| Framework preservado | `cac6ad75…711df9` | ✅ |

Diff de remediación **recalculado independientemente**: coincide exactamente con el `.diff` del TPL. Distinción de evidencia: el reporte de remediación TPL está **embebido y preservado** en el artefacto (§0.1); el reporte de re-verificación CTO **no está preservado como artefacto** — solo su dictamen transcrito en esta orden; mis condiciones originales las cotejé contra **mi propio registro de sesión**, no contra transcripciones.

## 5. Resultado de cada condición CRO

| ID | Requisito exacto | Evidencia / ubicación | Resultado |
|---|---|---|---|
| **F-2** (≡ CTO-F1) | Reapertura de G2 invalida **3–10** | §10.1 fila 2: corregido a `3–10`; fila 3: evidencia de entrada ahora exige «Dictamen G2 vigente» | **CERRADA** — verificada en el texto, no por dicho de terceros |
| **F-4** (≡ CTO-F2) | Eliminar ancla «§K paso 1» | §3.1 ¶1: sustituida por «Este alcance **no coincide con ningún paso completo del plan §K**» + primitive vocabulary explícitamente fuera | **CERRADA** — supera lo pedido |
| **F-3 / DF-1** | Depósito de reportes CTO/CRO en GitHub antes de G4 | §7 DF-1 ampliada con especificación exacta (texto íntegro + dictamen literal + autor + fecha + SHA-256 del artefacto revisado); estado honesto `UNRESOLVED` | **ABIERTA (correctamente)** — el TPL no puede depositarlos; ver punto 11 |
| **F-1** | Clausura exhaustiva de pares + ablación por fila (designadas T-20/T-21 en mi reporte) | §9 íntegro del remediado | **ABIERTA — NO REMEDIADA + COLISIÓN** (puntos 6–9) |

## 6. Adjudicación expresa de la colisión T-20/T-21

1. **Sí** — mi reporte de cierre asignó textualmente: «Añadir como **T-20/T-21** (sin renumerar T-18/T-19 ya asignadas)… T-20 (clausura exhaustiva: todo par ordenado fuera de la whitelist rechazado — enumeración completa) y T-21 (ablación: por cada fila de §5.2, remover cada elemento requerido ⇒ rechazo)». La atribución del CTO es correcta.
2. **Sí, la colisión es real**: la remediación consumió T-20/T-21 para controles distintos (preservación de dictámenes; identidad por hash) y §0.1 los atribuye a «CRO» — una definición que **el CRO nunca emitió**. Esto es R-14 materializado **por segunda vez**: la transcripción sin reportes preservados volvió a perder y esta vez **sustituyó** contenido de una condición CRO.
3. **Sí — la sustancia de F-1 permanece ausente**: en todo el §9 remediado no existe ni la enumeración exhaustiva de pares ni la ablación generalizada por fila.
4. **T-3 sigue siendo muestreo** («saltos de gate y pares no listados» — casos seleccionados, no el producto completo de pares). Muestreo ≠ clausura exhaustiva. **Insuficiente.**
5. **T-13 sigue siendo fuzzing acotado.** Fuzzing ≠ ablación individual de cada elemento obligatorio de cada una de las 14 filas (T-7R cubre ablación solo de los componentes §5C; T-4/T-6 cubren autoridad/evidencia genéricamente, no elemento-por-elemento por fila). **Insuficiente.**
6. **Los controles de preservación son válidos en sustancia** (punto 10) — el conflicto es exclusivamente de numeración/atribución.
7. **La colisión afecta trazabilidad y verificación independiente**: cuando DF-1 deposite mi reporte original, el registro institucional contendría **dos definiciones contradictorias de T-20/T-21 a perpetuidad**; las referencias de G9, §12 (DoD), §7 y R-14 a «T-20/T-21» quedarían ambiguas respecto a qué contenido ratificó el CRO.

## 7–9. Sustancia de F-1 y evaluación de los controles añadidos

**Clausura exhaustiva**: no existe en el artefacto ninguna prueba que enumere todos los pares ordenados aplicables, identifique la whitelist, demuestre aceptación de cada par autorizado y rechazo determinista de todo el resto, ligada a I-2 y G6/G8. **Ausente.** · **Ablación por fila**: no existe prueba que, para cada una de las 14 transiciones, elimine uno a uno cada elemento obligatorio (autoridad, cada pieza de evidencia, registro de verificación cuando aplique) demostrando rechazo. **Ausente.** → **F-1 permanece abierta y requiere nueva edición limitada del TPL.**

**Controles de preservación añadidos (§9.3)** — evaluados en sustancia, no por recomendación del CTO: ambos son controles de riesgo **válidos y ratificables**: campos completos (los nueve), fail-closed genuino («dictamen no preservado = inexistente a efectos de gates»; «hash abreviado jamás aceptado como valor»; mismatch al recomputar ⇒ rechazo), pruebas positivas/negativas/regresión/determinismo, revisor independiente y gate correctos, e incorporación condicionada en G9/DoD correcta («en los términos que el CRO ratifique»). **Ratifico su sustancia condicionada a su renumeración** (punto 8 infra). Operacionalizan CR-4/DF-1 y mitigan directamente R-11/R-14.

## 8 (de la orden). Tratamiento de numeración — determinación CRO

**Procede: renumerar los controles de preservación a T-22/T-23 y restaurar T-20/T-21 con el contenido del reporte CRO original.** Fundamento: el reporte CRO original tiene precedencia temporal y de autoridad sobre esos identificadores; el artefacto remediado aún no es canónico, por lo que su corrección es barata hoy y carísima después de DF-1 (dos definiciones en conflicto en el registro permanente). La alternativa (mantener los del TPL y poner los míos como T-22/T-23) preservaría la trazabilidad solo mediante una nota, dejando el conflicto vivo en el registro. **Especificación exacta para el TPL (autocontenida, para que ninguna transcripción vuelva a perderla):**

- **T-20 — Clausura exhaustiva de pares**: enumerar programáticamente **todos** los pares ordenados (estado_origen, estado_destino) de los vocabularios implementados; identificar la whitelist (las 14 filas de §5.2); demostrar que cada par autorizado con autoridad y evidencia válidas transiciona, y que **cada uno de los restantes pares es rechazado fail-closed**; determinista y reproducible; ligada a I-2; gate G6/G8.
- **T-21 — Ablación por fila**: para **cada una** de las 14 transiciones de §5.2, construir el evento válido de control y derivar variantes eliminando **uno a uno** cada elemento obligatorio (autoridad; cada pieza de evidencia de la fila; registro de verificación §5C donde aplique); cada variante debe ser rechazada; determinista; ligada a I-6/I-14 (y I-4 en `APPROVED→IMPLEMENTED`); gate G6/G8.
- **T-22/T-23**: los actuales controles de §9.3 (preservación de dictámenes; identidad por hash completo), sin cambio de sustancia, con nota de trazabilidad en §9.3 que documente la colisión y la reasignación.
- Actualizar las referencias en §0.1, §7 (DF-1), la nota de T-14 («T-21 prohíbe hashes abreviados» → T-23), G9, §12 (DoD) y R-14.

Esto no sobrescribe controles, no reutiliza identificadores para requisitos distintos, preserva la trazabilidad con el reporte CRO original, no expande el alcance y no toca decisiones de Luis.

## 10–11. DF-1 / H-9 / R-14 — determinación independiente

Verificado directamente: **ningún reporte CTO/CRO está preservado en GitHub** (no existen tales documentos en `main`). Determino: (1) DF-1 **permanece abierto**; (2) **no bloquea este dictamen** — pude cotejar contra mis condiciones originales de sesión, exactamente como instruye la orden; (3) sí permite avance condicionado con **cierre obligatorio antes del Gate 4**; (4) reportes a depositar, **cada uno por su autor**, registrando el SHA-256 completo del artefacto exacto que revisó: CRO `PLAN CONDITIONAL PASS` (sobre `e19245a4…`), CRO `0.4.1-DRAFT CLOSURE CONDITIONAL PASS` (sobre `d6e11b7f…`), este reporte (sobre `ee1759c5…`), y los homólogos CTO (PLAN, CLOSURE y REMEDIATION RE-VERIFICATION); (5–7) evidencia de cierre: documentos resolubles en `main` con dictamen literal, autor, fecha y hash; (8) **sí se requiere orden separada de Luis** para el PR de depósito (todo cambio a `main` exige su autorización). **R-14 debe re-calificarse**: su probabilidad «Baja» quedó refutada dos veces (pérdida de CR-3; colisión T-20/T-21) — Media/Alta mientras DF-1 siga abierto. La colisión de esta remediación es la demostración empírica de por qué DF-1 es condición dura.

## 12. Control del diff

Todos los cambios del diff (176 líneas) pertenecen exclusivamente a: CTO-F1 (§10.1), CTO-F2 (§3.1), CTO-F3 (identidades y hashes completos en cabecera/§2/D9/T-14), CTO-F4 (nota §5.2 — que además **refuerza** la exclusión de §3.1 al confinar `REVISION_REQUIRED` a su documento de origen), T-20/T-21 (§9.3 + referencias G9/DoD/R-14/H-9), DF-1/H-9/R-14 ampliados, y trazabilidad (§0.1, cabecera, dictamen TPL). **Sin expansión material, sin cambios semánticos no autorizados, sin modificación fuera de alcance.** El único defecto es de atribución/numeración (punto 6), no de alcance. El TPL además se abstuvo correctamente de auto-certificar y de fabricar reportes ajenos.

**Separación de autoridades — confirmada:** el TPL no certificó cierres CRO (todo «sujeto a re-verificación»); el CTO no adjudicó definitivamente mi condición (la elevó a adjudicación CRO — correcto); yo no edito el paquete ni decido por Luis; y las diez desigualdades de la orden (aprobación técnica ≠ implementación; riesgo ≠ capital; merge ≠ activación; tag ≠ autoridad; silencio ≠ aprobación; etc.) permanecen íntegras en §10.2/§5A/§16 del artefacto.

## 13–19. Hallazgos materiales

| ID | Severidad | Hallazgo | Componente | Condición/test | Gate | Consecuencia | Responsable | ¿Regresa al TPL? |
|---|---|---|---|---|---|---|---|---|
| **RF-1** | **MATERIAL — impide PASS** | Sustancia de F-1 ausente + colisión de identificadores T-20/T-21 (evidencia: §9 remediado; mi F-1 original; §0.1 atribuye al CRO definiciones no emitidas) | §9, §0.1, G9, DoD, R-14 | F-1 / I-2, I-6, I-14 / T-20, T-21 | G3 | El paquete no puede ratificarse; dos definiciones en conflicto entrarían al registro permanente | TPL (edición limitada per especificación del punto 8) | **Sí** |
| **RF-2** | CONDITION | DF-1 abierto; R-14 materializado dos veces; probabilidad a re-calificar | §7, §13, §15 | F-3 / T-22 (preservación) | Antes de G4 | Sin depósito, cada ciclo de transcripción arriesga nueva pérdida | Autores (CTO, CRO) + Luis (orden y merge del PR de depósito) | No |
| RF-3 | NO BLOQUEANTE | Ratificación CRO de los controles de preservación: **otorgada en sustancia**, condicionada a renumeración T-22/T-23 | §9.3 | — | G3 | — | TPL (numeración) | Con RF-1 |

**Riesgos residuales:** R-14 en Media/Alta hasta DF-1; el resto de residuales del registro permanecen válidos.

## 20. Estado institucional final

Reconfirmado idéntico al del punto 2 — ninguna variable cambió. No modifiqué archivos, no reparé el paquete, no deposité reportes, no creé código/tests/ramas/commits/PRs/tags, no canonizé el draft, no ejecuté funciones TPL/CTO, no resolví L-1…L-10.

## 21. Dictamen CRO exacto

# `CRO SPRINT 7 0.4.1-DRAFT REMEDIATION REQUIRES REVISION`

La remediación cerró correctamente F-2 y F-4, avanzó honestamente DF-1 y añadió dos controles de preservación válidos en sustancia — pero **la condición central del CRO (F-1) regresó sin remediar y con sus identificadores consumidos por contenido distinto**. Fail-closed: el incumplimiento de una condición obligatoria no se convierte en condición nuevamente aplazable. El paquete debe regresar al TPL mediante orden separada y estrictamente limitada a: (a) restaurar T-20/T-21 con el contenido del reporte CRO original (especificación autocontenida en el punto 8), (b) renumerar los controles de preservación a T-22/T-23 con nota de trazabilidad, y (c) actualizar las referencias cruzadas. **Recomendación de secuencia para evitar una tercera pérdida por transcripción: cerrar DF-1 (depósito de los reportes CTO/CRO, con orden de Luis) antes o junto con la próxima edición TPL.**

Este dictamen no autoriza Sprint 7, implementación, canonización, activación, señales, operaciones, capital ni decisión alguna L-1…L-10.

Me detengo aquí.

<!-- END ORIGINAL DICTAMEN TEXT -->
