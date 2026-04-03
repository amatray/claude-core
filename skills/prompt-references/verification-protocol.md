# Verification Protocol for Model Derivations

*Consult this file before running verification checks on flagged derivation steps. Each `% VERIFY`-flagged step receives all three local checks. Oracle re-derivation is applied only to user-selected critical steps.*

---

## Check A — Dimensional Consistency

**Procedure:**
1. Assign a unit label to every variable using the model's notation table.
2. For each side of the equation, compute the composite unit.
3. Verify: units(LHS) = units(RHS).

**Standard unit assignments (macro):**

| Variable type | Units | Example |
|---------------|-------|---------|
| Output, capital, consumption | Goods [$G$] | $Y, K, C$ |
| Labor | Labor [$L$] | $L, N$ |
| Goods price | [$\$/G$] | $p$ |
| Wage | [$\$/L$] | $w$ |
| Interest/rental rate | [dimensionless, per period] | $r$ |
| Discount factor | [dimensionless] | $\beta$ |
| Share parameters | [dimensionless] | $\alpha, \theta$ |
| Lagrange multiplier | Inherits from constraint — units of objective per unit of constraint slack | $\lambda, \mu$ |

**Common traps:**
- $r$ is dimensionless but $rK$ has units [$G$/period] only if $r$ is the rental rate; financial returns may differ
- Mixing stock variables (measured at a point) with flow variables (measured per period)
- Lagrange multipliers: $\lambda$ on a budget constraint in goods has units [utils/$G$]; $\mu$ on a collateral constraint $b \leq \theta k$ is [utils/$G$] if the objective is in utils and the constraint in goods
- Forgetting that $\delta k$ has the same units as $k$ (goods), not dimensionless

**Output format:**
```
Dimensional check: PASS/FAIL
  LHS units: [unit expression]
  RHS units: [unit expression]
  Details: [explanation if FAIL]
```

---

## Check B — Limiting Cases

**Procedure:**
1. Identify the key parameter(s) in the flagged expression.
2. Evaluate the expression as the parameter approaches its boundary values:
   - $\theta \to 0$ and $\theta \to 1$ (for share/friction parameters in $[0,1]$)
   - $\theta \to 0$ and $\theta \to \infty$ (for unbounded parameters)
   - Any other natural boundary from the model's domain restrictions
3. Verify each limit matches the known special case or economic intuition.

**What to verify at each limit:**
- Does the expression reduce to a known benchmark? (e.g., frictionless first-best when constraint parameter → 0)
- Is the limit finite when it should be? Infinite when it should be?
- Does the limit respect non-negativity and domain constraints?
- For CES-type expressions: does $\sigma \to 1$ yield Cobb-Douglas? Does $\sigma \to \infty$ yield linear?

**Common traps:**
- Claiming a limit "goes to zero" without checking whether the denominator also goes to zero (0/0 forms)
- Forgetting that a binding constraint in the limit may change the relevant case
- Ignoring that some limits require L'Hopital or Taylor expansion

**Output format:**
```
Limiting case check: PASS/FAIL
  Parameter: [name] → [limit value]
  Expression evaluates to: [result]
  Expected (intuition): [what it should be and why]
  Match: YES/NO
```

---

## Check C — Numerical Spot-Check

**Procedure:**
1. Select parameter values from the appropriate table below (or user-provided values).
2. Substitute into LHS and RHS of the equation separately.
3. **Execute via Python** — do NOT compute in-context. Use:
   ```bash
   python3 -c "lhs = <expr>; rhs = <expr>; print(f'LHS={lhs:.6f} RHS={rhs:.6f} DIFF={abs(lhs-rhs):.2e}')"
   ```
4. PASS if $|\text{LHS} - \text{RHS}| < 10^{-6}$ (equalities) or if inequality direction is correct.

**Important:** For FOCs and equilibrium conditions, first solve for consistent endogenous values at the given parameters before checking. Do not plug in arbitrary values for endogenous variables — they must satisfy the model's equations.

### Parameter Tables

**Macro (baseline):**

| Parameter | Value | Source |
|-----------|-------|--------|
| $\alpha$ (capital share) | 0.33 | Gollin (2002) |
| $\beta$ (annual discount) | 0.96 | Standard |
| $\delta$ (depreciation) | 0.10 | Standard annual |
| $\sigma$ (CRRA) | 2.0 | Standard |
| $\gamma$ (Frisch elasticity) | 0.5 | Chetty et al. (2011) |
| $A$ (TFP, normalized) | 1.0 | Normalization |
| $r$ (interest rate) | 0.04 | Standard annual |

**Trade:**

| Parameter | Value | Source |
|-----------|-------|--------|
| $\tau$ (iceberg cost) | 1.3 | Anderson & van Wincoop (2004) |
| $f_x$ (fixed export cost) | 0.5 | Calibrated |
| $\kappa$ (Pareto shape) | 4.25 | Chaney (2008) |
| $\sigma_{\text{CES}}$ (elasticity of substitution) | 4.0 | Broda & Weinstein (2006) |
| $f_e$ (entry cost) | 1.0 | Normalization |
| $L$ (labor endowment) | 1.0 | Normalization |

**Finance:**

| Parameter | Value | Source |
|-----------|-------|--------|
| $\theta$ (pledgeability) | 0.5 | Rampini & Viswanathan (2010) |
| $\sigma_z$ (productivity volatility) | 0.15 | Standard |
| $r_f$ (risk-free rate) | 0.02 | Standard |
| $\phi$ (leverage ratio) | 0.4 | Typical |
| $\lambda_{\text{adj}}$ (adjustment cost) | 0.5 | Cooper & Haltiwanger (2006) |

---

## Verification Log Template

Use the **Verification Log Format** template from `model-solving-conventions.md`. Always show all 4 rows (Dimensional, Limiting cases, Numerical, Oracle). Steps not sent to Oracle use "NOT SELECTED."

**Per-operation granularity:** For steps with substeps (e.g., Step 4a, 4b), each substep gets its own verification log entry with all 4 rows.

---

## HALT Protocol

If ANY check returns FAIL or Oracle returns DISAGREE:

1. **Stop immediately.** Do not proceed to the next verification check or the next step.
2. **Present side-by-side:**
   ```
   ⚠️ VERIFICATION FAILURE — Step N

   ORIGINAL DERIVATION:
   [the step as written in derivation.tex]

   FAILING CHECK ([Check A/B/C]):
   [the check result with full details]

   Please adjudicate: Is the original derivation correct, or does it need correction?
   ```
3. **Wait for user decision.** Do not suggest which is correct — present both and let the user decide.
4. If user identifies an error: correct `derivation.tex` (after backing up to `.bak`), then re-run ALL checks on the corrected step before continuing.

---

## Weasel Word List

After writing `derivation.tex`, scan for these phrases. Any step containing them must be flagged with `% VERIFY` regardless of whether it matches the standard non-trivial categories:

- "clearly"
- "trivially"
- "obviously"
- "it is easy to see"
- "it can be shown"
- "straightforward"
- "by inspection"
- "by symmetry"
- "without loss of generality"
- "immediately follows"
- "one can verify that"
- "a simple calculation shows"

This list is extensible — add domain-specific phrases as needed.
