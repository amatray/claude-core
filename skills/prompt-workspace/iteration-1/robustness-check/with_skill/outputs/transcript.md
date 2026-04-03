# /prompt: Robustness Check — Clustering Alternatives

## Phase 1: Formatted Prompt

**Role auto-selected:** Research & Data Analysis (signals: regression, robustness, specification, econometrics, Stata)

**Depth:** Standard (task involves empirical analysis with multiple specifications and comparison)

```
You are a senior quantitative economist with expertise in experimental design, causal inference, and applied econometric analysis.

**Task:** Re-estimate the main regression specification under three different clustering schemes and produce a comparison table of standard errors:
1. Baseline: clustering at the county level (current specification)
2. Alternative 1: clustering at the state level
3. Alternative 2: two-way clustering at the state and year level

**Context:** This is a robustness check for an existing empirical result. The main regression is already estimated with county-level clustering. The goal is to assess sensitivity of inference to the level of clustering.

**Constraints:**
- Use Stata. Use `reghdfe` or the existing estimation command from the main specification.
- For two-way clustering, use `vce(cluster state_var year_var)` syntax (reghdfe) or `cluster2` / Cameron-Gelbach-Miller approach if using `regress`.
- Keep all regressors, fixed effects, and sample restrictions identical across specifications. Only the clustering changes.

**Output format:**
- A single comparison table with one row per regressor (or at minimum the key treatment variable), showing:
  - Point estimate (should be identical across columns)
  - Standard errors under each clustering scheme (3 columns)
  - Stars based on each column's own standard errors
- Save the do-file to the project's `code/` directory.

Include at the end:
- Key assumptions (2-3 bullets)
- Brief rationale for major choices
```

**Tool routing:** Proceed in Claude Code (Stata via MCP, local file access).

---

## Phase 2: Execution Approach

Since there are no actual project files available, here is the concrete approach I would take to execute this prompt.

### Step 1: Locate the main specification

I would search the project's `code/` directory for the main regression do-file, looking for `reghdfe` or `reg` commands with `cluster(county*)` in the `vce()` option. This identifies the exact command, dependent variable, regressors, fixed effects, and sample restrictions.

### Step 2: Write the do-file

I would create a do-file (e.g., `code/robustness_clustering.do`) structured as follows:

```stata
* ==============================================================================
* Robustness: Alternative clustering
* ==============================================================================

* Load data
use "path/to/analysis_data.dta", clear

* --- (1) Baseline: county clustering ---
eststo clear
reghdfe y treatment controls, absorb(fe1 fe2) vce(cluster county_fips)
eststo m_county

* --- (2) State clustering ---
reghdfe y treatment controls, absorb(fe1 fe2) vce(cluster state_fips)
eststo m_state

* --- (3) Two-way clustering: state x year ---
reghdfe y treatment controls, absorb(fe1 fe2) vce(cluster state_fips year)
eststo m_twoway

* --- Comparison table ---
esttab m_county m_state m_twoway using "output/table_clustering_robustness.tex", ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("County" "State" "State x Year") ///
    keep(treatment) ///
    label replace booktabs ///
    title("Robustness: Alternative Clustering of Standard Errors")
```

### Step 3: Execute via MCP and check output

Run the do-file using `mcp__stata__run_do_file`, inspect the log for errors, and verify the output table. Point estimates should be identical across all three columns; only standard errors and significance levels may differ.

### Key assumptions

- The main specification uses `reghdfe`, which natively supports multi-way clustering via `vce(cluster var1 var2)`.
- A state identifier variable exists in the dataset (or can be derived from the county FIPS code by taking the first two digits).
- The year variable used for two-way clustering is the same time variable used in the panel structure.

### Rationale

- State-level clustering accounts for within-state spatial correlation that county clustering may understate (Moulton problem when treatment varies at a coarser level).
- Two-way clustering (state and year) additionally allows for arbitrary temporal correlation within years across all states, following Cameron, Gelbach, and Miller (2011).
- Keeping everything else identical ensures the comparison isolates the effect of the clustering choice on inference.
