# Beamer Production Workflow

## At the Start of Every Beamer Task

**ALWAYS ASK**: "Should I use orchestrator mode for this task?"

Wait for user response:
- **"Yes"** / **"orchestrator"** → Use Mode 2 (Orchestrator)
- **"No"** / **"simple"** → Use Mode 1 (Simple)
- **No response / user continues with instructions** → Default to Mode 1 (Simple)

---

## Mode 1: Simple (One Feedback Round)

**Use when**: Small edits, adding a few slides, quick tasks, routine work

**Process**:
1. **Producer generates** initial content
2. **Critic reviews** and identifies violations (with score)
3. **Producer fixes** those specific violations (one time only)
4. **Done** - no further iteration

**Output**: Improved content + critic's final report

**Example flow**:
```
User: "Add slides for Section 5"
Assistant: "Should I use orchestrator mode for this task?"
User: "No" or "simple" or [continues with details]
→ Producer generates slides
→ Critic reviews: "Score 85/100, found 3 violations"
→ Producer fixes those 3 violations
→ DONE
```

**Advantages**:
- Fast (one round)
- Good for small tasks
- You maintain control

**Limitations**:
- Might not catch all issues
- Final score may be below 95
- No guarantee of perfection

---

## Mode 2: Orchestrator (Iterative Loop)

**Use when**: Generating full sections from scratch, important presentations, need high quality, complex new content

**Process**:
1. **Producer generates** initial content
2. **Critic reviews** and calculates score
3. **Check stop conditions**:
   - If score ≥95 → ✅ DONE
   - If iterations ≥5 → ❌ DONE (max reached)
   - Otherwise → continue
4. **Producer fixes** violations from critic feedback
5. **Repeat** steps 2-4 until stop condition met
6. **Final summary** with pass/fail status

**Output**: Polished content + iteration summary showing progress

**Parameters**:
- Max iterations: **5**
- Score threshold: **≥95/100**
- Stop when: `(score ≥95) OR (iterations ≥5)`

**Example flow**:
```
User: "Generate full Section 5 on geopolitical considerations"
Assistant: "Should I use orchestrator mode for this task?"
User: "Yes" or "orchestrator"

→ Iteration 1/5: Producer generates → Critic: 78/100 (5 violations)
→ Iteration 2/5: Producer fixes → Critic: 88/100 (2 violations)
→ Iteration 3/5: Producer fixes → Critic: 96/100 ✅ PASS

Summary: PASSED after 3 iterations. Final score: 96/100
```

**Advantages**:
- High quality output (score ≥95)
- Catches and fixes issues iteratively
- Systematic refinement

**Limitations**:
- Takes longer (up to 5 rounds)
- Uses more tokens
- May still fail to reach 95 after 5 iterations (edge cases)

---

## Agent Architecture

### Producer Agents (3)

1. **Content Writer** (`beamer-content-writer.md`)
   - Generates semantic content with color markup
   - Outputs: `[[term::color]]` format
   - Reviewed by: Style Critic

2. **Template Assembler** (`beamer-template-assembler.md`)
   - Converts content to LaTeX using exact templates
   - Mechanical, deterministic work
   - Reviewed by: Layout Critic

3. **Equation Writer** (`beamer-equation-writer.md`)
   - Creates equation slides with progressive reveals
   - Handles overlay logic and color transitions
   - Reviewed by: Style Critic + Layout Critic + Equation Critic

### Critic Agents (3)

1. **Style Critic** (`beamer-style-critic.md`)
   - Reviews color semantics and patterns
   - Checks over-coloring, consistency
   - Reviews: ALL content (from all producers)

2. **Layout Critic** (`beamer-layout-critic.md`)
   - Reviews technical dimensions and spacing
   - Checks minipage sizes, margins, alignment
   - Reviews: Template Assembler + Equation Writer output

3. **Equation Critic** (`beamer-equation-critic.md`)
   - Reviews overlay logic and synchronization
   - Checks equation-text coordination, coverage gaps
   - Reviews: ONLY Equation Writer output

### Review Matrix

| Producer Agent | Style Critic | Layout Critic | Equation Critic |
|----------------|--------------|---------------|-----------------|
| Content Writer | ✅ | ❌ | ❌ |
| Template Assembler | ✅ | ✅ | ❌ |
| Equation Writer | ✅ | ✅ | ✅ |

**Key insight**: Equation slides are reviewed by ALL THREE critics because they involve:
- Color semantics (Style)
- Minipage dimensions (Layout)
- Overlay logic (Equation)

## Detailed Process Flows

### Simple Mode (Mode 1)

```
START
  ↓
User provides task
  ↓
Assistant asks: "Should I use orchestrator mode?"
  ↓
User: "No" / "simple" / [continues]
  ↓
[PRODUCER AGENT(S)]
- Content Writer: Generates semantic content
- Template Assembler: Converts to LaTeX
- Equation Writer: Creates equation slides (if needed)
  ↓
[CRITIC AGENT(S)]
- Style Critic: Reviews colors/semantics
- Layout Critic: Reviews dimensions/spacing
- Equation Critic: Reviews overlay logic (if equation slides)
- Calculates score (100 - violations)
- Returns: Score, violations list
  ↓
[PRODUCER AGENT(S) - FIX ROUND]
- Reads violations from critics
- Fixes specific violations only
- Returns updated file
  ↓
END
```

### Orchestrator Mode (Mode 2)

```
START
  ↓
User provides task
  ↓
Assistant asks: "Should I use orchestrator mode?"
  ↓
User: "Yes" / "orchestrator"
  ↓
ITERATION = 1
  ↓
[PRODUCER AGENT(S)]
- If iteration = 1: Generate from scratch
  * Content Writer → semantic content
  * Template Assembler → LaTeX conversion
  * Equation Writer → equation slides (if needed)
- If iteration > 1: Fix violations from previous critic feedback
- Returns updated file
  ↓
[CRITIC AGENT(S)]
- Style Critic: Reviews colors/semantics
- Layout Critic: Reviews dimensions/spacing
- Equation Critic: Reviews overlay logic (if equation slides)
- Aggregates scores from all critics
- Returns: Combined Score, Status (PASS/FAIL), violations list by critic
  ↓
[CHECK STOP CONDITIONS]
- If ALL scores ≥ 95 → Go to SUCCESS
- If iteration ≥ 5 → Go to FAILURE
- Otherwise → ITERATION++, return to PRODUCER AGENT(S)
  ↓
SUCCESS:
  ↓
Output summary:
  Status: PASSED ✅
  Final Scores:
    - Style: [X]/100
    - Layout: [Y]/100
    - Equation: [Z]/100 (if applicable)
  Iterations: [N]/5
  END
  ↓
FAILURE:
  ↓
Output summary:
  Status: FAILED ❌
  Final Scores:
    - Style: [X]/100
    - Layout: [Y]/100
    - Equation: [Z]/100 (if applicable)
  Iterations: 5/5
  Remaining violations by critic: [list]
  END
```

---

## Scoring System (Used by Critic)

**Start at 100 points**, deduct for violations:

### Critical violations (-10 points each):
- Figure environment using `\hspace*{-1.cm}` and `{1.3\textwidth}` (causes title misalignment)
- Missing `\centering` in figure columns
- Side-by-side figure columns instead of full-page overlays
- Missing `\vfill` before first item `[1.]` when intro outside itemize
- Missing `\bigskip` before intro text outside itemize
- Frame title >80 characters without splitting

### Important violations (-5 points each):
- Wrong color category (blue vs green vs red)
- Inconsistent color application
- Wrong number coloring
- Standalone bold instead of colors
- Parentheses incorrectly colored lightgrey
- Wrong figure height specification

### Minor violations (-2 points each):
- Uneven spacing in itemize lists
- Missing `\pause` between major sections
- Inconsistent use of `\bitem`, `\mitem`, `\vitem`
- Thank you slide format not matching template
- Over-coloring text

**Pass threshold**: ≥95 (max 5 points deductions)

---

## When to Use Each Mode

### Use Simple Mode (Mode 1) for:
- Adding 1-3 slides to existing presentation
- Small edits to existing content
- Fixing specific issues
- Quick iterations during development
- When you want to maintain control and review after each change

### Use Orchestrator Mode (Mode 2) for:
- Generating entire new sections (5+ slides)
- Creating presentations from scratch
- Important presentations for conferences/meetings
- When quality is critical and you want systematic refinement
- When you're not sure what violations might exist
- Final polish before presentation delivery

---

## Example Conversations

### Example 1: Simple Mode

```
User: "Add a slide showing Figure X in Section 3"