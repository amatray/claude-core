# Replication Guidelines

## Applicability

**This rule applies whenever:**
- User asks to "replicate" or "reproduce" tables/figures from a paper
- Working directory is under `~/claude-workflows/replications/`
- User mentions verifying results from a publication
- User asks to check if results match a paper

**Key phrases that trigger this rule:**
- "replicate this paper"
- "reproduce Table X"
- "verify the results"
- "check if this matches the paper"
- "we're replicating [Author Year]"

---

## ⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔
## 🚨 MANDATORY FIRST ACTIONS - DO THIS BEFORE ANYTHING ELSE 🚨
## ⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║                                                                       ║
# ║  STOP. DO NOT READ CODE. DO NOT RUN ANYTHING.                        ║
# ║  DO NOT EXTRACT TARGETS. DO NOT START REPLICATION.                   ║
# ║  DO NOT ASSUME ANYTHING ABOUT DATA AVAILABILITY.                     ║
# ║                                                                       ║
# ║  STEP 1: READ THE PAPER AND IDENTIFY ALL TABLES/FIGURES              ║
# ║                                                                       ║
# ║  Use pdf-chunker skill (NOT Read tool) on paper PDF.                 ║
# ║  Create a numbered inventory showing ALL tables and figures.         ║
# ║                                                                       ║
# ║  STEP 2: STOP AND ASK USER WHICH ITEMS TO REPLICATE                 ║
# ║                                                                       ║
# ║  Present inventory and ask:                                          ║
# ║  "I found X tables and Y figures in the paper. Which would you       ║
# ║   like me to replicate?                                              ║
# ║                                                                       ║
# ║   You can select:                                                    ║
# ║   - '2, 6' to replicate specific items by number                     ║
# ║   - 'all main' to replicate all HIGH priority items                  ║
# ║   - '1-4' to replicate a range                                       ║
# ║   - 'all' to replicate everything"                                   ║
# ║                                                                       ║
# ║  STEP 3: ONLY AFTER USER SELECTS, EXTRACT TARGETS                   ║
# ║                                                                       ║
# ║  Extract gold standard numbers from paper ONLY for selected items.   ║
# ║  Create targets/ files for selected items only.                      ║
# ║                                                                       ║
# ║  STEP 4: VERIFY ALL DATASETS EXIST BEFORE EXECUTING                 ║
# ║                                                                       ║
# ║  Create data inventory table showing:                                ║
# ║  - Dataset name                                                      ║
# ║  - Time period covered                                               ║
# ║  - Whether it exists in replication package (Yes/No)                 ║
# ║                                                                       ║
# ║  If ANY dataset is missing: HARD STOP                                ║
# ║  Ask user: "I found that [X] datasets are missing from the           ║
# ║  replication package. Do you already have these data files?          ║
# ║  If yes, where are they located? If not, I can help you              ║
# ║  identify how to obtain them."                                       ║
# ║                                                                       ║
# ║  STEP 5: EXECUTE REPLICATION FOR SELECTED ITEMS ONLY                ║
# ║                                                                       ║
# ║  Run/translate code to generate ONLY the selected outputs.           ║
# ║                                                                       ║
# ║  IF YOU SKIP STEPS 2 OR 4, YOU HAVE WASTED THE ENTIRE SESSION.      ║
# ║  DO NOT EXTRACT TARGETS BEFORE USER SELECTS ITEMS.                   ║
# ║  DO NOT START REPLICATION BEFORE USER SELECTS ITEMS.                 ║
# ║  DO NOT RUN CODE BEFORE VERIFYING ALL DATA EXISTS.                   ║
# ║                                                                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝

**IF YOU ARE READING THIS AND HAVE ALREADY STARTED WITHOUT FOLLOWING STEPS 1-4, STOP IMMEDIATELY. ACKNOWLEDGE THE ERROR AND START OVER.**

---

## Critical Rules

### 1. PDF Handling

**NEVER USE THE READ TOOL ON PDF FILES.**

Large PDFs will fill your entire context window and cause session failure.

**MANDATORY APPROACH:**
- Use the `pdf-chunker` skill (invoke with Skill tool)
- OR explicitly ask user how to proceed before touching any PDF

### 2. Data Availability Check

**NEVER ASSUME DATA EXISTS OR IS ACCESSIBLE.**

Before running any code or downloading anything:

1. **Ask user explicitly:**
   - "Do you have the raw data files?"
   - "Where are they located?"
   - "Are all required datasets accessible?"

2. **Check symlinks and paths:**
   - If you see symlinks in `original/` directory, verify they point to real files
   - Test with `ls -lh` or `file` commands before trying to load data
   - Report broken symlinks immediately

3. **Document data sources:**
   - Where each dataset comes from
   - How to obtain it if missing
   - Expected file sizes and formats

**If data is missing:** Help user identify what's needed and where to get it BEFORE proceeding.

### 3. Scope Selection

**NEVER REPLICATE EVERYTHING BY DEFAULT.**

Users typically want a subset of results. Wasting time on unrequested items is inefficient.

**MANDATORY PROCESS:**
1. Read paper and create inventory of ALL available items
2. Assign priority levels:
   - **HIGH:** Main results, key figures, primary specifications
   - **Medium:** Robustness checks, heterogeneity, mechanisms
   - **Low:** Summary stats, balance tables, appendix items
3. Present inventory to user with priority levels
4. Wait for explicit selection before extracting targets
5. Only work on selected items

### 4. Phase Boundaries

**STOP AND ASK FOR APPROVAL AT EACH PHASE:**

- **After Phase 1 (Inventory):** "Ready to proceed to execution?"
- **After Phase 2 (Execute):** "Ready to proceed to verification?"
- **When encountering blockers:** Report and ask how to proceed

Do not silently continue through all phases without user checkpoints.

---

## Three-Phase Protocol

### Phase 1: Inventory & Selection

1. **Use pdf-chunker** to read paper PDF
2. **Scan for all tables and figures**
3. **Create inventory table:**

```
| # | Item     | Description              | Page | Priority |
|---|----------|--------------------------|------|----------|
| 1 | Table 1  | Summary statistics       | 12   | Low      |
| 2 | Table 2  | Main results             | 15   | HIGH     |
| 3 | Figure 1 | Event study              | 16   | HIGH     |
```

4. **Ask user to select items**
5. **Extract targets ONLY for selected items**
6. **Update PROJECT.md** with replication scope
7. **STOP and get approval before Phase 2**

### Phase 2: Execute

#### Step 4A: Create Data Inventory (MANDATORY - HARD STOP IF DATA MISSING)

**Before running ANY code, create a comprehensive data inventory table.**

1. **Read the paper** (data section, footnotes, online appendix)
2. **Read original code** (if available) to identify all data files used
3. **Create data inventory table:**

```
| Dataset                        | Period        | In Replication Package? |
|--------------------------------|---------------|-------------------------|
| Compustat Annual               | 1990-2010     | No                      |
| CRSP Daily Returns             | 1990-2010     | No                      |
| Federal Reserve H15 rates      | 1990-2010     | Yes                     |
| Hand-collected merger data     | 2005-2008     | No                      |
```

4. **Check replication package** for each dataset:
   - Look in `original/data/` or similar directory
   - Verify symlinks actually point to existing files (use `ls -lh` or `file`)
   - Check file sizes (>0 bytes)
   - Mark as "Yes" only if file exists and is accessible

5. **IF ANY DATASET SHOWS "No": HARD STOP**

   Present the data inventory table to user and ask:

   ```
   "I've identified the following datasets required for replication:

   [Show data inventory table]

   The following datasets are MISSING from the replication package:
   - Compustat Annual (1990-2010)
   - CRSP Daily Returns (1990-2010)
   - Hand-collected merger data (2005-2008)

   Do you already have these data files? If yes, please tell me where
   they are located. If not, I can help you identify how to obtain them."
   ```

6. **WAIT for user response** - do NOT proceed until all data is confirmed available

#### Step 4B: Execute Code (only after data verification)

1. **Run/translate code** for selected items only
2. **Save outputs** to `output/` folder
3. **Match original specifications exactly** - no improvements
4. **STOP and present outputs before Phase 3**

### Phase 3: Verify

1. **Compare outputs to targets** for selected items
2. **Apply tolerance thresholds:**
   - N (sample size): Exact match required
   - Coefficients: < 0.01 difference acceptable
   - Standard errors: < 0.05 difference acceptable
   - P-values: Same significance level required
3. **Generate verification report**
4. **DONE - present final report to user**

---

## Common Mistakes to Avoid

❌ **Starting replication without asking which items to replicate**
- Wastes time on unwanted tables/figures
- User only wanted 2 items, you replicated 20

❌ **Running code before verifying all data exists**
- Code fails halfway through
- Discover missing data after hours of work
- **ALWAYS create data inventory table BEFORE running any code**

❌ **Assuming data files exist and are accessible**
- Symlinks may be broken
- Files may need to be downloaded
- Paths may be machine-specific

❌ **Using Read tool on PDF files**
- Fills context window
- Causes session to fail
- Always use pdf-chunker skill instead

❌ **Continuing silently when code fails**
- Missing data → Report immediately, don't try to download without asking
- Broken dependencies → Ask user, don't install without permission
- Wrong results → Stop and investigate, don't keep going

❌ **Improving or modernizing code during replication**
- First replication must match original exactly
- Improvements come later, after verification

---

## Project Structure

```
~/claude-workflows/replications/author-year-journal/
├── .claude/
│   └── PROJECT.md              # Project-specific context
├── paper/                       # Paper PDF (REQUIRED)
│   └── paper.pdf
├── original/                    # Original replication package
│   ├── data/                    # (may be empty, symlinks, or actual data)
│   ├── code/
│   └── results/
├── targets/                     # Gold standard (selected items only)
│   ├── table2_targets.csv
│   └── figure1_targets.csv
├── translated/                  # Your code
│   ├── 01_clean_data.R
│   └── 02_analysis.R
├── output/                      # Your results (selected items only)
│   ├── tables/
│   └── figures/
├── verification/                # Comparison reports
│   └── replication_report.md
├── DATA_INVENTORY.md           # List of all required datasets
├── REPLICATION_LOG.md          # Progress tracking
└── README.md
```

---

## When Resuming Work

**If user is returning to an existing replication project:**

1. **Check if REPLICATION_LOG.md exists** and read it first
2. **Check PROJECT.md** for selected items and current phase
3. **Check DATA_INVENTORY.md** to see which datasets were identified
4. **Verify data availability** hasn't changed
5. **Continue from last checkpoint**, not from scratch

---

## Summary Checklist

At start of ANY replication task:

- [ ] Step 1: Use pdf-chunker to read paper
- [ ] Step 2: Create inventory and ask user which items to replicate
- [ ] Step 3: Extract targets for selected items only
- [ ] Step 4A: **Create data inventory table** (Dataset | Period | In Package?)
- [ ] Step 4A: **Check replication package** for each dataset
- [ ] Step 4A: **HARD STOP if any data missing** - ask user if they have it
- [ ] Step 4B: Execute code only after all data confirmed available

**If you skip any step, you have violated the replication protocol.**
