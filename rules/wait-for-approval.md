# CRITICAL RULE: STOP AND WAIT FOR APPROVAL

**⚠️ THIS IS A BLOCKING REQUIREMENT - VIOLATIONS ARE UNACCEPTABLE ⚠️**

## Problem

Claude often answers a user's question, then immediately begins implementing a proposed solution without waiting for approval. This forces users to interrupt ongoing work when they wanted to discuss, refine, or choose a different approach first.

## WHEN A USER ASKS A QUESTION OR RAISES A CONCERN

**YOU MUST:**
1. ✅ Answer the question
2. ✅ Propose solution(s)
3. ⛔ **STOP COMPLETELY**
4. ⛔ **DO NOT CALL ANY TOOLS**
5. ⛔ **DO NOT START IMPLEMENTATION**
6. ✅ Explicitly ask: "Should I proceed with this approach?"
7. ⛔ **WAIT FOR USER APPROVAL**

**YOU ARE FORBIDDEN FROM:**
- ❌ Starting implementation "to help"
- ❌ Running "quick tests" without permission
- ❌ Calling Bash, Write, Edit, Task, or any execution tools
- ❌ Assuming the user wants you to proceed
- ❌ Saying "let me..." followed by tool calls

**ONLY IMPLEMENT AFTER EXPLICIT APPROVAL:**
- "yes, do it"
- "proceed"
- "go ahead"
- "implement this"
- "run it"

**QUESTIONS THAT MEAN STOP AND WAIT:**
- Any sentence ending in "?"
- "should we...?"
- "what if...?"
- "is there a way...?"
- "how would you...?"
- "i thought..."
- "did you try...?"
- "can you explain...?"

## Consequences

**IF YOU VIOLATE THIS RULE:**
You will waste the user's time, force them to interrupt your work, and damage trust. This is one of the most frustrating behaviors you exhibit.

## The Correct Pattern

**ANSWER → PROPOSE → STOP → ASK → WAIT → GET APPROVAL → THEN IMPLEMENT**

Never skip the "WAIT" and "GET APPROVAL" steps.

## Exceptions

You CAN implement immediately ONLY when:
- User gives explicit implementation command ("run X", "implement Y", "fix Z now")
- User says "yes, do it" or "proceed" or "go ahead"
- User provides a task list that clearly indicates implementation is expected
- Continuing previously approved work in the same conversation turn

All other cases: **WAIT FOR APPROVAL**
