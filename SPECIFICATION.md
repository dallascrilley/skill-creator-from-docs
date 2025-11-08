# skill-creator-from-docs — Specification

## Mission Statement

Automate the creation of high-quality, documentation-based Claude Code skills that provide:
- **Usable templates** extracted and synthesized from documentation examples
- **Automated guardrails** to prevent common pitfalls
- **Workflow orchestration** through scripts and checklists
- **Self-validating outputs** via test scripts and validation checklists

## Target Documentation Types

- **CLI tools** (e.g., crawl4ai, uv, gh)
- **API/SDK references** (REST APIs, Python libraries, Node packages)
- **All documentation formats:** single-page, multi-page sites, versioned docs

## Core Workflow

### Phase 1: Documentation Acquisition
**Input:** URLs or markdown files
**Process:**
1. If URLs provided → Use `crawl4ai-cli` skill to extract documentation
2. Ask user to specify key pages/sections for focused analysis
3. Crawl everything first, then filter based on relevance
4. Store raw documentation in research log

**Output:** Structured documentation corpus

### Phase 2: Documentation Analysis
**Process:**
1. Identify tool type (CLI, API, library, framework)
2. Extract common workflows and use cases
3. Collect all code examples verbatim
4. Identify patterns across multiple examples
5. Note ambiguities, gaps, or unclear sections
6. Flag advanced features mentioned but not explained

**Output:** Analysis document with:
- Workflow patterns identified
- Example code catalog
- Gap analysis
- Pitfall warnings from docs

### Phase 3: Research & Clarification
**Triggers:**
- Documentation ambiguity detected
- LLM hits roadblock developing scripts/templates
- Advanced features mentioned but unexplained
- Common use cases implied but not documented

**Process:**
1. Use Perplexity MCP to research gaps
2. Document findings in research log with rationale
3. Determine if findings are:
   - **Generally useful** → Incorporate into final skill
   - **Task-specific** → Keep in research log only
4. If research fails → Request human review

**Output:** Research log + clarified understanding

### Phase 4: Template Synthesis
**Process:**
1. Extract examples verbatim first
2. Test basic validity (syntax, structure)
3. Identify patterns across examples
4. Create generalized templates (basic/advanced as appropriate)
5. Add inline comments for every parameter/section
6. Synthesize examples into practical, usable forms

**Template Requirements:**
- Inline parameter explanations
- Default values where sensible
- Variable placeholders clearly marked
- Usage examples included

**Output:** Template files ready for use

### Phase 5: Guardrails Creation
**Multi-layered approach:**

**Layer 1: Inline Warnings (in templates)**
```bash
# ⚠️ PITFALL: This will fail if API_KEY is not set
# ⚠️ COMMON ERROR: Users forget to escape special chars in $INPUT
```

**Layer 2: Pre-flight Validation Scripts**
```bash
#!/bin/bash
# validate_prereqs.sh - Run before main commands
check_api_key() { ... }
check_dependencies() { ... }
validate_input_format() { ... }
```

**Layer 3: Checklists**
```markdown
## Before Running
- [ ] API key configured in environment
- [ ] Input file exists and is readable
- [ ] Network connectivity available
```

**Layer 4: Automated Boilerplates**
Scripts that handle common tasks automatically:
- Setup/initialization with error handling
- Input validation built-in
- Common pitfalls prevented by default
- "Solve once" approach for repetitive guards

**Output:** Complete guardrail system

### Phase 6: Support Assets Creation
**Based on use case, generate:**

1. **Setup/Installation Scripts**
   - Dependency installation
   - Environment configuration
   - Verification steps

2. **Configuration Templates**
   - `.toolnamerc` files
   - Environment variable templates
   - Config with sensible defaults

3. **Troubleshooting Decision Trees**
   - Common error → diagnosis → solution
   - "If X fails, check Y" flowcharts

4. **Quick Reference Cards**
   - Command cheatsheets
   - Parameter reference tables
   - Common workflow recipes

**Output:** Complete support file set

### Phase 7: Test & Validation Creation
**Three-tier validation:**

1. **Automated Test Scripts**
   - Verify templates are syntactically valid
   - Test basic execution paths
   - Validate configuration files
   - Not required for skill creation, but generated

2. **Validation Checklists**
   - Manual verification steps for user
   - Success criteria per workflow
   - Edge cases to test

3. **Example Usage Scenarios**
   - Real-world use case walkthroughs
   - Expected outputs
   - Common variations

**Output:** Complete test suite

### Phase 8: SKILL.md Generation
**Use specialized template for documentation-based skills**

**Structure:**
```markdown
---
name: tool-name
description: |
  [Auto-generated from doc analysis]

  Use when: [extracted from common workflows]

  Prevents X documented issues: [from pitfall analysis]

  Keywords: [from documentation + common queries]
---

# Tool Name — [Brief Description]

## Overview
[What it does, when to use it]

## Quick Start
[Simplest possible usage]

## Common Workflows
[Extracted and validated patterns]

## Templates
[Reference to template files with inline docs]

## Guardrails & Validation
[Reference to validation scripts and checklists]

## Troubleshooting
[Decision trees and common issues]

## Advanced Usage
[Complex patterns, if applicable]

## Research Notes
[Link to research log for transparency]
```

**Output:** Complete SKILL.md file

### Phase 9: Validation & Packaging
**Process:**
1. Run `validate_skill.py` on generated SKILL.md
2. Verify all referenced files exist
3. Test template execution (basic)
4. Generate final validation checklist for user
5. Create research log summary

**Output:** Valid, complete skill ready for use

## File Structure

```
skill-name/
├── SKILL.md                          # Main skill file
├── RESEARCH_LOG.md                   # What was researched and why
├── templates/                        # Usable templates
│   ├── basic-usage.sh
│   ├── advanced-workflow.sh
│   └── config-template.yaml
├── scripts/                          # Automation helpers
│   ├── validate_prereqs.sh
│   ├── setup.sh
│   └── troubleshoot.sh
├── checklists/                       # Manual validation
│   ├── pre-flight.md
│   ├── validation.md
│   └── troubleshooting.md
├── tests/                            # Automated validation
│   ├── test_templates.sh
│   └── validate_config.py
└── docs/                             # Support documentation
    ├── quick-reference.md
    └── troubleshooting-tree.md
```

## Key Differentiators from Base skill-creator

1. **Documentation-first:** Starts with docs, not abstract requirements
2. **Automated extraction:** Uses crawl4ai-cli for web docs
3. **Research-augmented:** Uses Perplexity MCP for gap-filling
4. **Template synthesis:** Creates usable artifacts from examples
5. **Multi-layered guardrails:** Prevents pitfalls automatically
6. **Self-validating:** Generates tests alongside templates

## Success Criteria

A successful skill creation produces:
- [ ] Valid SKILL.md passing validate_skill.py
- [ ] At least 1 working template per common workflow
- [ ] Guardrails for all documented pitfalls
- [ ] Automated tests for template validity
- [ ] Manual validation checklist for user
- [ ] Research log documenting decisions
- [ ] Quick reference for common tasks

## Non-Goals

- Generating skills for undocumented tools (require human input)
- Creating skills from incomplete/stub documentation
- Supporting binary/proprietary tools without public docs
- Replacing human judgment in skill design decisions
