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
# ║  DO NOT DOWNLOAD ANYTHING BEFORE ASKING USER.                        ║
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
# ║  STEP 4: CREATE DATA INVENTORY - MANDATORY HARD STOP                ║
# ║                                                                       ║
# ║  Create comprehensive data inventory table showing:                  ║
# ║  - Dataset name and description                                      ║
# ║  - Time period covered                                               ║
# ║  - Whether it exists (check Dropbox, previous replications)          ║
# ║  - File location if available                                        ║
# ║  - Estimated file size                                               ║
# ║  - Required action (Download/Symlink/Ask User)                       ║
# ║                                                                       ║
# ║  If ANY dataset is missing: HARD STOP                                ║
# ║  Ask user: "I found that [X] datasets are missing. Do you already    ║
# ║  have these data files? If yes, where are they located? If not,      ║
# ║  I can help you identify how to obtain them."                        ║
# ║                                                                       ║
# ║  DO NOT DOWNLOAD ANYTHING BEFORE USER APPROVAL                       ║
# ║  Large files (>1GB) require explicit permission with size shown      ║
# ║                                                                       ║
# ║  STEP 5: EXECUTE REPLICATION FOR SELECTED ITEMS ONLY                ║
# ║                                                                       ║
# ║  Run/translate code to generate ONLY the selected outputs.           ║
# ║                                                                       ║
# ║  IF YOU SKIP STEPS 2 OR 4, YOU HAVE WASTED THE ENTIRE SESSION.      ║
# ║  DO NOT EXTRACT TARGETS BEFORE USER SELECTS ITEMS.                   ║
# ║  DO NOT START REPLICATION BEFORE USER SELECTS ITEMS.                 ║
# ║  DO NOT DOWNLOAD DATA BEFORE VERIFYING USER DOESN'T HAVE IT.        ║
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

### 2. Data Inventory is MANDATORY

**BEFORE downloading, fetching, or acquiring ANY data files, you MUST create a data inventory table.**

**This is NOT optional. This is NOT a suggestion. This is MANDATORY.**

Failure to create this table first will result in:
- Wasted bandwidth downloading files the user already has
- Wasted disk space storing duplicate data
- Wasted time and computational resources
- System performance issues from unnecessary large downloads

**ALWAYS CHECK FIRST:**
1. Ask user explicitly if they have the data
2. Check their Dropbox folders
3. Check previous replication packages
4. Check shared data repositories
5. ONLY THEN download missing files

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

- **After Phase 1 (Inventory):** "Ready to proceed to data inventory?"
- **After Phase 2 (Data Inventory):** "Ready to proceed to execution?"
- **After Phase 3 (Execute):** "Ready to proceed to verification?"
- **When encountering blockers:** Report and ask how to proceed

Do not silently continue through all phases without user checkpoints.

### 5. Figure Comparison Output - MANDATORY

**WHEN REPLICATING ANY FIGURE, YOU MUST CREATE A SIDE-BY-SIDE COMPARISON.**

**This is NOT optional. Every figure output MUST include:**

1. **Original figure** extracted from the paper PDF
2. **Replicated figure** generated from your code
3. **Side-by-side layout** for easy visual comparison

**Implementation:**
- Extract original figure from PDF (using appropriate tools)
- Generate replicated figure from code
- Create composite image with both side-by-side
- Save as: `figure_X_comparison.png` (or .pdf)
- Label clearly: "Original (Paper)" and "Replicated"

**Example output structure:**
```
┌─────────────────────────────────────────┐
│  Original (Paper)  │  Replicated        │
│                    │                    │
│  [Figure from PDF] │  [Your figure]     │
│                    │                    │
└─────────────────────────────────────────┘
```

**Tools to use:**
- R: `cowplot::plot_grid()`, `patchwork`, or `gridExtra::grid.arrange()`
- Python: `matplotlib.pyplot.subplot()` or `PIL.Image`
- ImageMagick: `convert +append original.png replicated.png comparison.png`

**Why this matters:**
- User can immediately see visual differences
- Makes verification much faster
- Highlights subtle differences in scales, colors, layout
- No need to open multiple files or switch between windows

**If you generate a figure without the original for comparison, you have failed this requirement.**

---

## Five-Phase Protocol

### Phase 1: Paper Analysis & Item Selection

#### Step 1: Extract and Read the Paper

Use pdf-chunker skill to extract paper content:
```bash
# The skill handles this automatically when invoked
```

**NEVER use Read tool directly on PDF files** - they will fill your context window.

#### Step 2: Identify All Tables and Figures

Create a complete inventory of ALL items in the paper:
- Scan through entire paper
- List ALL tables and figures
- Note page numbers
- Classify priority (High/Medium/Low)
- Mark which are feasible without confidential data

#### Step 3: Create Inventory Table

**MANDATORY TABLE FORMAT:**
- Use markdown table with clear column headers
- Include: # (sequential number), Item (Table/Figure name), Description, Page, Priority
- Priority levels: **HIGH** (bold for main results), Medium, Low
- Add a summary line at the end showing total count by priority
- Present the FULL table without truncation

**Example:**
```markdown
| # | Item | Description | Page | Priority |
|---|------|-------------|------|----------|
| 1 | Table 1 | Summary statistics | 12 | Low |
| 2 | Table 2 | Main results | 15 | **HIGH** |
| 3 | Figure 1 | Event study | 16 | **HIGH** |
| 4 | Table 3 | Robustness checks | 18 | Medium |

**Summary:** 4 total items (2 HIGH, 1 Medium, 1 Low)
```

#### Step 4: Ask User to Select Items

**ASK the user which tables/figures they want to replicate.**

Do NOT assume which items to replicate. Let the user decide based on:
- Data availability
- Complexity
- Research priorities
- Time constraints

**Wait for explicit selection before proceeding.**

#### Step 5: Extract Targets for Selected Items Only

Only after user selects items:
- Extract gold standard numbers from paper
- Create target files in `targets/` directory
- One file per selected table/figure
- Document exactly where numbers come from in the paper

#### Step 6: Update PROJECT.md

Document the replication scope:
- Which items were selected
- Why (if user provided reasons)
- Current phase
- Any special considerations

**STOP and get approval before Phase 2**

---

### Phase 2: Data Inventory (MANDATORY - HARD STOP IF DATA MISSING)

#### Step 1: Identify All Required Datasets

**Before running ANY code or downloading ANYTHING:**

1. **Read the paper's data section** (data description, footnotes, online appendix)
2. **Read original code** (if available) to identify all data files used
3. **List every dataset** needed for the selected tables/figures

#### Step 2: Create Comprehensive Data Inventory Table

**YOU MUST create this table and show it to the user BEFORE downloading anything:**

```markdown
### Data Inventory for [Paper] - [Selected Tables]

**Replication Package Available:** [Yes/No] [URL if yes]

| # | Data Source | Description | Required Coverage | In Rep. Pkg? | Already Have? | Location | Est. Size | Action |
|---|-------------|-------------|------------------|--------------|---------------|----------|-----------|--------|
| 1 | [Name] | [Brief desc] | [Years/periods] | ✅/❌ | ✅/❌/⚠️ | [Path or N/A] | [Size] | [Download/Symlink/Ask] |
| 2 | | | | | | | | |

**Legend:**
- ✅ Yes / Available
- ❌ No / Not Available
- ⚠️ Partial / Needs Verification

**Before proceeding with any downloads, please confirm:**
- [ ] Do you have any of these datasets in Dropbox, shared drives, or previous projects?
- [ ] For items marked "Download" - should I proceed?
- [ ] Any large files (>1GB) require explicit approval with size shown.

**Total download size (if all missing):** [X.X GB]
```

#### Step 3: Check for Existing Data

**Priority order for finding data:**

1. **First:** Check if data is in existing replication packages
   ```bash
   # Example: Check previous replications by same authors
   find ~/claude-workflows/replications -name "*author_name*" -type d
   ```

2. **Second:** Ask user about their existing data
   - Check Dropbox folders (especially `_Source/` directories)
   - Check shared drives
   - Check previous projects
   - Ask: "Do you have [dataset name] anywhere in your Dropbox or shared drives?"

3. **Third:** Check replication package (if one exists)
   - Look in `original/data/` directory
   - Verify symlinks actually point to existing files (use `ls -lh` or `file`)
   - Check file sizes (>0 bytes)
   - Mark as "Yes" only if file exists and is accessible

4. **Last:** Download only what's truly missing
   - Always show download size first
   - For files >100MB, ask for explicit permission
   - For files >1GB, REQUIRE explicit permission with size shown

#### Step 4: HARD STOP if Data is Missing

**IF ANY DATASET SHOWS "No" or "⚠️": HARD STOP**

Present the data inventory table to user and ask:

```
"I've identified the following datasets required for replication:

[Show data inventory table]

The following datasets are MISSING from the replication package:
- [Dataset 1] ([required coverage])
- [Dataset 2] ([required coverage])

Do you already have these data files? If yes, please tell me where
they are located. If not, I can help you identify how to obtain them."
```

**WAIT for user response** - do NOT proceed until all data is confirmed available or user approves downloads.

#### Step 5: Handle Large Downloads

For files >1GB, **YOU MUST:**

```
STOP and show the user:

"⚠️ LARGE DOWNLOAD ALERT ⚠️

File: [filename]
Size: [X.X GB]
Source: [URL]
Purpose: [what it's needed for]

This will take approximately [estimate] to download and use [X.X GB] of disk space.

Should I proceed? (yes/no)"
```

Wait for explicit user approval before proceeding.

**If you realize mid-download that the user likely has the data:**
1. **STOP the download immediately** using KillShell
2. Ask user about existing data
3. Only resume if user confirms they don't have it

**Better to ask twice than download once unnecessarily.**

---

### Phase 3: Data Acquisition (Only After User Approval)

#### Symlinks vs Copies

**ALWAYS use symlinks (never copy) for existing data files:**

```bash
# Create symlink to existing data
cd /path/to/replication/original/data_folder
ln -s "/path/to/existing/data.dta" .

# Example:
ln -s "/Users/user/Matray Dropbox/_Source/Trade/data_2007.dta" .
```

**Why symlinks, not copies:**
- Avoids duplicate storage (critical for large files)
- Maintains single source of truth
- Shows clear data provenance
- Automatic updates if source is revised

**Never copy data files** unless:
- File is very small (<1MB) AND
- You need to modify it for this specific replication

#### Document Data Provenance

In each processing script, include header:
```r
# Data Source: [Name and URL]
# Downloaded: [Date]
# Original location: [Path]
# File size: [Size]
# Coverage: [Years/scope]
```

---

### Phase 4: Execute Replication

#### Create Modular Scripts

Organize processing into logical steps:

```
translated/
├── 00_download_data.R          # Only if downloads are needed
├── 01_process_[dataset1].R     # Clean and prepare first dataset
├── 02_process_[dataset2].R     # Clean and prepare second dataset
├── 03_merge_datasets.R         # Combine data sources
├── 04_replicate_table_X.R      # Generate specific table
└── utils.R                     # Shared functions
```

#### Execution Rules

1. **Run/translate code** for selected items only
2. **Save outputs** to `output/` folder
3. **Match original specifications exactly** - no improvements
4. **Use proper directory structure:**
   - Scripts in `translated/`
   - Outputs in `output/`
   - Targets in `targets/`
5. **STOP and present outputs before Phase 5**

#### Figure Replication - Special Requirements

**When replicating figures, you MUST create side-by-side comparisons.**

**Step-by-step process:**

1. **Extract original figure from paper PDF:**
   ```bash
   # Use pdfimages, pdftoppm, or similar
   pdftoppm -png -f [page] -l [page] paper.pdf original_fig
   # Or crop specific region if needed
   ```

2. **Generate replicated figure from your code:**
   ```r
   # Standard figure generation
   ggplot(...) + ...
   ggsave("replicated_figure1.png", width=6, height=4, dpi=300)
   ```

3. **Create side-by-side comparison:**

   **Option A: Using R (cowplot):**
   ```r
   library(cowplot)
   library(magick)

   # Load images
   original <- image_read("original_figure1.png")
   replicated <- image_read("replicated_figure1.png")

   # Create side-by-side comparison
   comparison <- image_append(c(original, replicated))

   # Add labels
   comparison <- image_annotate(comparison, "Original (Paper)",
                                 size=20, location="+50+20")
   comparison <- image_annotate(comparison, "Replicated",
                                 size=20, location="+[width/2]+20")

   # Save
   image_write(comparison, "output/figure1_comparison.png")
   ```

   **Option B: Using ImageMagick (command line):**
   ```bash
   # Horizontal side-by-side
   convert original.png replicated.png +append comparison.png

   # Add labels
   convert comparison.png -pointsize 20 -annotate +50+30 'Original' \
           -annotate +[width/2]+30 'Replicated' figure1_comparison.png
   ```

   **Option C: Using Python (matplotlib):**
   ```python
   import matplotlib.pyplot as plt
   from PIL import Image

   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

   # Load and display original
   original = Image.open('original_figure1.png')
   ax1.imshow(original)
   ax1.set_title('Original (Paper)', fontsize=14)
   ax1.axis('off')

   # Load and display replicated
   replicated = Image.open('replicated_figure1.png')
   ax2.imshow(replicated)
   ax2.set_title('Replicated', fontsize=14)
   ax2.axis('off')

   plt.tight_layout()
   plt.savefig('output/figure1_comparison.png', dpi=300, bbox_inches='tight')
   ```

4. **Save with clear naming convention:**
   - Format: `figureX_comparison.png` (or `.pdf`)
   - Also save individual files: `figureX_original.png`, `figureX_replicated.png`

5. **Document in verification report:**
   - Note any visual differences (scales, colors, symbols)
   - Explain if dimensions differ (aspect ratio)
   - Highlight if data patterns match despite cosmetic differences

**Why this is mandatory:**
- Immediate visual verification
- User can spot differences at a glance
- Much faster than opening multiple files
- Highlights subtle differences in formatting/styling
- Essential for effective figure replication verification

**Output directory structure for figures:**
```
output/
├── figure1_original.png         # Extracted from paper
├── figure1_replicated.png       # Your generated figure
├── figure1_comparison.png       # MANDATORY: Side-by-side
└── figure1_notes.md             # Optional: Notes on differences
```

---

### Phase 5: Verification

#### Compare Results to Targets

1. Load gold standard numbers from paper
2. Generate results
3. Create comparison table showing:
   - Target value
   - Replicated value
   - Absolute difference
   - Percentage error
   - Match status (within tolerance?)

#### Apply Tolerance Thresholds

**Acceptable tolerances by data type:**

- **Survey data:** ±1-3 percentage points (sampling variation)
- **Financial data:** ±0.1-0.5% (rounding, data vintage)
- **Trade data:** ±1-2% (revisions, classification changes)
- **Sample size (N):** Exact match required
- **Coefficients:** < 0.01 difference acceptable
- **Standard errors:** < 0.05 difference acceptable
- **P-values:** Same significance level required

#### Generate Verification Report

Create comprehensive report in `verification/` directory:
- Summary statistics (how many exact matches, within tolerance, etc.)
- Detailed comparison tables
- Analysis of discrepancies
- Potential explanations for differences
- Recommendations for further investigation

#### Document Discrepancies

If differences exceed tolerances:
1. Check for data vintage issues
2. Check for methodological ambiguities in paper
3. Check for translation errors (Stata → R)
4. Check for different random seeds (if applicable)
5. Document findings in verification report

---

## Common Mistakes to Avoid

❌ **Starting replication without asking which items to replicate**
- Wastes time on unwanted tables/figures
- User only wanted 2 items, you replicated 20
- **Always ask first, then extract targets**

❌ **Downloading data without asking if user has it**
- Wasted bandwidth downloading files the user already has
- Wasted disk space storing duplicate data
- **Always create data inventory table first**

❌ **Running code before verifying all data exists**
- Code fails halfway through
- Discover missing data after hours of work
- **Always verify data availability BEFORE running code**

❌ **Assuming data files exist and are accessible**
- Symlinks may be broken
- Files may need to be downloaded
- Paths may be machine-specific
- **Always check with ls -lh or file commands**

❌ **Using Read tool on PDF files**
- Fills context window
- Causes session to fail
- **Always use pdf-chunker skill instead**

❌ **Continuing silently when code fails**
- Missing data → Report immediately, don't try to download without asking
- Broken dependencies → Ask user, don't install without permission
- Wrong results → Stop and investigate, don't keep going
- **Always report blockers and ask how to proceed**

❌ **Improving or modernizing code during replication**
- First replication must match original exactly
- Improvements come later, after verification
- **Match original specifications exactly**

❌ **Downloading large files (>1GB) without permission**
- May use significant bandwidth and disk space
- User may already have the data elsewhere
- **Always show size and ask for approval**

❌ **Copying data files instead of symlinking**
- Wastes disk space with duplicates
- Creates confusion about which version is canonical
- **Use symlinks for all existing data files**

---

## Example Workflows

### ✅ GOOD Workflow:

```
1. User: "Replicate Tables 1 and 2 from this paper"
2. Assistant: [Uses pdf-chunker to read paper]
3. Assistant: "I found 8 tables and 5 figures. Here's the inventory..."
4. Assistant: "Which would you like me to replicate?"
5. User: "Tables 1 and 2"
6. Assistant: [Extracts targets for Tables 1 & 2 only]
7. Assistant: [Creates data inventory table]
8. Assistant: "Here's what we need. Do you already have any of these?"
9. User: "Yes, trade data is in my Dropbox at X"
10. Assistant: [Creates symlinks to existing data]
11. Assistant: [Runs replication for Tables 1 & 2]
12. ✅ Efficient, no wasted work
```

### ❌ BAD Workflow:

```
1. User: "Replicate Tables 1 and 2 from this paper"
2. Assistant: [Immediately starts extracting all 8 tables]
3. Assistant: [Starts downloading 19GB trade data]
4. User: "Wait, I only wanted Tables 1 and 2!"
5. User: "And I already have that trade data in Dropbox!"
6. 😱 Wasted extraction work
7. 😱 Wasted bandwidth
8. 😱 Wasted disk space
```

---

## Project Structure

```
~/claude-workflows/replications/author-year-journal/
├── .claude/
│   └── PROJECT.md              # Project-specific context
├── paper/                       # Paper PDF (REQUIRED)
│   └── paper.pdf
├── original/                    # Original replication package (if available)
│   ├── data/                    # (may be empty, symlinks, or actual data)
│   ├── code/
│   └── results/
├── targets/                     # Gold standard (selected items only)
│   ├── table2_targets.csv
│   └── figure1_targets.csv
├── translated/                  # Your code
│   ├── 01_clean_data.R
│   └── 02_replicate_table2.R
├── output/                      # Your results (selected items only)
│   ├── table2_comparison.csv
│   └── figure1_output.png
├── verification/                # Comparison reports
│   └── replication_report.md
├── DATA_INVENTORY.md           # List of all required datasets
├── README.md                    # Project documentation
└── REPLICATION_LOG.md          # Progress tracking (optional)
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
- [ ] Step 2: Create inventory of ALL tables/figures with priority levels
- [ ] Step 3: **ASK USER** which items to replicate
- [ ] Step 4: Extract targets for **selected items only**
- [ ] Step 5: Create **data inventory table** (Dataset | Period | Already Have? | Location | Size | Action)
- [ ] Step 6: **CHECK with user** if they have any datasets before downloading
- [ ] Step 7: **STOP if data missing** - ask user where it is or if they approve download
- [ ] Step 8: Use **symlinks** for existing data, not copies
- [ ] Step 9: Execute code **only after** all data confirmed available
- [ ] Step 10: Generate **verification report** comparing to targets

**If you skip any step, you have violated the replication protocol.**

**This is especially critical for Steps 3 (Ask which items), 5 (Create data inventory), and 6 (Ask about existing data) - these prevent wasted work.**

---

## Enforcement

This protocol is MANDATORY for all replication tasks.

**You MUST:**
- Ask which items to replicate before extracting targets
- Create data inventory table before downloading anything
- Ask user if they have data before downloading
- Use symlinks for existing data files
- Stop at phase boundaries for user approval

**If you violate these rules, you have failed the task regardless of whether the replication ultimately succeeds.**
