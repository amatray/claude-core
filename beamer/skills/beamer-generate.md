# Beamer Generate Skill

This skill orchestrates the complete workflow for generating a Beamer presentation from bullet-point outlines.

## When to Use

Use this skill when the user provides:
- Research outline with bullet points
- Target presentation length (e.g., "20-minute talk", "job talk seminar")
- Available results (graphs, tables, figures)

## Output Structure

The skill generates a modular presentation with this file structure:

```
presentation/
├── main.tex                    # Master file (compile this)
├── preamble.tex               # Standard preamble
└── sections/                  # Section files
    ├── 00_title.tex
    ├── 01_introduction.tex
    ├── 02_motivation.tex
    ├── 03_data.tex
    ├── 04_empirical_strategy.tex
    ├── 05_results.tex
    ├── 06_conclusion.tex
    └── 99_thankyou.tex
```

**Benefits:**
- Easy to work on specific sections independently
- Compilation errors point to specific files
- Better for version control and collaboration
- Simple to reorder or temporarily disable sections

**To compile:** Always compile `main.tex` using:
```bash
bash ~/claude-workflows/claude-core/beamer/scripts/compile_beamer.sh main.tex
```

## Workflow

This skill coordinates the producer-critic agent loop to create polished presentations.

### Phase 1: Architecture (Structure Planning)

**Agent**: Beamer Architect (producer)

**Input from user:**
- Research outline with bullet points
- Target presentation length
- Key results to highlight

**Architect creates:**
- Frame-by-frame outline
- Content allocation
- Progressive reveal planning
- Timing estimates

**Output**: Structured outline document

---

**Agent**: Beamer Structure-Critic (critic)

**Reviews:**
- Logical flow
- Slide density and pacing
- Section balance
- Engagement risks

**Output**: Critical review with severity-rated issues

---

**Iteration**: If Structure-Critic finds Critical or Important issues, Architect revises. Loop continues until approval.

---

### Phase 2: Writing (LaTeX Generation)

**Agent**: Beamer Writer (producer)

**Input**: Approved frame-by-frame outline with file organization plan

**Writer creates:**
- `main.tex` with section structure and \input statements
- Separate `.tex` files for each section in `sections/` directory
- Complete LaTeX code for each frame
- Frame separators between frames (`%-------...`)
- Proper style command usage
- Progressive reveal syntax
- Formatted equations and tables

**Output**: Complete modular LaTeX presentation (main.tex + section files)

---

**Agent**: Beamer Style-Critic (critic)

**Reviews:**
- Style command correctness
- Color usage conventions
- Pattern compliance
- Notation standards

**Output**: Style compliance report

---

**Iteration**: If Style-Critic finds Critical violations, Writer fixes. Loop continues until compliance.

---

### Phase 3: Styling (Final Polish)

**Agent**: Beamer Stylist (producer)

**Input**: Style-compliant LaTeX code

**Stylist perfects:**
- Spacing and alignment
- Overlay optimization
- Hyperlink network
- Visual consistency

**Output**: Polished, production-ready LaTeX

---

**Agent**: Beamer Technical-Critic (critic)

**Reviews:**
- Compilation viability
- File references
- Cross-references
- LaTeX warnings

**Output**: Technical validation report

---

**Iteration**: If Technical-Critic finds errors, Stylist fixes. Loop continues until validation passes.

---

### Phase 4: Compilation and Delivery

**Final output:**
- Complete .tex file with preamble
- Compiled PDF (if compilation successful)
- List of required graphics files
- Implementation notes

## User Interaction Points

### At Start

Ask user for:
1. **Presentation context**: "Is this for a 20-minute conference talk, 45-minute seminar, or 60-minute job talk?"
2. **Content source**: "Please provide your research outline in bullet points."
3. **Results availability**: "Which graphs and tables do you have ready? (Provide file paths if available)"
4. **Special requirements**: "Any specific sections to emphasize or de-emphasize?"

### After Architecture Phase

Present outline to user:
```
I've created a structure with [X] slides for your [length] presentation.

Main sections:
- Introduction & Motivation: [X] slides
- Empirical Strategy: [X] slides
- Results: [X] slides
- Mechanism/Robustness: [X] slides
- Conclusion: [X] slides

The Structure-Critic identified [Y] issues:
- [Summary of Critical/Important issues]

Would you like me to:
1. Proceed with this structure
2. Revise based on critic feedback
3. Make specific changes you suggest
```

### After Writing Phase

Show sample frames:
```
I've written LaTeX for all [X] frames. Here are a few examples:

[Show 2-3 representative frames - e.g., title, main result, conclusion]

The Style-Critic found [Y] style issues, which I've corrected.

Shall I proceed to final polish?
```

### After Styling Phase

Present final product:
```
Your presentation is ready!

Files created:
- [presentation_name].tex (main file)
- Required graphics: [list of paths]

Technical validation: [Pass/Issues found]

Would you like me to:
1. Compile the PDF now
2. Make any adjustments
3. Generate compilation script
```

## Output Structure

Create this file structure:

```
[presentation_name]/
├── main.tex (complete presentation)
├── 0_packages.tex (preamble, automatically included)
├── README.md (instructions for use)
├── figures/ (directory for graphics)
│   └── [list required files]
└── compile.sh (compilation script)
```

## Success Criteria

Presentation is complete when:
- [ ] Structure approved by Structure-Critic
- [ ] Style approved by Style-Critic
- [ ] Technical validation passed
- [ ] All required files identified
- [ ] Compilation instructions provided
- [ ] User confirms satisfaction

## Error Handling

If any phase fails repeatedly (>3 iterations):
1. **Report to user**: Explain the persistent issue
2. **Suggest alternatives**: Offer manual intervention points
3. **Provide partial output**: Give best-effort result with notes on problems

## Example Usage

```
User: "I need a 20-minute conference presentation. Here's my outline: [bullet points]"

Skill executes:
1. Architect creates 18-slide structure
2. Structure-Critic reviews → 2 issues found
3. Architect revises → Structure-Critic approves
4. Writer generates LaTeX for all 18 frames
5. Style-Critic reviews → 5 violations found
6. Writer fixes violations → Style-Critic approves
7. Stylist polishes all frames
8. Technical-Critic validates → 1 missing file warning
9. Stylist notes missing file → Technical-Critic passes

Output: Complete presentation with notes about required figure file
```

## Integration with Claude Code

This skill should be invokable as:

```
/beamer-generate
```

Or with the Skill tool:

```
Skill("beamer-generate")
```

## Notes

- **Time estimate**: Full generation takes 5-15 minutes depending on complexity
- **Iteration limit**: Max 3 rounds per critic to prevent infinite loops
- **User control**: User can skip critic reviews if desired (but not recommended)
- **Incremental delivery**: Show progress after each phase completion

---

**Goal**: Deliver a complete, polished, style-compliant Beamer presentation ready for use.
