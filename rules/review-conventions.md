# General Rules for All Modules

## How to write the audit

- **Think first, write second.** Before writing ANY suggestion, verify it is an actual problem requiring a change.
- **Never withdraw or revise suggestions mid-response.** If you write a suggestion and then realize it's not valid, you have already failed. Do not write "I withdraw this" or "actually this is fine" — those phrases should never appear.
- **Each suggestion you write is final.** If you are unsure whether something is a problem, do not include it.

## What NOT to include in the audit

- **Only report actual problems or changes needed.** Do NOT list things that are already correct.
- Do NOT say things like "this sentence is fine" or "no change needed here"
- If the text is fine, do not mention it at all
- Every item in your audit should be something that requires action or a decision from me
- **NEVER describe your review process.** Do not say "I checked X and it was fine" or "After reviewing, I found no issues with Y"

## Technical terms and jargon

Economics and finance papers use field-specific terminology. Do NOT flag as errors:

- Standard econometric terms (heteroskedasticity, endogeneity, etc.)
- Financial terms (yield spread, basis points, etc.)
- Variable names and notation
- Standard abbreviations (OLS, IV, GMM, CAPM, etc.)

If you are unsure whether something is a technical term, do not flag it.

## Consistency rule

When you find ANY error, immediately search the entire document for:

1. The exact same error elsewhere
2. The same pattern applied to different words (e.g., if you find one subject-verb disagreement, re-check ALL subject-verb pairs; if you find "Earning" should be "Earnings", check ALL similar words throughout)

This prevents inconsistent corrections and missed duplicates.

## Second-pass requirement

After completing your first pass through Modules 1 and 2, do a second pass through the entire document applying the systematic checks described above. The first pass catches obvious errors; the second pass catches errors that require careful grammatical analysis.

## Context management and `/clear`

**General principle:** Avoid `/clear` mid-task when accumulated context matters (e.g., building code incrementally, tracking decisions across a project). However, use `/clear` strategically between completed phases when:

1. **All work is saved to disk** - The files carry the complete state
2. **No conversation history is needed** - Previous context isn't required for the next phase
3. **Fresh attention improves quality** - A clean context window catches things that pattern-matching would miss

**For paper auditing specifically:** Use `/clear` between module groups (after Modules 1–2, after Module 3) to give each phase fresh context. The paper files on disk preserve all corrections, so no state is lost.

**For incremental building:** Do NOT use `/clear` while building features, refactoring code, or making connected changes where later work depends on understanding earlier decisions.
