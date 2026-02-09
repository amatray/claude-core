# Stata to R Conversion Guide

This guide documents critical differences between Stata and R that cause silent bugs when translating code. These patterns emerged from real replication failures.

## ⚠️ Critical Translation Issues

### 1. Row Dropping Syntax

**Stata:**
```stata
drop in 820/996    /* Drops rows 820 THROUGH 996 (inclusive range) */
```

**WRONG R translation:**
```r
df <- df[1:819, ]  # Drops EVERYTHING after row 819!
```

**CORRECT R translation:**
```r
df <- df[-(820:996), ]  # Drops only rows 820-996
```

**Why this matters:** Using `[1:819]` when you meant to drop a specific range will silently delete all subsequent data. In a real case, this caused items at row 2834+ to disappear, leading to 40% underestimation of results.

---

### 2. Empty String vs NA/Missing Value Checking

**Stata:**
```stata
drop if var == ""    /* ONLY drops empty strings, NOT missing values */
```

**WRONG R translation:**
```r
df <- df %>% filter(var != "")  # Drops BOTH empty strings AND NA values!
```

**CORRECT R translation:**
```r
df <- df %>% filter(is.na(var) | var != "")  # Explicitly keep NAs
```

**Why this matters:** Many datasets (especially BLS/Census tables) use NA for header rows or metadata that must be preserved. The default R behavior of dropping NAs will corrupt hierarchical data structures.

**Test case:**
```r
# Create test data
df <- data.frame(
  item = c("Header", "Data", "Footer"),
  value = c(NA, "100", "")
)

# Wrong: loses the Header row
df %>% filter(value != "")  # Returns 1 row (Data only)

# Correct: keeps Header row
df %>% filter(is.na(value) | value != "")  # Returns 2 rows (Header and Data)
```

---

### 3. Hierarchical Survey Data Structure

Many BLS/Census survey tables (CEX, CPS, etc.) use this structure:

```
Item                        Value
────────────────────────────────
Food                        NA        ← Category header
  Mean                      1000      ← Actual data
  SE                        50        ← Standard error
  CV(%)                     5.0       ← Coefficient of variation
Clothing                    NA        ← Next category
  Mean                      500
  ...
```

**Stata approach:**
```stata
/* Stata's collapse handles this implicitly */
collapse (sum) Value, by(Item) fast
```

**R requires explicit handling:**
```r
# Step 1: Identify and rename "Mean" rows to their parent category
last_item_name <- NA
for (i in 1:nrow(df)) {
  current_item <- df$Item[i]

  # Track most recent category name (not Mean/SE/CV)
  if (!current_item %in% c("Mean", "SE", "CV(%)")) {
    last_item_name <- current_item
  }

  # Rename "Mean" row to its parent category
  if (current_item == "Mean" && !is.na(last_item_name)) {
    df$Item[i] <- last_item_name
  }
}

# Step 2: Drop SE and CV(%) rows
df <- df %>% filter(!Item %in% c("SE", "CV(%)"))

# Step 3: Now collapse works correctly
df <- df %>%
  group_by(Item) %>%
  summarise(across(starts_with("Value"), ~ sum(., na.rm = TRUE)))
```

**Why this matters:** Without explicit Mean row renaming, category headers remain with NA values while actual data sits in separate "Mean" rows. This causes all category values to be zero after collapse.

---

## Common Translation Patterns

### Destring (Convert to Numeric)

**Stata:**
```stata
destring varname, replace force
```

**R equivalent:**
```r
df <- df %>%
  mutate(varname = as.numeric(as.character(varname)))
```

Note: `as.character()` first is important if the column is a factor.

---

### Collapse (Aggregate)

**Stata:**
```stata
collapse (sum) value1 value2, by(group) fast
collapse (mean) value, by(group1 group2)
```

**R equivalent:**
```r
# Sum
df <- df %>%
  group_by(group) %>%
  summarise(across(c(value1, value2), ~ sum(., na.rm = TRUE)), .groups = "drop")

# Mean
df <- df %>%
  group_by(group1, group2) %>%
  summarise(value = mean(value, na.rm = TRUE), .groups = "drop")
```

---

### Reshape (Long/Wide)

**Stata:**
```stata
reshape long value, i(id) j(year)
reshape wide value, i(id) j(year)
```

**R equivalent:**
```r
# Long
df_long <- df %>%
  pivot_longer(
    cols = starts_with("value"),
    names_to = "year",
    names_prefix = "value",
    values_to = "value"
  )

# Wide
df_wide <- df_long %>%
  pivot_wider(
    id_cols = id,
    names_from = year,
    values_from = value
  )
```

---

### Generate New Variable with Condition

**Stata:**
```stata
gen newvar = value if Item == "Target"
bysort group: egen total = mean(newvar)
```

**R equivalent:**
```r
df <- df %>%
  mutate(newvar = ifelse(Item == "Target", value, NA)) %>%
  group_by(group) %>%
  mutate(total = mean(newvar, na.rm = TRUE)) %>%
  ungroup()
```

---

### Merge (Join)

**Stata:**
```stata
merge 1:1 id using other_data, keep(3)  /* Keep only matched */
merge m:1 id using other_data           /* Many-to-one merge */
```

**R equivalent:**
```r
# Inner join (keep matched only)
df <- df %>% inner_join(other_data, by = "id")

# Left join (many-to-one, keep all from left)
df <- df %>% left_join(other_data, by = "id")
```

---

## Regression Translation

### Fixed Effects Regression

**Stata:**
```stata
reghdfe y x1 x2, absorb(firm year) cluster(firm year)
```

**R equivalent:**
```r
library(fixest)
model <- feols(y ~ x1 + x2 | firm + year,
               data = df,
               cluster = ~firm + year)  # TWO separate variables, not interaction!
```

**Critical:** `cluster = ~firm + year` is two-way clustering on SEPARATE dimensions, NOT `firm × year` interaction.

---

### Winsorization

**Stata:**
```stata
winsor2 var, replace cuts(1 99)  /* Winsorize at 1st and 99th percentile */
```

**R equivalent:**
```r
library(DescTools)
df <- df %>%
  mutate(var = Winsorize(var, probs = c(0.01, 0.99)))
```

---

## Testing Your Translation

Before running full analysis, always test edge cases:

```r
# Test 1: Row dropping
df_test <- data.frame(row = 1:1000)
df_dropped <- df_test[-(820:996), ]  # Should have 823 rows (1000 - 177)
stopifnot(nrow(df_dropped) == 823)

# Test 2: Empty string vs NA
df_test <- data.frame(
  item = c("A", "B", "C"),
  value = c(NA, "", "100")
)
df_filtered <- df_test %>% filter(is.na(value) | value != "")
stopifnot(nrow(df_filtered) == 2)  # Should keep "A" (NA) and "C" ("100")

# Test 3: Hierarchical structure preservation
# Verify that category headers with NA are preserved through filtering
```

---

## When to Suspect Translation Bugs

1. **Results are systematically too low** → Check row dropping logic (issue #1)
2. **Results are exactly zero** → Check NA handling (issue #2) or hierarchical structure (issue #3)
3. **Sample size is wrong** → Check filtering conditions and NA handling
4. **Results differ between years using same methodology** → Check if filters are removing different amounts of data

---

## References

These patterns were discovered during replication of Hottman & Monarch (2020, JIE), where:
- Issue #1 caused 40% underestimation in 1998 (items at row 2834+ were deleted)
- Issue #2 caused ExpShare2014 to be zero (header row was dropped)
- Issue #3 caused all crosswalk items to have zero expenditure (Mean rows not linked to categories)

All three bugs were silent—code ran without errors, but produced wrong results.
