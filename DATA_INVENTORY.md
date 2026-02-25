# Data Inventory for Hottman & Monarch (2023) - Tables 1 & 2

## Selected Items to Replicate
- Table 1: Selected Demographic Characteristics in CE Survey (2018)
- Table 2: Share of Total Expenditure on Imports (1996, 2007, 2018)

## Required Datasets

| # | Dataset | Description | Time Period | Source | Available? | Location | File Size | Status |
|---|---------|-------------|-------------|--------|-----------|----------|-----------|--------|
| 1 | Consumer Expenditure Survey (CE) PUMD | Household-level expenditure data by UCC codes and demographics | 2012-2016 only | BLS | ⚠️ Partial | `/Users/adrienmatray/Matray Dropbox/_AdrienTeam/_Julia_Adrien/tariff_debt/data/source/CEX/` | ~500 MB | **MISSING: Need 1996, 2007, 2018** |
| 2 | U.S. Import Data (HS6 level) | Import values by HS6 product category | 1996+ available | U.S. Census | ✅ Yes | `/Users/adrienmatray/Matray Dropbox/_Source/Trade/Schott_UScustoms/imp_detl_YEAR_12n.dta` | ~178 MB (1996) | **Ready** |
| 3 | U.S. Export Data (HS6 level) | Export values by HS6 product category | 1996+ available | U.S. Census | ✅ Yes | `/Users/adrienmatray/Matray Dropbox/_Source/Trade/Schott_UScustoms/exp_detl_YEAR_12n.dta` | ~178 MB (1996) | **Ready** |
| 4 | NBER-CES Manufacturing Database | U.S. production data at NAICS-5 level | 1996-2018 (annual) | NBER | ❌ No | Not found | ~50 MB | **MISSING** |
| 5 | UCC to HS6 Concordance | Mapping between CE product codes and HS6 trade codes | 1996-2018 | Furman et al. (2017) | ✅ Yes | `/Users/adrienmatray/Matray Dropbox/_AdrienTeam/_Julia_Adrien/tariff_debt/data/source/concordance/ucc_hs6/` | ~4.5 MB total | **Ready** |
| 6 | CE Hierarchical Grouping (Stubs) | Product category structure for CE | 1997-2024 | BLS | ✅ Yes | `/Users/adrienmatray/Matray Dropbox/_AdrienTeam/_Julia_Adrien/tariff_debt/data/source/concordance/stubs/` | ~10 MB total | **Ready** |
| 7 | BEC Classification | Identifies consumer-facing goods among HS6 products | HS 2012/2017 | UN Statistics | ❌ No | Not found | <1 MB | **MISSING** |

## Notes

**Table 1** requires:
- Dataset #1 (CE PUMD) for 2018 only
- Demographic variables: AGE, EDUC_REF, MEMRACE, SEX, BLS_URBN

**Table 2** requires:
- Dataset #1 (CE PUMD) for 1996, 2007, 2018
- Datasets #2, #3, #4 to calculate import penetration rates by HS6
- Dataset #5 to map UCC codes to HS6
- Dataset #6 to filter to consumer-facing products only

**Calculation of Import Penetration Rate:**
- For each HS6 product: `Import Share = Imports / (Production - Exports + Imports)`

## ⚠️ CRITICAL DATA GAPS IDENTIFIED

### MISSING CE DATA
The CE PUMD data is only available for 2012-2016 in your Dropbox. We need:
- **1996 CE PUMD** (for Table 2)
- **2007 CE PUMD** (for Table 2)
- **2018 CE PUMD** (for Tables 1 and 2)

### MISSING OTHER DATA
- **NBER-CES Manufacturing Database** (needed to calculate import penetration rates)
- **BEC Classification file** (needed to filter consumer-facing goods)

## Options to Proceed

**Option 1: Check for replication package**
- Authors may have provided processed data files
- Check: [Ryan Monarch's website](https://sites.google.com/view/ryanmonarch/research)
- Check: Federal Reserve IFDP working paper page

**Option 2: Use available years only**
- We could replicate Table 1 and Table 2 for years 2012-2016 only
- This would be a partial replication showing the methodology works

**Option 3: Download missing CE data**
- BLS provides CE PUMD files publicly
- Files are large (~1-2 GB per year)
- Would you like me to identify download URLs?

**Option 4: Ask if you have CE data elsewhere**
- Do you have CE PUMD files in another Dropbox location?
- Do you have access to a data repository with CE microdata?

**Which option would you prefer?**
