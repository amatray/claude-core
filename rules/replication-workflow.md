# Replication Workflow Protocol

This protocol defines the mandatory workflow for replicating academic papers.

---

## ⚠️ CRITICAL: Data Inventory is MANDATORY

**BEFORE downloading, fetching, or acquiring ANY data files:**

### YOU MUST CREATE A DATA INVENTORY TABLE

**This is NOT optional. This is NOT a suggestion. This is MANDATORY.**

Failure to create this table first will result in:
- Wasted bandwidth downloading files the user already has
- Wasted disk space storing duplicate data
- Wasted time and computational resources
- System performance issues from unnecessary large downloads

---

## Phase 1: Paper Analysis & Table Selection

### Step 1: Extract and Read the Paper

```bash
python ~/claude-workflows/claude-core/scripts/extract_pdf.py <pdf_path> --output /tmp/extracted.txt
```

### Step 2: Identify All Tables and Figures

Create a complete inventory in `PROJECT.md`:
- List ALL tables and figures in the paper
- Note their page numbers
- Classify priority (High/Medium/Low)
- Mark which are feasible without confidential data

### Step 3: User Selects Target Tables

**ASK the user which tables they want to replicate.**

Do NOT assume which tables to replicate. Let the user decide based on:
- Data availability
- Complexity
- Research priorities

---

## Phase 2: Data Inventory (MANDATORY)

### **CRITICAL STEP: Create Data Inventory Table BEFORE Any Downloads**

You MUST create this table and show it to the user BEFORE downloading anything:

```markdown
### Data Inventory for [Paper Name] - [Selected Tables]

| Data Source | Required Years/Coverage | In Replication Package? | Already Available? | Location (if available) | File Size | Action Needed |
|-------------|------------------------|------------------------|-------------------|------------------------|-----------|---------------|
| [Dataset 1] | [Years] | ✅/❌ | ✅/❌/⚠️ | [Path or N/A] | [Size] | [Download/Copy/Ask User] |
| [Dataset 2] | [Years] | ✅/❌ | ✅/❌/⚠️ | [Path or N/A] | [Size] | [Download/Copy/Ask User] |
| ... | ... | ... | ... | ... | ... | ... |
```

**Legend:**
- ✅ Yes / Available
- ❌ No / Not Available
- ⚠️ Partial / Needs Verification

### Required Information for Each Data Source

1. **Exact description** of the data source
2. **Time coverage** needed (years, quarters, months)
3. **Whether it's in a replication package** (if one exists)
4. **Whether user already has it** - ASK them to check:
   - Their Dropbox folders
   - Previous replication packages
   - Shared data repositories
5. **Estimated file size** (if known from documentation)
6. **Required action:**
   - Download from [URL]
   - Copy from [existing location]
   - Ask user for location
   - Aggregate from monthly/quarterly files

### Presenting the Table to the User

**YOU MUST:**
1. Create this table completely
2. Show it to the user
3. **EXPLICITLY ASK:** "Before I download any files, please verify:
   - Do you already have any of these datasets in Dropbox or elsewhere?
   - For items marked 'Download' - should I proceed?"

**YOU MUST NOT:**
- Start any downloads before user approval
- Assume user doesn't have the data
- Download large files (>1GB) without explicit permission

---

## Phase 3: Data Acquisition (Only After User Approval)

### Priority Order:

1. **First:** Check if data is in existing replication packages
   ```bash
   # Example: Check previous replications by same authors
   find /path/to/replications -name "*author_name*" -type d
   ```

2. **Second:** Ask user about their existing data
   - Check Dropbox folders
   - Check shared drives
   - Check previous projects

3. **Third:** Symlink from existing locations
   ```bash
   # ALWAYS use symlinks (never copy) for existing data files
   cd /path/to/replication/original/data_folder
   ln -s "/path/to/existing/data.dta" .

   # Example:
   ln -s "/Users/user/Dropbox/_Source/Trade/data_2007.dta" .
   ```

   **Why symlinks, not copies:**
   - Avoids duplicate storage (critical for large files)
   - Maintains single source of truth
   - Shows clear data provenance
   - Automatic updates if source is revised

   **Never copy data files** unless:
   - File is very small (<1MB) AND
   - You need to modify it for this specific replication

4. **Last:** Download only what's truly missing
   - Always show download size first
   - For files >100MB, ask for explicit permission
   - For files >1GB, REQUIRE explicit permission with file size shown

### For Large Downloads (>1GB)

**YOU MUST:**
```
STOP and show the user:

"⚠️ LARGE DOWNLOAD ALERT ⚠️

File: [filename]
Size: [X.X GB]
Source: [URL]
Purpose: [what it's needed for]

This will take approximately [estimate] to download.

Should I proceed? (yes/no)"
```

Wait for explicit user approval before proceeding.

---

## Phase 4: Data Processing

### Create Modular Scripts

Organize processing into logical steps:

```
translated/
├── 00_download_data.R          # Only if downloads are needed
├── 01_process_[dataset1].R     # Clean and prepare first dataset
├── 02_process_[dataset2].R     # Clean and prepare second dataset
├── 03_merge_datasets.R         # Combine data sources
├── 04_generate_table_X.R       # Generate specific table
└── utils.R                     # Shared functions
```

### Document Data Provenance

In each processing script, include header:
```r
# Data Source: [Name and URL]
# Downloaded: [Date]
# Original location: [Path]
# File size: [Size]
# Coverage: [Years/scope]
```

---

## Phase 5: Verification

### Compare Results to Targets

1. Load gold standard numbers from paper
2. Generate results
3. Create comparison table showing:
   - Target value
   - Replicated value
   - Absolute difference
   - Percentage error

### Acceptable Tolerances

- Survey data: ±1-3 percentage points (sampling variation)
- Financial data: ±0.1-0.5% (rounding, data vintage)
- Trade data: ±1-2% (revisions, classification changes)

### Document Discrepancies

If differences exceed tolerances:
1. Check for data vintage issues
2. Check for methodological ambiguities
3. Check for translation errors (Stata → R)
4. Document findings in verification report

---

## Common Mistakes to Avoid

### ❌ DON'T:
- Download data without checking if user has it
- Download entire datasets when only subset is needed
- Download 19GB files for 3 years of data
- Assume replication package doesn't exist
- Start downloading during initial exploration

### ✅ DO:
- Create data inventory table FIRST
- Ask user about existing data sources
- Use symlinks for large existing files
- Download only missing components
- Show file sizes before large downloads
- Check previous replications by same authors

---

## Example: Good vs Bad Workflow

### ❌ BAD Workflow:
```
1. User: "Replicate Tables 1 and 2"
2. Assistant: *immediately starts downloading 19GB trade data*
3. User: "Wait, I already have that in Dropbox!"
4. 😱 System resources wasted
```

### ✅ GOOD Workflow:
```
1. User: "Replicate Tables 1 and 2"
2. Assistant: Creates data inventory table
3. Assistant: "Here's what we need. Do you already have any of these?"
4. User: "Yes, trade data is in my Dropbox at X"
5. Assistant: Creates symlinks to existing data
6. ✅ No wasted downloads
```

---

## Emergency Stop Procedures

If you realize mid-download that the user likely has the data:

1. **STOP the download immediately** using KillShell
2. Ask user about existing data
3. Only resume if user confirms they don't have it

**Better to ask twice than download once unnecessarily.**

---

## Template: Data Inventory Table

Copy and adapt this template:

```markdown
### Data Inventory for [Paper] - [Tables X, Y, Z]

**Replication Package Available:** [Yes/No] [URL if yes]

| # | Data Source | Description | Required Coverage | In Rep. Pkg? | Already Have? | Location | Est. Size | Action |
|---|-------------|-------------|------------------|--------------|---------------|----------|-----------|--------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |

**Before proceeding with any downloads, please confirm:**
- [ ] Do you have any of these datasets in Dropbox, shared drives, or previous projects?
- [ ] For items marked "Download" - should I proceed?
- [ ] Any large files (>1GB) require explicit approval with size shown.

**Total download size (if all missing):** [X.X GB]
```

---

## Enforcement

This protocol is MANDATORY for all replication tasks.

If you skip the data inventory step, you have failed the task regardless of whether the replication ultimately succeeds.

**The data inventory table is not optional documentation - it is a required safety check.**
