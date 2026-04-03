I don't have access to project files to identify your main regression, so I can't write and execute the do-file directly. Here is the general approach and code template you would adapt.

The idea is to run the same regression three times, varying only the `vce()` option, then compare standard errors side by side in a single table.

**Approach:**

1. Baseline: cluster at county level (your current spec)
2. Alternative 1: cluster at state level
3. Alternative 2: two-way cluster at state and year

**Stata code template** (save as, e.g., `code/robustness_clustering.do`):

```stata
* ==============================================================================
* Robustness: Alternative clustering of standard errors
* ==============================================================================

* --- Setup ---
use "$datapath/your_main_dataset.dta", clear
eststo clear

* --- (1) County clustering (baseline) ---
reghdfe y treatment x1 x2 x3, absorb(county year) vce(cluster county_fips)
eststo county

* --- (2) State clustering ---
reghdfe y treatment x1 x2 x3, absorb(county year) vce(cluster state_fips)
eststo state

* --- (3) Two-way clustering: state x year ---
reghdfe y treatment x1 x2 x3, absorb(county year) vce(cluster state_fips year)
eststo twoway

* --- Comparison table ---
esttab county state twoway using "$output/robustness_clustering.tex", ///
    replace booktabs label                                             ///
    se star(* 0.10 ** 0.05 *** 0.01)                                  ///
    mtitles("County" "State" "State x Year")                          ///
    title("Robustness: Alternative Clustering")                       ///
    note("Standard errors in parentheses. Column 1 clusters at the county level, " ///
         "Column 2 at the state level, Column 3 two-way clusters by state and year.") ///
    keep(treatment)
```

**What to look for in the output:**

- Point estimates should be identical across all three columns (only the standard errors change).
- State-level clustering will typically produce larger standard errors than county-level, because it accounts for within-state correlation across counties.
- Two-way clustering (state and year) adds protection against cross-sectional dependence within years. Standard errors could be larger or smaller than state-only clustering depending on the correlation structure in your data.
- If significance holds across all three, that is strong evidence of robustness.

**To proceed:** point me to the project directory and main do-file (or tell me the variable names), and I will write the actual do-file and run it via Stata.
