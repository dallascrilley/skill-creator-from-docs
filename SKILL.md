---
name: skill-creator
description: |
  This skill provides comprehensive guidance for creating effective Claude Code skills with templates,
  best practices, and validation. It should be used when creating new skills, improving existing ones,
  validating skill quality and structure, or troubleshooting skill discovery issues.

  Use when: building Claude Code skills, creating SKILL.md files, validating skill structure,
  packaging skills for distribution, implementing evaluation-driven development (EDD), applying
  progressive disclosure, troubleshooting skill discovery, fixing YAML frontmatter, or learning
  skill best practices.

  Keywords: skill creation, skill-creator, creating skills, build skill, new skill, SKILL.md,
  YAML frontmatter, skill validation, skill templates, skill packaging, EDD, evaluation-driven
  development, progressive disclosure, init_skill.py, validate_skill.py, package_skill.py,
  skill not discovered, invalid YAML, frontmatter missing, skill best practices, skill standards,
  multi-model testing, Haiku Sonnet Opus, skill compliance
license: MIT
---

# Skill Creator

**Purpose**: Complete reference documentation (loaded when skill triggers)  
**If you're new**: Start with [00_START_HERE.md](00_START_HERE.md)  
**If you need quick start**: Use [QUICK_WORKFLOW.md](QUICK_WORKFLOW.md)

Create high-quality skills that extend Claude's capabilities through modular, self-contained packages of specialized knowledge, workflows, and tools.

## Helper Scripts

Run scripts with `--help` first to see usage options. Scripts are designed as black-box tools to minimize context usage.

- `scripts/init_skill.py` - Initialize new skill from template
- `scripts/validate_skill.py` - Validate skill quality and structure
- `scripts/package_skill.py` - Package skill for distribution
- `scripts/analyze_conciseness.py` - Analyze token usage and verbosity
- `scripts/quick_validate.py` - Quick validation for basic checks

---

## Prerequisites

**Required:**
- Python ≥ 3.7
- Access to skill-creator scripts

**Recommended:**
- Perplexity MCP for research (see setup below)
- GitHub access for pattern analysis

**Optional Python Packages:**
- `tiktoken` (for `analyze_conciseness.py`)
- `pyyaml` (for validation scripts)

Install optional packages:
```bash
pip install tiktoken pyyaml
```

### MCP Tooling Setup

**Perplexity MCP** (required for research workflow):
- **What it is**: Model Context Protocol server for Perplexity search
- **Installation**: Follow [Perplexity MCP setup guide](https://github.com/modelcontextprotocol/servers/tree/main/src/perplexity-mcp)
- **Authentication**: Requires Perplexity API key (get from [Perplexity API settings](https://www.perplexity.ai/settings/api))
- **Usage**: `perplexity_search_web "<query>" --recency 365`

**Alternative if MCP unavailable**: Use Perplexity web interface and manually document findings in research log.

---

## What Are Skills?

Skills are modular packages that transform Claude from general-purpose to specialized agent.

**Skills Provide:**
- Specialized workflows (multi-step procedures)
- Tool integrations (file formats, APIs)
- Domain expertise (company-specific knowledge, schemas)
- Bundled resources (scripts, references, assets)

**Anatomy:**
```
skill-name/
├── SKILL.md (required, < 500 lines)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions (imperative form)
└── Resources (optional)
    ├── scripts/     - Executable code
    ├── references/  - Documentation loaded as needed
    └── assets/      - Files used in output
```

**Progressive Disclosure:**
1. **Metadata** (name + description) - Always loaded
2. **SKILL.md** - Loaded when skill triggers (< 500 lines)
3. **Resources** - Loaded as Claude determines need

---

## Core Principles

1. **Concise is Key** - Claude is smart; only add what's missing
2. **Evaluations First** - Test → Gaps → Minimal docs → Re-test
3. **Match Freedom to Fragility** - High/medium/low specificity based on task
4. **Scripts Solve, Don't Punt** - Explicit error handling with fallbacks
5. **Test All Models** - Haiku, Sonnet, and Opus compatibility

See [Core Principles](references/core_principles.md) for detailed examples.

---

## Common Anti-Patterns to Avoid

### ❌ Over-Explaining Basics
```markdown
PDF files are documents that contain text and images.
To work with PDFs, you need to understand...
```

### ✅ Concise and Actionable
```markdown
Extract PDF text with pdfplumber:
\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`
```

### ❌ Vague Descriptions
```yaml
description: Helps with documents
```

### ✅ Specific with Trigger Terms
```yaml
description: Extract text from PDFs, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### ❌ Verbose Instructions
```markdown
First, you'll need to install the library. Then you can use it...
```

### ✅ Direct Instructions
```markdown
Install: `pip install pdfplumber`

Use:
\`\`\`python
import pdfplumber
...
\`\`\`
```

---

## Skill Creation Process

### Process Checklist

**REQUIRED:** Create a tracking checklist for each item before starting.

**What is TodoWrite?** TodoWrite is a tool for creating structured task lists in Claude conversations. If unavailable, use any tracking method (checklist file, issue tracker, or manual notes).

**Create checklist items:**
```
- [ ] Step 1: Research & Plan (Perplexity MCP + GitHub, create evaluations, plan structure, extract patterns)
- [ ] Step 2: Initialize from template (with --auto-fill --create-research-log)
- [ ] Step 3: Build resources (scripts/references/assets, delete boilerplate)
- [ ] Step 4: Write SKILL.md content (frontmatter, instructions, resource references)
- [ ] Step 5: Validate & Measure (token efficiency ≥50%, full validation, package)
- [ ] Step 6: Test & Iterate (multi-model testing, refine based on gaps)
```

**Why tracking is mandatory:**
- Ensures systematic approach
- Prevents skipped steps
- Provides visible progress
- Maintains quality checkpoints

**For comprehensive phase-based checklist:** See [Comprehensive Checklist](references/comprehensive_checklist.md) for detailed quality gates, time estimates, and maintenance requirements.

---

## Step 1: Research & Plan

### 1.1: Mandatory Research (Perplexity + GitHub)

**Research is mandatory for first-time builders.** If you're already an expert in the domain and have verified current package versions, you may skip to Step 1.2 (Create Test Evaluations).

**Mandatory research workflow (for first-time builders):**
1. **Query Perplexity MCP for up-to-date commands, endpoints, and documentation.**
   - Run at least two `perplexity_search_web "<platform> common commands <current year>" --recency 365` style queries that target official docs, CLI usage, REST endpoints, changelog notes, and pricing/limits.
   - Capture the latest stable version, 3-5 canonical commands/endpoints, authentication or rate-limit requirements, and deep links to docs with timestamps. Focus on common commands, critical parameters, and request/response patterns.
   - Log findings (with citations) while completing the [Research Protocol](references/research_protocol.md) so every skill starts with verified, current data.
   - Example queries:
     ```bash
     perplexity_search_web "jira automation api common endpoints 2025" --recency 365
     perplexity_search_web "jira automation api authentication cli" --recency 365
     ```
2. **Analyze at least one relevant GitHub repository and extract lessons/patterns/takeaways.**
   - Use Perplexity or GitHub search to locate an actively maintained repo (recent commits within 24 months) that uses the same API/platform you are targeting.
   - Review README plus key implementation files (scripts/, workflows/, examples/) and record ≥3 lessons, patterns, or takeaways (auth flows, error handling, pagination, testing, project layout), noting exact file paths.
   - Document how those insights will influence your skill's scripts/references before proceeding.
3. **Archive and surface the research.**
   - Store Perplexity summaries and GitHub insights in `planning/research-logs/<skill-name>.md` (or `references/research_log.md` if skill-specific) and reference it inside SKILL.md wherever the research informs guidance.
   - Highlight blockers, risky assumptions, and anything requiring validation downstream so later contributors can re-run the research quickly.

**Gather 3-5 concrete examples** of how the skill will be used, informed by the research above.

**Questions to ask:**
- What functionality should this skill support?
- What would users say to trigger this skill?
- Who is the target user? (developer, analyst, etc.)

**Quality Checkpoint:** See [Research Checklist](ONE_PAGE_CHECKLIST.md#research-checklist) and [Pre-Build Checklist](ONE_PAGE_CHECKLIST.md#pre-build-checklist)
- [ ] Perplexity research log includes commands/endpoints, doc links, and timestamps
- [ ] ≥1 GitHub repo analyzed with ≥3 lessons/patterns/takeaways captured
- [ ] 3-5 concrete examples documented
- [ ] Target user persona identified
- [ ] Trigger phrases noted

### 1.2: Create Test Evaluations (EDD)

**CRITICAL:** Create evaluations BEFORE extensive documentation.

1. **Baseline Testing** - Run Claude WITHOUT skill, document struggles
2. **Create 3-5 Scenarios** - Convert Step 1.1 examples
3. **Document Gaps** - Categorize: information, efficiency, quality
4. **Define Success Criteria** - Clear metrics per scenario

**Quality Checkpoint:** See [EDD Checklist](ONE_PAGE_CHECKLIST.md#evaluation-driven-development-edd-checklist)
- [ ] 3-5 test scenarios created
- [ ] Baseline testing completed
- [ ] Gaps categorized
- [ ] Success criteria defined

See [Evaluation-Driven Development](references/evaluation_driven_development.md) for complete methodology.

### 1.3: Plan Skill Structure

Plan scripts, references, and assets needed.

**Quick Decision Guide:**
- **Repeated code?** → scripts/
- **Detailed docs Claude references?** → references/
- **Files for output?** → assets/

See [Detailed Process Steps](references/detailed_process_steps.md) for planning decision trees and examples.

**Quality Checkpoint:**
- [ ] Scripts identified
- [ ] References planned
- [ ] Assets determined

### 1.4: Extract Patterns from Examples

Search `examples/` folder for similar skills.

```bash
ls examples/document-skills/  # For document processing
ls examples/               # For other skill types
```

**Document findings:**
- Script patterns
- Reference organization
- Asset usage
- Workflow structure

See [Detailed Process Steps](references/detailed_process_steps.md) for search strategies.

### 1.5: Plan Resource Contents

Analyze examples to determine specific resources:

**Examples:**
- **PDF Rotation** → Need `scripts/rotate_pdf.py`
- **Web App Builder** → Need `assets/hello-world/` templates
- **Database Queries** → Need `references/schema.md`

**Quality Checkpoint:**
- [ ] Resources address identified gaps
- [ ] Progressive disclosure planned if > 300 lines

---

## Step 2: Initialize from Template

**Create TodoWrite checklist** from process above, then initialize:

**Recommended: Full automation**
```bash
python scripts/init_skill.py <skill-name> --path <path> \
  --template skill-skeleton --auto-fill --create-research-log
```

**This command:**
- Creates skill structure from template
- Auto-fills [TODO:] placeholders (--auto-fill)
- Creates research log file (--create-research-log)
- Reduces manual work by ~70%

**Alternative: Basic initialization**
```bash
# If you prefer manual control
python scripts/init_skill.py <skill-name> --path <path> \
  --template skill-skeleton
```

**Templates:**
- `skill-skeleton` - Universal template with all optional sections (default, recommended for complex skills)
- `minimal-skeleton` - Simplified template with core sections only (for straightforward skills)

**Template provides:**
- [TODO:] placeholders for easy customization
- Section markers indicating what to keep vs delete
- Best practices built-in

**Flags:**
- `--auto-fill` - Automatically replace [TODO: ...] placeholders with skill name, display name, status, and date
- `--create-research-log` - Create `planning/research-logs/<skill-name>.md` with starter template
- `--display-name "Custom Name"` - Override default title-cased skill name
- `--status "Production Ready"` - Set status label (default: Beta)

**Quality Checkpoint:** See [Initialization Checklist](ONE_PAGE_CHECKLIST.md#initialization-checklist)
- [ ] Template initialized
- [ ] All placeholders identified (or auto-filled)
- [ ] Optional sections marked for deletion

---

## Step 3: Build Resources

Create scripts, references, and assets based on Step 1 planning.

**Scripts:**
- Solve problems, don't punt to Claude
- Explicit error handling with fallbacks
- Document usage clearly

**Example:**
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ''
```

**Delete template boilerplate** so only intentional resources remain:
- Remove placeholder docs like `references/example-reference.md`, `references/template.md`
- Delete unused starter scripts/assets (e.g., `scripts/example_script.py`, `assets/sample-output/`)
- Run `git status` to confirm only files you plan to customize remain

**Quality Checkpoint:** See [Bundled Resources Checklist](ONE_PAGE_CHECKLIST.md#bundled-resources-checklist)
- [ ] Scripts created with error handling
- [ ] References organized and referenced in SKILL.md
- [ ] Assets tested and functional
- [ ] Template boilerplate deleted

---

## Step 4: Write SKILL.md Content

**Frontmatter:**
- `name`: Lowercase with hyphens (gerund form preferred)
- `description`: Specific, includes trigger terms (< 1024 chars, third-person)

**SKILL.md Content:**
- Imperative/infinitive form: "To do X, run Y" not "You should do X"
- < 500 lines total
- Examples for complex operations
- Clear resource references

**Customization:**
- Fill in all [TODO:] markers with your content
- Delete sections marked with `<!-- DELETE if ... -->` that don't apply
- Keep core sections (Quick Start, Critical Rules, Common Patterns)
- See [Template Guide](templates/README.md) for detailed customization guidance

**Quality Checkpoint:** See [YAML Frontmatter Checklist](ONE_PAGE_CHECKLIST.md#yaml-frontmatter-checklist) and [SKILL.md Body Checklist](ONE_PAGE_CHECKLIST.md#skillmd-body-checklist)
- [ ] Frontmatter complete
- [ ] Imperative voice used
- [ ] < 500 lines
- [ ] Progressive disclosure applied
- [ ] All [TODO:] markers replaced

See [Editing Guidance](references/editing_guidance.md) for detailed best practices.

---

## Step 5: Validate & Measure

**Before packaging, measure and document skill value:**

### Token Efficiency Measurement

**Required:** Demonstrate ≥50% token savings over manual approach.

1. **Baseline** (without skill): Run representative task, measure tokens/errors/time
2. **With Skill**: Same task with skill loaded, measure tokens/errors/time
3. **Calculate**: Token savings %, error prevention %, time savings %
4. **Document**: In SKILL.md or README with evidence

See [Token Efficiency Guide](references/token_efficiency.md) for complete measurement methodology.

**Minimum Thresholds:**
- Token savings: ≥ 50%
- Error prevention: 100% of documented errors
- Known issues: Documented with source links

**Quality Checkpoint:** See [Token Efficiency Checklist](ONE_PAGE_CHECKLIST.md#token-efficiency-checklist) and [Validation Checklist](ONE_PAGE_CHECKLIST.md#validation-checklist)
- [ ] Token efficiency measured (≥50% savings)
- [ ] Known issues documented with sources (GitHub issues, docs, etc.)
- [ ] Error prevention verified (100% of documented errors)

### Package and Validate

```bash
# Validate first
python scripts/validate_skill.py --full-check <skill-dir>

# Then package
python scripts/package_skill.py <skill-dir>
```

**Validation stages:**
1. Structure validation
2. Best practices check
3. Content quality review
4. Token efficiency check

**Quality Checkpoint:** See [Validation Checklist](ONE_PAGE_CHECKLIST.md#validation-checklist) and [Packaging Checklist](ONE_PAGE_CHECKLIST.md#packaging-checklist)
- [ ] All validation passes
- [ ] Package created successfully

---

## Step 6: Test & Iterate

**Multi-Model Testing:**
- **Haiku**: Enough guidance?
- **Sonnet**: Clear and efficient?
- **Opus**: Avoids over-explaining?

**Iteration Process:**
1. Test with scenarios from Step 1.1
2. Observe where Claude struggles
3. Improve systematically
4. Re-validate

**Quality Checkpoint:** See [Testing Checklist](ONE_PAGE_CHECKLIST.md#testing-checklist) and [Quality Gates Checklist](ONE_PAGE_CHECKLIST.md#quality-gates-checklist)
- [ ] Tested with 3+ scenarios
- [ ] All models tested
- [ ] Validation re-run
- [ ] Improvements verified

See [Multi-Model Testing](references/multi_model_testing.md) for complete protocol.

---

## Validation Command Reference

| Command | When to Use | What It Checks |
|---------|-------------|----------------|
| `--check-structure` | After init | Directory layout, required files |
| `--check-content` | During editing | Writing style, progressive disclosure |
| `--full-check` | Before packaging | All quality checks combined |
| `--check-init` | After template copy | Template properly initialized |

**Usage:**
```bash
# During development
python scripts/validate_skill.py --check-content <skill-dir>

# Before packaging
python scripts/validate_skill.py --full-check <skill-dir>
```

---

## When to Create a Skill vs. Using Prompts

**Create a skill when:**
- Information needed repeatedly across conversations
- Same code/scripts rewritten > 3 times
- Domain knowledge is organization-specific
- Multi-step workflows require consistency

**Use prompts when:**
- One-off or infrequent tasks
- Requirements change frequently
- Task easily explained in context

---

## Migrating Existing Skills

If upgrading older skills to current standards, see [MIGRATION_GUIDE.md](references/MIGRATION_GUIDE.md) for:

- **Frontmatter Updates**: Converting to standard YAML format with required fields
- **Directory Restructuring**: Moving to official structure (scripts/, references/, assets/)
- **Content Modernization**: Applying progressive disclosure and conciseness principles
- **Validation Fixes**: Resolving common compliance issues
- **Discovery Optimization**: Adding comprehensive keywords and trigger terms

The migration guide provides step-by-step instructions for bringing legacy skills up to official Anthropic standards.

---

## Troubleshooting

Common issues and solutions:

- **Skill not discovered**: Add trigger terms to description
- **Too verbose**: Move content to references/, apply progressive disclosure
- **Scripts fail**: Implement "solve don't punt" error handling
- **Validation fails**: Check error messages, fix specific issues

See [Troubleshooting Guide](references/troubleshooting.md) for complete solutions.

---

## Quick Reference

### Key Quality Targets
- **SKILL.md**: < 500 lines, < 5000 tokens
- **Description**: < 1024 characters
- **Token Efficiency**: ≥ 50% savings over manual approach
- **Error Prevention**: 100% of documented errors
- **Multi-Model**: Tested with Haiku, Sonnet, and Opus
- **Progressive Disclosure**: Use references/ for details > 300 lines

### Essential Commands
```bash
# Initialize (recommended: full automation)
python scripts/init_skill.py <skill-name> --path <path> \
  --template skill-skeleton --auto-fill --create-research-log

# Validate
python scripts/validate_skill.py --full-check <skill-dir>

# Analyze
python scripts/analyze_conciseness.py <skill-dir>

# Package
python scripts/package_skill.py <skill-dir>
```

### Available Templates
- **skill-skeleton** - Universal template with [TODO: ...] placeholders, all optional sections (default, recommended for complex skills)
- **minimal-skeleton** - Simplified template with core sections only (for straightforward skills)

**Note:** Choose `skill-skeleton` for complex skills needing optional sections. Choose `minimal-skeleton` for simple skills. Customize by deleting sections you don't need. See [Template Guide](templates/README.md) for customization examples.

See [Template Guide](templates/README.md) for details

### Resource Guide

**Planning & Process:**
- [Comprehensive Checklist](references/comprehensive_checklist.md) - Phase-based checklist with quality gates and time estimates
- [Research Protocol](references/research_protocol.md) - Pre-build research with log template and red flags
- [Detailed Process Steps](references/detailed_process_steps.md) - In-depth guidance for each step

**Core Methodology:**
- [Core Principles](references/core_principles.md) - Detailed philosophy with examples
- [Evaluation-Driven Development](references/evaluation_driven_development.md) - Complete EDD methodology
- [Token Efficiency](references/token_efficiency.md) - Measurement methodology and ≥50% threshold

**Content & Quality:**
- [Editing Guidance](references/editing_guidance.md) - Writing and style best practices
- [Progressive Disclosure](references/progressive_disclosure.md) - Managing content size
- [Best Practices Checklist](references/best_practices_checklist.md) - Topic-based quality reference
- [Pattern Library](references/patterns.md) - Proven skill patterns

**Auto-Activation Systems:**
- [Auto-Activation Patterns](references/auto_activation_patterns.md) - Production patterns from skill-developer for building skills with trigger systems, hook mechanisms, and enforcement strategies

**Testing & Troubleshooting:**
- [Multi-Model Testing](references/multi_model_testing.md) - Testing protocol
- [Troubleshooting Guide](references/troubleshooting.md) - Common issues and solutions

### Examples
- Document processing: `examples/document-skills/pdf/`
- API integration: `examples/mcp-builder/`
- Analysis workflows: `examples/document-skills/analyzing-financial-statements/`

---

## Summary

**Process:** 1 (Research & Plan) → 2 (Initialize) → 3 (Build Resources) → 4 (Write Content) → 5 (Validate & Measure) → 6 (Test & Iterate)

**Principles:** Concise, evaluations-first, match freedom to fragility, scripts solve, test all models

**Quality Thresholds:**
- Content: < 500 lines, < 5000 tokens
- Efficiency: ≥ 50% token savings
- Error Prevention: 100% of documented errors
- Testing: All 3 models (Haiku, Sonnet, Opus)

**Key Resources:**
- [Comprehensive Checklist](references/comprehensive_checklist.md) - TodoWrite-ready phase checklist
- [Research Protocol](references/research_protocol.md) - Mandatory Perplexity + GitHub workflow (log queries + repo takeaways)
- [Token Efficiency](references/token_efficiency.md) - Measurement & ≥50% threshold

Start with template, immediately remove boilerplate, run Perplexity MCP + GitHub research before writing, then test systematically with EDD. Measure value. Iterate based on feedback.
