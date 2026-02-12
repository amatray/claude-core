# Markdown to PDF Export Guidelines

## Applicability

**This rule applies when:**
- Creating markdown reports that will be converted to PDF
- User asks for reports, analyses, or documentation in `.md` format
- Working on files in `output/`, `reports/`, `verification/` directories
- Creating deliverable documentation (replication reports, analysis summaries, etc.)

---

## Critical Requirements for PDF-Ready Markdown

### 1. Number ALL Tables and Figures

**Problem:** Without numbers, referencing tables/figures in text is impossible ("see table above" breaks when PDF is printed or sections are moved).

**MANDATORY FORMAT:**

```markdown
**Table 1: Descriptive Title Here**

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |

**Figure 1: Event Study Results**

![Figure description](path/to/figure.png)
```

**In-text references:**
- ✅ "Table 1 shows summary statistics..."
- ✅ "As seen in Figure 3, the effect..."
- ✅ "Results are presented in Tables 2-4"
- ❌ "The table above shows..."
- ❌ "See the figure below..."

**Numbering conventions:**
- Use **Table 1**, **Table 2**, etc. (bold the label)
- Use **Figure 1**, **Figure 2**, etc. (bold the label)
- Number sequentially throughout the document
- Include descriptive title after the number
- Separate numbering sequences for tables vs figures

**Example:**
```markdown
## Results

Our main findings are presented in Table 1. The demographic distribution
(Table 2) shows that 62.9% of households are homeowners. Figure 1 illustrates
the time trend, while Figure 2 shows the geographic distribution.

**Table 1: Summary Statistics**

| Variable | Mean | SD | N |
|----------|------|----|----|
| Income   | 50K  | 30K| 127,103 |

**Table 2: Demographic Distribution**

| Category | Share |
|----------|-------|
| Homeowner| 62.9% |
| Renter   | 37.1% |

**Figure 1: Consumption Trends Over Time**

![Trends](output/trends.png)
```

---

### 2. Replace Special Characters with LaTeX Equivalents

**Problem:** Markdown special characters (emojis, checkmarks, mathematical symbols, arrows) often fail to render in PDF or render as boxes/question marks.

**SOLUTION:** Use inline LaTeX for special characters that don't translate well.

#### Common Replacements

| ❌ Markdown | ✅ LaTeX | Renders As |
|------------|----------|------------|
| ✓ or ✔     | `$\checkmark$` | ✓ |
| ✗ or ✘     | `$\times$` | × |
| → | `$\rightarrow$` | → |
| ← | `$\leftarrow$` | ← |
| ≥ | `$\geq$` | ≥ |
| ≤ | `$\leq$` | ≤ |
| ≠ | `$\neq$` | ≠ |
| ± | `$\pm$` | ± |
| × | `$\times$` | × |
| ÷ | `$\div$` | ÷ |
| ∞ | `$\infty$` | ∞ |
| 🚨 🔥 ⚠️ etc. | **[avoid emojis entirely]** | Use **bold**, *italic*, or CAPS |

#### Checkboxes and Status Indicators

**Instead of:**
```markdown
- [x] Completed task
- [ ] Pending task
```

**Use:**
```markdown
- $\checkmark$ Completed task
- $\times$ Pending task
```

**For status tables:**
```markdown
| Item | Status |
|------|--------|
| Data validation | $\checkmark$ PASS |
| Sample size check | $\checkmark$ PASS |
| Missing values | $\times$ FAIL |
```

#### Mathematical Expressions

Always use LaTeX for any mathematical notation:

```markdown
- Coefficient: $\beta = 0.42$ (SE = $0.05$)
- P-value: $p < 0.01$
- R-squared: $R^2 = 0.26$
- Range: $[0, 1]$
- Null hypothesis: $H_0: \beta = 0$
```

#### Emphasis Instead of Emojis

**Instead of:**
```markdown
🚨 WARNING: Critical data issue
✅ SUCCESS: All tests passed
⚠️ ALERT: Large download required
```

**Use:**
```markdown
**⚠ WARNING:** Critical data issue
**✓ SUCCESS:** All tests passed
**! ALERT:** Large download required (1.2 GB)
```

Or use LaTeX:
```markdown
**$\times$ WARNING:** Critical data issue
**$\checkmark$ SUCCESS:** All tests passed
```

---

### 3. Prevent Table Column Overflow

**Problem:** Long text in one column invades adjacent columns, making tables unreadable in PDF output.

**ROOT CAUSE:** Markdown table syntax has no built-in column width control. PDF renderers don't auto-wrap long text in table cells.

#### Solution 1: Manual Line Breaks (Simple Cases)

For moderately long text, break into multiple lines within the cell:

```markdown
| Variable | Description |
|----------|-------------|
| income_clean | Household total income,<br>range $8 to $583K,<br>median ~$50K |
| age_clean | Reference person age,<br>range 18 to 85 years |
```

**Note:** `<br>` works in most markdown-to-PDF converters (Pandoc, etc.)

#### Solution 2: Abbreviate and Use Footnotes

**Instead of:**
```markdown
| Variable | Description |
|----------|-------------|
| income_clean | Household total annual income from all sources including wages, self-employment, investments, and transfers |
```

**Use:**
```markdown
| Variable | Description |
|----------|-------------|
| income_clean | Total annual household income* |

*Includes wages, self-employment, investments, and transfers.
```

#### Solution 3: Use Narrower Columns for Codes/IDs

**Good table design:**
```markdown
| Code | Category | N | % |
|------|----------|------:|-----:|
| 8007 | Owner-occupied housing | 79,853 | 65.8% |
| 9101 | Personal insurance | 6,355 | 5.0% |
```

**Not this (ID column too wide):**
```markdown
| Category_Code_ID | Full_Category_Description | Sample_Size | Percentage_Share |
|------------------|---------------------------|-------------|------------------|
```

#### Solution 4: Transpose Wide Tables

If you have many columns with long headers, transpose the table:

**Instead of:**
```markdown
| Specification | R² (Weighted) | R² (Unweighted) | Bins (Weighted) | Bins (Unweighted) | Sample Size |
|---------------|---------------|-----------------|-----------------|-------------------|-------------|
| Income only   | 8.37%         | 6.78%           | 570             | 323               | 127,103     |
```

**Use:**
```markdown
| Metric | Income Only | Income × Age | All Demographics |
|--------|-------------|--------------|------------------|
| R² (Weighted) | 8.37% | 17.35% | 26.29% |
| R² (Unweighted) | 6.78% | 14.99% | 22.09% |
| Bins (Weighted) | 570 | 959 | 1,268 |
| Sample Size | 127,103 | 127,103 | 111,476 |
```

#### Solution 5: Split into Multiple Tables

For very complex tables, split into logical subtables:

**Instead of one massive table with 15+ columns:**

Create:
- **Table 1a: Model Specifications and Sample Sizes**
- **Table 1b: Performance Metrics (R², AIC, BIC)**
- **Table 1c: Coefficient Estimates**

#### Solution 6: Use Alignment to Your Advantage

```markdown
| Variable | Mean | SD | Min | Max | N |
|:---------|-----:|---:|----:|----:|------:|
| Income   | 50,234 | 30,122 | 8 | 583,241 | 127,103 |
| Age      | 48.5 | 17.3 | 18 | 85 | 127,103 |
```

**Alignment guide:**
- `:---` = Left align (for text, labels)
- `---:` = Right align (for numbers)
- `:---:` = Center align (for short codes, rarely needed)

Left-align text columns, right-align numeric columns. This improves readability and reduces overflow risk.

---

## Pre-Flight Checklist: Before Converting MD to PDF

Before running `pandoc` or any MD→PDF tool, verify:

**Numbering:**
- [ ] All tables have numbers: **Table 1:**, **Table 2:**, etc.
- [ ] All figures have numbers: **Figure 1:**, **Figure 2:**, etc.
- [ ] In-text references use table/figure numbers, not "above" or "below"
- [ ] Numbering is sequential (no gaps like Table 1, 2, 4)

**Special Characters:**
- [ ] No emojis (🚨 ⚠️ ✅ ❌ 🔥 etc.) — use bold/italic instead
- [ ] Checkmarks use `$\checkmark$` not ✓ or ✔
- [ ] X-marks use `$\times$` not ✗ or ✘
- [ ] All math notation in LaTeX: `$\beta$`, `$R^2$`, `$p < 0.05$`
- [ ] Arrows use LaTeX: `$\rightarrow$` not →

**Tables:**
- [ ] No single cell has >80 characters of unbroken text
- [ ] Long descriptions use `<br>` breaks or footnotes
- [ ] Column headers are short and clear
- [ ] Numeric columns are right-aligned (`---:`)
- [ ] Text columns are left-aligned (`:---`)
- [ ] Tables fit within standard page width (test with preview)

**Images:**
- [ ] All image paths are correct (relative or absolute)
- [ ] Images exist at specified paths
- [ ] Image dimensions are reasonable (<8 inches wide for portrait page)

---

## Pandoc Conversion Command (Reference)

**Basic conversion:**
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

**With custom margins and fonts:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="Times New Roman"
```

**With table of contents:**
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  -N  # Number sections
```

---

## Example: Before and After

### ❌ BEFORE (PDF will have issues)

```markdown
## Results

The table below shows summary statistics:

| Variable | Description |
|----------|-------------|
| income_clean | Household total annual income from all sources including wages, self-employment income, investment income, and government transfers, range $8 to $583,241 |
| age_clean | Age of household reference person in years |

✓ Data validation completed
✗ Missing values detected

Key finding: R² = 26.29% → shows that income matters
```

**Issues:**
- No table number (can't reference it)
- "table below" will break if content moves
- Second column text is way too long (will overflow)
- Unicode checkmark/X won't render properly
- Arrow (→) may not render properly
- Missing LaTeX for R²

---

### ✅ AFTER (PDF-ready)

```markdown
## Results

Summary statistics for key demographic variables are presented in Table 1.

**Table 1: Summary Statistics for Demographic Variables**

| Variable | Description |
|----------|-------------|
| income_clean | Household total income,*<br>range: $8 to $583K |
| age_clean | Age of reference person<br>(years) |

*Includes wages, self-employment, investments, and transfers.

**Data Quality Checks:**
- $\checkmark$ Data validation completed
- $\times$ Missing values detected (15,627 households, 12.3%)

**Key finding:** $R^2 = 26.29\%$, indicating that income is the dominant predictor of consumption patterns.
```

**Improvements:**
- Table is numbered (Table 1) and can be referenced
- Long text broken with `<br>` and footnote
- Checkmark and X using LaTeX
- R² properly formatted
- Removed problematic arrow, used clearer prose
- Professional formatting that will render correctly in PDF

---

## Summary

When creating markdown for PDF export:

1. **Always number tables and figures** — enables proper referencing
2. **Use LaTeX for special characters** — ensures correct rendering
3. **Keep table columns narrow** — prevents text overflow

Following these rules ensures your markdown documents convert cleanly to professional-looking PDFs without formatting issues or lost information.
