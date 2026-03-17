---
name: optimize-code
description: Optimize Stata dofiles for performance through mechanical substitutions, structural improvements, and code compactness. Use when user asks to optimize code or improve performance.
disable-model-invocation: false
argument-hint: [path-to-dofiles-directory]
---

# CRITICAL WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES. THEY ARE NON-NEGOTIABLE.**

**Work modularly.** Complete one dofile at a time. After each dofile, report the required output and wait for confirmation before proceeding.

**Be explicit about confidence.** Every suggestion must include a confidence tag as defined in the Confidence Levels section below. If you cannot confidently explain *why* something is faster, do not suggest it.

**Report only actionable changes.** If code is already efficient for its purpose, say nothing about it. Never describe what you reviewed. Never explain that something is "already optimal."

**Do not break correctness for speed.** If an optimization could change results in any edge case — different sort order, floating-point precision, handling of missing values, treatment of duplicates — you must flag this explicitly. Note that even commands labeled "behaviorally identical" may have subtle differences in edge cases (e.g., string length limits, numeric precision, treatment of extended missing values).

**Only audit `.do` files.** Ignore all other file types in the folder (`.R`, `.py`, `.txt`, `.csv`, `.md`, etc.). If a folder contains a mix of file types, only process files with the `.do` extension.


## Confidence Levels

Every suggestion must include a confidence tag according to this table:

| Level | Meaning | Rule |
|---|---|---|
| `[HIGH]` | Drop-in replacement, well-documented, no behavioral change | Always include |
| `[MEDIUM]` | Likely faster, but depends on data size or structure; minor behavioral differences possible | Include with risk flag |
| `[LOW]` | Speculative or context-dependent; requires careful testing | Include only if you can clearly explain the trade-off |

**When in doubt, leave it out.** A missed optimization is harmless. A broken suggestion wastes your time.

**Dataset Size Inference (since you cannot run the code):**

You must infer dataset size from contextual clues:

- **Clearly small datasets**:
  - Metadata files, crosswalks, lookup tables (often in filename)
  - Hand-built data (visible in code: small number of manual `input` commands or hardcoded values)
  - Aggregated summary statistics files
  - Files with names like "xwalk", "meta", "lookup", "codebook"
  - → **Skip optimization suggestions** for these

- **Clearly large datasets**:
  - Administrative data (DADS, FICUS, FARE, tax records, social security data)
  - Panel data spanning many firms/years/workers
  - Patent databases, transaction-level data
  - Files that are loaded from "rawdata" folders with institutional names
  - → **Suggest optimizations** for these

- **Uncertain size**:
  - If you cannot determine size from context, **default to suggesting the optimization** and flag confidence as [MEDIUM] rather than [HIGH]


## CRITICAL: Stata Syntax Limitations

**Before suggesting ANY optimization, verify that the Stata syntax actually exists and works as described.**

Common mistakes to NEVER make:

1. **`append using` takes only ONE filename at a time.** There is NO way to append multiple files in a single command. You MUST loop sequentially or use the first file with `use`, then append the rest.

   **WRONG (this syntax does NOT work):**
   ```stata
   local files "file1 file2 file3"
   append using `files'  // DOES NOT WORK IN STATA
   ```

   **CORRECT:**
   ```stata
   use "file1", clear
   foreach f in file2 file3 {
       append using "`f'"
   }
   ```

   **NEVER suggest "consolidating sequential appends into a single append" - this is IMPOSSIBLE in Stata.**

2. **`merge` takes only ONE filename in the using clause.** Cannot merge multiple files at once.

3. **DO NOT suggest "consolidating" sequential file operations unless you can provide exact, working Stata syntax.** If you cannot write the exact code that would execute correctly in Stata, do not suggest the optimization.

**When in doubt about Stata syntax, DO NOT suggest the optimization. A wrong suggestion that breaks code is infinitely worse than missing an optimization opportunity.**


# Code Optimization

I want you to go through the dofiles and suggest performance improvements.

**CRITICAL WORKFLOW:** Process **ONE dofile at a time**, completing all three modules for that dofile before moving to the next dofile.

For each dofile, complete all three modules:

- **Module 1**: Mechanical substitutions — a fixed checklist of safe, well-known replacements.
- **Module 2**: Structural optimizations — improvements to the logic or flow of the code that reduce runtime or memory usage.
- **Module 3**: Code compactness — consolidating repetitive code into cleaner, shorter structures.

After completing all three modules for one dofile, **STOP** and wait for approval before proceeding to the next dofile.


## IMPORTANT: Stop-and-Check Points

Throughout this project, there are mandatory **STOP AND CHECK** points. At each of these points, you must:

1. Summarize what you have completed
2. Present key outputs for review
3. List any issues or concerns
4. **Wait for human approval before proceeding**

Do not proceed past a STOP checkpoint without explicit approval.


---

## Module 1: Mechanical Substitutions

Go through each dofile and apply the following checklist. These are **safe, drop-in replacements** where the gtools/ftools equivalent is strictly faster and behaviorally identical.

### Substitution Checklist

| Base Stata Command | Faster Replacement | Notes |
|---|---|---|
| `egen` | `gegen` | Drop-in replacement for all `egen` functions supported by `gegen` |
| `collapse` | `gcollapse` | Identical syntax |
| `contract` | `gcontract` | Identical syntax |
| `duplicates` | `gduplicates` | Identical syntax |
| `levelsof` | `glevelsof` | Identical syntax |
| `isid` | `gisid` | Identical syntax |
| `xtile` | `fasterxtile` or `gquantiles` | Check syntax compatibility |
| `reshape` | `greshape` | Mostly identical; flag if using advanced reshape options |
| `encode` | `sencode` (from `egenmore`) | Only for clearly large datasets (see inference guidelines) |
| `tabulate ..., gen()` | `flevelsof` + manual dummies | Rarely beneficial; only if context suggests very many levels |
| `sort` followed by operation | Check if `hashsort` is faster | Only for clearly large datasets (see inference guidelines); `sort` is fine otherwise |
| `merge` | **NEVER REPLACE WITH `fmerge`** | `fmerge` is far less versatile and can break code in many cases |

**Scope restriction:** Only flag substitutions from this checklist. Do not invent other mechanical substitutions.

### What NOT to flag in Module 1

- Commands that have no gtools/ftools equivalent
- Cases where the dataset is clearly small (e.g., a metadata file, a crosswalk, a hand-built lookup table — see inference guidelines) — speed gains are negligible
- `merge` operations on clearly small files
- `sort` operations that precede `by:` operations (Stata requires this; `hashsort` would not help here unless the dataset is clearly large)

### Output format for Module 1

For the current dofile being optimized, present substitutions with numbered labels for easy reference.

**Module 1 — Mechanical Substitutions: filename.do**

If substitutions exist, list them with labels **M1, M2, M3**, etc.:

**M1** (Line 45) `[HIGH]`

**Current:**
```stata
egen group_mean = mean(x), by(g)
```

**Suggested:**
```stata
gegen group_mean = mean(x), by(g)
```


**M2** (Line 78) `[HIGH]`

**Current:**
```stata
collapse (mean) x, by(group)
```

**Suggested:**
```stata
gcollapse (mean) x, by(group)
```

If no substitutions exist, write: **"No mechanical substitutions."**


---

## Module 2: Structural Optimizations

### What to look for

Only flag structural optimizations that fall into the following categories:

**Category A — Redundant operations `[HIGH confidence expected]`**
- Unnecessary `sort` commands (data is already sorted from a prior operation)
- Unnecessary `preserve` / `restore` blocks (where a `tempfile` or restructuring avoids the need)
- Repeated `merge` or `joinby` operations that could be combined
- Dropping variables late that could be dropped early (reducing memory footprint)
- Loading an entire dataset when only a few variables are needed (suggest `use varlist using`)

**Category B — Loop inefficiencies `[HIGH confidence expected]`**
- Loops that grow a dataset row by row (suggest `post` / `postfile` or pre-allocation)
- Loops that run a command on subsets when a `by` prefix or `bysort` would work
- Loops over `levelsof` that could be replaced with a `by:` operation
- Repeated file I/O inside loops (loading/saving the same file multiple times)

**Category C — Merge and reshape logic `[MEDIUM confidence expected]`**
- Multiple sequential reshapes that could be consolidated
- **NOTE:** Do NOT suggest consolidating multiple `append using` statements into a single operation - this is syntactically impossible in Stata (see Stata Syntax Limitations section above)

### What NOT to flag in Module 2

- Adding `compress` before `save` — stylistic preference
- Adding `quietly` or `noisily` — verbosity is not a performance issue
- Adding comments or documentation
- Rewriting code for readability alone — only flag if readability changes also improve performance
- Anything that would require installing packages beyond `gtools`, `ftools`, `reghdfe`, `estout`, `binscatter`, and standard SSC packages
- **Sequential `append using` or `merge` operations that cannot be consolidated due to Stata syntax limitations** (see Stata Syntax Limitations section above)

### Output format for Module 2

Organize findings by category. For each category that has findings, include the category header once, then list all findings.

**Module 2 — Structural Optimizations: filename.do**

### **Category A — Redundant operations**

**A1** (Line 45) `[HIGH]`

**Current:**
```stata
[code snippet showing the issue]
```

**Suggested:**
```stata
[optimized code]
```

**Why it is faster:** [one sentence explaining the mechanism - fewer disk operations, reduced memory, vectorized vs. loop, etc.]

**Risk flag:** [if applicable, note any edge case where behavior might differ]


**A2** (Line 78) `[HIGH]`

**Current:**
```stata
...
```

**Suggested:**
```stata
...
```

**Why it is faster:** [explanation]

### **Category B — Loop inefficiencies**

**B1** (Line 120) `[HIGH]`

[same format as above]

### **Category C — Merge and reshape logic**

[same format as above]

**If a category has no findings, omit the category header entirely.**

### Before submitting Module 2 for this dofile

**STOP. Before proceeding to Module 3, validate every item:**

Go through EVERY numbered item (A1, A2, B1, etc.) you drafted. Delete any item where:
- The "Suggested" code is identical to the "Current" code → DELETE IMMEDIATELY
- You wrote "no change needed", "this is fine", "already optimal" → DELETE IMMEDIATELY
- You cannot articulate in one sentence WHY it is faster → DELETE IMMEDIATELY
- You are explaining why existing code is already correct → DELETE IMMEDIATELY

**Only include items that make the code measurably faster. The user doesn't want a list of things you checked.**

**After completing Module 2, immediately proceed to Module 3 for this same dofile. Do NOT stop between modules for a single dofile.**


### CRITICAL: Maintaining Consistency Based on User Feedback

**If you provide ANY corrections, clarifications, or modifications at any stop point, I MUST apply those same corrections/modifications consistently to ALL remaining dofiles.**

This includes but is not limited to:

- **False positive corrections**: If you say "that substitution doesn't actually help here," I must not suggest it in similar contexts later
- **Confidence overrides**: If you say "that's not really [HIGH], treat it as [MEDIUM]," I must recalibrate for all future dofiles
- **Category exclusions**: If you say "don't flag Category X anymore," I must skip it entirely going forward
- **Context clarifications**: If you tell me a dataset is small, I must not suggest large-data optimizations for that dataset in other dofiles
- **Package restrictions**: If you say "I don't use package X," I must stop suggesting it

**Before each new dofile, I must review all prior feedback and ensure consistency.**

**I must NEVER flag the same issue type again after you have indicated it should not be flagged.**


---

## Module 3: Code Compactness

### Purpose

This module is **not about speed**. It is about making code shorter, cleaner, and easier to maintain by eliminating unnecessary repetition.

### What to look for

### **CRITICAL: NEVER Loop Over Pairwise Mappings**

**IF YOU SEE A PATTERN WHERE EACH LINE MAPS ONE VALUE TO ANOTHER VALUE (A → B), DO NOT SUGGEST A LOOP. PERIOD.**

This is the #1 most common mistake. When code establishes pairwise relationships between two distinct values, the sequential structure is ALWAYS clearest. Do NOT try to "optimize" these with loops, parallel lists, or tokenization.

**NEVER suggest loops for these patterns:**

1. **Time-series lookup tables:**
   ```stata
   replace wage_min = 4860/6.56 if year==1988
   replace wage_min = 4961/6.56 if year==1989
   replace wage_min = 5156/6.56 if year==1990
   ```
   Each line = empirical data point. Sequential structure shows "year → value" directly.

2. **Classification crosswalks:**
   ```stata
   replace naf2008 = "0113Z" if naf2003=="011A"
   replace naf2008 = "0149Z" if naf2003=="012J"
   replace naf2008 = "0161Z" if naf2003=="011C"
   ```
   Each line = one mapping in the crosswalk. Direct visibility of transformations.

3. **Arbitrary recoding:**
   ```stata
   replace code="0110" if code=="011A"
   replace code="0117" if code=="011D"
   replace code="0150" if code=="013Z"
   ```
   Each line = one specific transformation. Easy to verify and modify.

**Why sequential is better:** When you need to track TWO distinct values together (input + output), any loop requires parallel lists, tokenization, or position counting. This creates cognitive overhead and makes errors harder to spot.

**The ONLY exception:** Multiple inputs → SAME output:
```stata
replace code = "X" if inlist(code, "A", "B", "C")  // ✓ This is good - consolidates to show "these all become X"
```

**Before suggesting ANY loop in Category D:** Ask yourself: "Does each line establish a relationship between two distinct values?" If yes, DO NOT suggest a loop.

---

**Category D — Repetitive operations that should be loops `[HIGH confidence expected]`**
- A command (e.g., `gen`, `replace`, `rename`, `label`, `recode`) repeated multiple times with only a systematic variation (different variable names, different values, different suffixes)
- Repeated `merge` or `append` calls on files that follow a naming pattern
- Repeated regression or estimation commands that differ only in the dependent variable, sample restriction, or a single option
- Copy-pasted blocks that differ in only one or two tokens

**IMPORTANT EXCEPTION for replacement/recoding operations:**
- **DO NOT suggest looping when the mappings are arbitrary** (e.g., recoding industry codes, country codes, or any lookup table)
- Example of what NOT to flag:
  ```stata
  replace ape="0110" if ape=="011A"
  replace ape="0117" if ape=="011D"
  replace ape="0150" if ape=="013Z"
  ```
  This should NOT be converted to a loop with parallel lists. Why?
  - Direct mapping visibility: each line clearly shows input → output
  - Easy to verify, modify, and debug
  - No need to count positions in parallel lists
  - The sequential structure IS the clearest form for arbitrary mappings
- **HOWEVER**, DO flag when multiple conditions map to the SAME value. Example:
  ```stata
  replace ape="271Y" if ape=="271Z"
  replace ape="271Y" if ape=="273J"
  replace ape="282C" if ape=="282A"
  replace ape="282C" if ape=="282B"
  ```
  Should become:
  ```stata
  replace ape="271Y" if inlist(ape, "271Z", "273J")
  replace ape="282C" if inlist(ape, "282A", "282B")
  ```
  This consolidation is clearer because it shows "these inputs all map to the same output"
- Only suggest loops when there's a SYSTEMATIC pattern (e.g., applying same transformation to multiple variables, not when values are arbitrary mappings)

**Category E — Verbose constructs that have compact equivalents `[HIGH confidence expected]`**
- Multiple `gen` + `replace` pairs that could be a single `gen` with a `cond()` or nested `cond()`
- Multiple `replace X = ... if group == "A"` lines that could be `recode` or a single `gen` with `cond()`
- Sequential `rename` commands that could be a single `rename` with a pattern (e.g., `rename (var1 var2 var3) (new1 new2 new3)`) — BUT ONLY when variable names are completely different, NOT when adding/removing systematic prefixes or suffixes
- Sequential `label variable` commands that could use a loop
- Multiple `drop` or `keep` commands that could be consolidated into one
- Sequential `destring` commands that could be a single `destring varlist`
- `inlist()` conditions spread across multiple `if` / `else if` lines

**Category F — Macro and local patterns `[MEDIUM confidence expected]`**
- Hardcoded values repeated throughout the dofile that should be stored in a local macro once
- Long varlist repeated verbatim in multiple commands that should be stored in a local macro

### What NOT to flag in Module 3

- Code that is repeated only 2 times — the loop overhead is not worth it for just 2 repetitions. **Flag only 3+ repetitions.**
- Repetitive code where each instance has complex, non-systematic differences — if the loop would require many conditionals inside it, the loop is not cleaner
- Cases where the repetitive structure actually aids readability (e.g., a short block of 3 `label define` commands that is clearer written out than looped)
- Do not suggest consolidation that would make the code harder to debug
- **Loops that add/remove prefixes or suffixes systematically** — DO NOT suggest replacing these with pattern-based renames. For example:
  ```stata
  foreach var in emp ta sal va ebe {
      rename `var' `var'_
  }
  ```
  This loop is CLEARER than `rename (emp ta sal va ebe) (emp_ ta_ sal_ va_ ebe_)` because:
  - The transformation pattern is immediately obvious
  - Adding/removing variables requires changing the list only once
  - More maintainable and less error-prone
- Pattern-based `rename` should ONLY be suggested when variable names are completely different with no systematic relationship
- **Sequential replace statements for arbitrary mappings** — DO NOT suggest converting to loops with parallel lists. For example:
  ```stata
  replace code="0110" if code=="011A"
  replace code="0117" if code=="011D"
  replace code="0150" if code=="013Z"
  ```
  This should NOT be converted to a loop. The sequential structure is CLEARER because:
  - Direct visibility: each line shows the exact mapping
  - Easy to verify, modify, and debug any specific mapping
  - No need to count positions in parallel lists to understand transformations
  - This applies to: industry code recoding, country code mapping, any lookup table transformations
- **HOWEVER**, within such sequential mappings, DO flag when multiple conditions map to the SAME replacement value:
  ```stata
  replace code="271Y" if code=="271Z"
  replace code="271Y" if code=="273J"
  ```
  Should be consolidated to:
  ```stata
  replace code="271Y" if inlist(code, "271Z", "273J")
  ```
  This is clearer and shows "these inputs all map to the same output"

### Output format for Module 3

Organize findings by category. For each category that has findings, include the category header once, then list all findings.

**Module 3 — Code Compactness: filename.do**

### **Category D — Repetitive operations that should be loops**

**D1** (Lines 45–78) `[HIGH]`
*Pattern:* Same `gen ... if` structure repeated 8 times across different industries

**Current:**
```stata
[first instance]
...
[last instance]
```

**Suggested:**
```stata
[compact version]
```


**D2** (Lines 90–110) `[HIGH]`
*Pattern:* [description]

**Current:**
```stata
[code]
```

**Suggested:**
```stata
[code]
```

### **Category E — Verbose constructs that have compact equivalents**

**E1** (Lines 120–135) `[HIGH]`
*Pattern:* [description]

**Current:**
```stata
[code]
```

**Suggested:**
```stata
[code]
```


**E2** (Lines 140–150) `[HIGH]`
*Pattern:* [description]

**Current:**
```stata
[code]
```

**Suggested:**
```stata
[code]
```

### **Category F — Macro and local patterns**

**F1** (Lines 150, 160, 170) `[MEDIUM]`
*Pattern:* [description]

**Current:**
```stata
[code]
```

**Suggested:**
```stata
[code]
```


**F2** (Lines 180, 190, 200) `[MEDIUM]`
*Pattern:* [description]

**Current:**
```stata
[code]
```

**Suggested:**
```stata
[code]
```

**If a category has no findings, omit the category header entirely.**

### Before submitting Module 3 for this dofile

Re-read each item. Delete any item where:
- The suggested replacement is longer or equally long as the original
- The loop or consolidation would require complex conditionals that defeat the purpose
- The repetition count is fewer than 3
- **The replace statements establish pairwise mappings (A → B transformations) such as:**
  - Time-series data: year → value, period → rate, date → parameter
  - Classification crosswalks: old_code → new_code
  - Lookup tables: input_value → output_value
  - ANY pattern where each line maps one distinct value to another distinct value
- **You would need parallel lists, tokenization, or position counting to implement the loop**

### FINAL VALIDATION CHECKLIST

**STOP. Before presenting ANY findings, perform this validation:**

Go through EVERY numbered item (M1, M2, A1, A2, D1, D2, E1, etc.) you drafted and check:

1. **Does it have DIFFERENT code in "Suggested" vs "Current"?**
   - NO → DELETE THE ENTIRE ITEM IMMEDIATELY

2. **Did I write any phrase like: "no change needed", "already correct", "this is fine", "already optimal"?**
   - YES → DELETE THE ENTIRE ITEM IMMEDIATELY

3. **Am I explaining why existing code is already good?**
   - YES → DELETE THE ENTIRE ITEM IMMEDIATELY

4. **Would implementing this suggestion make the code SHORTER or FASTER?**
   - NO → DELETE THE ENTIRE ITEM IMMEDIATELY

**If you cannot confidently answer "this makes the code better" for an item, DELETE IT.**

**NEVER present an item to explain that code is already correct. The user doesn't need a list of things you checked.**

---

### MANDATORY STOP AFTER COMPLETING ALL THREE MODULES FOR ONE DOFILE

After completing **Modules 1, 2, and 3** for ONE dofile:

1. Present a consolidated report with all findings from all three modules
2. **STOP COMPLETELY**
3. **WAIT for my response**
4. **DO NOT proceed to the next dofile** until I explicitly say **"next"**

**Any other response from me (including "ok", "yes", "thanks", "I understand", corrections, or questions) is NOT permission to proceed.** Stay on the current dofile and respond to my input.

When you stop, always write:

```
STOPPED — AWAITING YOUR INPUT

Completed optimization for: [filename.do]
- Module 1: X mechanical substitutions
- Module 2: Y structural optimizations
- Module 3: Z compactness improvements

You may:
- Tell me which suggestions to implement (e.g., "implement M1, A2, D3")
- Say "next" to proceed to the next dofile
```


### CRITICAL: Maintaining Consistency Based on User Feedback

All feedback rules from Module 2 apply identically here. Additionally:

- If you indicate that a particular repetitive pattern is intentional or preferred expanded, I must not flag the same pattern in other dofiles
- If you set a higher threshold for repetitions (e.g., "only flag 5+"), I must apply it throughout


ARGUMENTS: {args}
