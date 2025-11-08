# skill-creator-from-docs - Design Document

**Date**: 2025-11-07
**Status**: Design Phase
**Purpose**: Specialized skill creator optimized for documentation-driven skill development

---

## Problem Statement

**Current workflow inefficiency:**
When creating skills from existing documentation (markdown files, API specs, cheat sheets), the standard skill-creator workflow requires:
- Redundant research (Perplexity/GitHub) when docs already exist
- Manual extraction of commands, workflows, and gotchas
- Unclear boundaries between scripts/, references/, and SKILL.md content
- No systematic approach to detecting optimal use cases

**Result**: Suboptimal skills that miss key patterns, lack convenience wrappers, and don't surface gotchas effectively.

---

## Solution: Documentation-First Skill Creation

### Core Philosophy

**KNOWLEDGE vs ACTION separation:**
- **Knowledge** → `references/` (what Claude should know)
- **Action** → `scripts/` + SKILL.md workflows (what Claude should do)
- **Gotchas** → Surfaced prominently in SKILL.md
- **Examples** → `assets/templates/`

### Input → Output Transformation

```
INPUT
├── Markdown docs (primary)
├── JSON API specs (supported)
├── Mixed formats (supported)
└── URLs (via crawl4ai-cli integration)
    ↓
PARSING & CATEGORIZATION (automated)
├── Commands/APIs detected → candidate scripts/
├── Sequential steps detected → workflows in SKILL.md
├── Warnings/errors detected → gotchas section
├── Code examples detected → templates in assets/
└── Reference content detected → references/
    ↓
SCAFFOLDING (semi-automated)
├── Generate script stubs with --help integration
├── Extract workflows into SKILL.md procedures
├── Surface gotchas prominently
├── Create templates from examples
└── Condense references with progressive disclosure
    ↓
VALIDATION (automated)
├── Verify all commands have wrappers or references
├── Verify gotchas are surfaced (not buried)
├── Verify templates embody best practices
└── Verify Knowledge vs Action separation
    ↓
OUTPUT: Production-ready skill
```

---

## Key Differentiators from Standard skill-creator

| Feature | standard skill-creator | skill-creator-from-docs |
|---------|----------------------|------------------------|
| **Step 1** | Research (Perplexity/GitHub) | Parse existing docs |
| **Pattern Detection** | Manual extraction | Automated detection |
| **Script Boundaries** | Unclear | Auto-detect commands → scaffold |
| **Examples** | Manual creation | Template generation from docs |
| **Gotchas** | User identifies | Auto-detect warnings/errors |
| **--help Integration** | Not enforced | Mandatory for CLI tools |
| **URL Scraping** | Manual | crawl4ai-cli integration |
| **Approval Flow** | N/A | Semi-automated (suggest → approve) |

---

## Workflow Design

### Phase 1: Input & Parsing

**Input sources:**
1. **Local files** (primary)
   - Markdown files (`*.md`)
   - JSON API specs (`*.json`)
   - Mixed formats (YAML, TXT, HTML)

2. **URLs** (via crawl4ai-cli)
   - Official documentation sites
   - API reference pages
   - GitHub README/wiki pages

**Parsing strategy:**
```python
# Parse documentation to detect patterns
patterns = {
    'commands': [],      # CLI commands, API endpoints
    'workflows': [],     # Sequential step procedures
    'gotchas': [],       # Warnings, common errors, limitations
    'examples': [],      # Code samples, templates
    'references': []     # Tables, schemas, reference content
}
```

**Detection rules:**
- **Commands**: Lines containing `$`, backticks with CLI syntax, API endpoint patterns
- **Workflows**: Numbered lists, "First... then... finally..." patterns
- **Gotchas**: "⚠️", "Warning", "Don't", "Common error", GitHub issue references
- **Examples**: Code blocks, "example:", "template:"
- **References**: Tables, schemas, long lists (> 10 items)

### Phase 2: Auto-Scaffolding

**Script generation for detected commands:**

```python
# For each detected command, generate wrapper script
def generate_script_wrapper(command_info):
    """
    Input: {
        'name': 'wp-post-get',
        'command': 'wp post get {id}',
        'params': ['id'],
        'flags': ['--field', '--format']
    }

    Output: scripts/wp_post_get.py with:
    - --help integration (runs wp post --help first)
    - Error handling
    - Convenience functions
    - Usage documentation
    """
```

**Workflow extraction:**

```python
# Extract sequential procedures into SKILL.md
def extract_workflows(doc_content):
    """
    Input: "First install, then configure, then test"

    Output: SKILL.md section:
    ## Quick Start
    1. Install: `pip install package`
    2. Configure: Run `scripts/setup_config.py`
    3. Test: `scripts/verify.py`
    """
```

**Gotcha surfacing:**

```python
# Surface warnings prominently
def surface_gotchas(detected_gotchas):
    """
    Input: ["Don't use X in production", GitHub issue #123]

    Output: SKILL.md section:
    ## ⚠️ Common Pitfalls
    - **Don't use X in production** - causes Y error
      - Fix: Use Z instead
      - Source: [GitHub Issue #123]
    """
```

### Phase 3: Semi-Automated Approval

**User reviews and approves:**
1. **Detected patterns** - Review parsed commands, workflows, gotchas
2. **Suggested scaffolds** - Approve/reject script stubs
3. **Template suggestions** - Approve/modify generated templates
4. **Structure plan** - Approve/adjust SKILL.md organization

**Interactive prompts:**
```bash
python scripts/init_from_docs.py wordpress-cli \
  --docs ./wp-cli-cheatsheet.md \
  --interactive

# Prompts:
# [1/5] Detected 12 commands. Generate scripts for all? [Y/n/select]
# [2/5] Found 3 workflows. Include all in Quick Start? [Y/n]
# [3/5] Detected 5 gotchas. Surface prominently? [Y/n]
# [4/5] Found 7 examples. Create templates? [Y/n/select]
# [5/5] Review structure plan...
```

### Phase 4: Validation

**Automated checks:**
```python
# Validation criteria specific to doc-driven skills
validation_checks = [
    'all_commands_have_wrappers_or_references',
    'gotchas_surfaced_not_buried',
    'templates_embody_best_practices',
    'knowledge_vs_action_separated',
    'help_integration_for_cli_tools',
    'progressive_disclosure_applied',
    'token_efficiency_measured'
]
```

---

## Specialized Scripts

```
skill-creator-from-docs/
├── scripts/
│   ├── parse_docs.py              # Parse docs, detect patterns
│   ├── detect_commands.py         # Find CLI/API patterns
│   ├── detect_workflows.py        # Find sequential procedures
│   ├── detect_gotchas.py          # Find warnings/errors
│   ├── detect_examples.py         # Find code samples
│   ├── generate_script_stubs.py   # Create script wrappers
│   ├── extract_workflows.py       # Convert to SKILL.md format
│   ├── surface_gotchas.py         # Create gotchas section
│   ├── generate_templates.py      # Create assets from examples
│   ├── condense_references.py     # Apply progressive disclosure
│   ├── init_from_docs.py          # Main orchestrator
│   └── validate_doc_skill.py      # Doc-specific validation
```

---

## Script Design: Key Components

### 1. `parse_docs.py` - Documentation Parser

**Responsibilities:**
- Accept multiple input formats (MD, JSON, YAML, HTML)
- Detect and categorize content patterns
- Return structured data for downstream processing

**Input:**
```bash
python scripts/parse_docs.py \
  --input ./docs/*.md \
  --input ./api-spec.json \
  --output parsing-results.json
```

**Output:**
```json
{
  "commands": [
    {
      "name": "wp post get",
      "syntax": "wp post get {id} [--field=<field>]",
      "params": ["id"],
      "flags": ["--field", "--format"],
      "source_file": "wp-cli-cheatsheet.md",
      "line_number": 42
    }
  ],
  "workflows": [
    {
      "name": "Quick Start",
      "steps": ["Install", "Configure", "Test"],
      "source_file": "getting-started.md",
      "line_number": 15
    }
  ],
  "gotchas": [
    {
      "warning": "Don't use --force in production",
      "severity": "high",
      "fix": "Use --force-with-lease instead",
      "source": "GitHub Issue #123",
      "source_file": "warnings.md",
      "line_number": 67
    }
  ],
  "examples": [...],
  "references": [...]
}
```

### 2. `generate_script_stubs.py` - Script Scaffolding

**Responsibilities:**
- Generate script wrappers for detected commands
- Include --help integration
- Add error handling patterns
- Create usage documentation

**Template:**
```python
#!/usr/bin/env python3
"""
{SCRIPT_NAME} - {DESCRIPTION}

Auto-generated from documentation by skill-creator-from-docs.
Customize error handling and add convenience functions as needed.

Usage:
    python {script_name}.py --help
    python {script_name}.py {args}
"""

import argparse
import subprocess
import sys


def get_help():
    """Run {command} --help to get latest documentation."""
    try:
        result = subprocess.run(
            ["{command}", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error getting help: {e}", file=sys.stderr)


def {function_name}({params}):
    """Execute {command} with error handling."""
    cmd = ["{command}", *{command_args}]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return None

        return result.stdout

    except subprocess.TimeoutExpired:
        print(f"Error: Command timed out", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("--help-command", action="store_true",
                       help="Show {command} --help output")
    # Add detected parameters and flags
    {arg_definitions}

    args = parser.parse_args()

    if args.help_command:
        get_help()
        sys.exit(0)

    result = {function_name}({params})
    if result:
        print(result)
    else:
        sys.exit(1)
```

### 3. `init_from_docs.py` - Main Orchestrator

**Responsibilities:**
- Coordinate all parsing and generation steps
- Present approval prompts (semi-automated flow)
- Generate final skill structure
- Run validation

**Usage:**
```bash
# Basic usage
python scripts/init_from_docs.py wordpress-cli \
  --docs ./wp-cli-cheatsheet.md

# With multiple sources
python scripts/init_from_docs.py jira-automation \
  --docs ./jira-docs.md \
  --docs ./jira-cheatsheet.md \
  --api-spec ./jira-api.json

# With URL scraping (crawl4ai-cli integration)
python scripts/init_from_docs.py stripe-payments \
  --url https://stripe.com/docs/api \
  --docs ./stripe-notes.md

# Fully automated (skip approval prompts)
python scripts/init_from_docs.py tool-name \
  --docs ./docs.md \
  --auto-approve
```

**Interactive approval flow:**
```
📋 Step 1/6: Parsing documentation...
✅ Parsed 3 files: wp-cli-cheatsheet.md, wp-cli-notes.md, api-reference.json

📋 Step 2/6: Detected patterns
   Commands: 12 found
   Workflows: 3 found
   Gotchas: 5 found
   Examples: 7 found
   References: 4 found

📋 Step 3/6: Generate scripts for detected commands?
   [1] wp post get
   [2] wp post update
   [3] wp media import
   ... (12 total)

   Options:
   [Y] Generate all scripts
   [n] Skip script generation
   [s] Select individually

   Choice: s

   Select scripts to generate:
   [✓] 1. wp post get
   [✓] 2. wp post update
   [ ] 3. wp media import (manual handling preferred)
   ...

📋 Step 4/6: Include detected workflows in Quick Start?
   [1] Discovery & Backup
   [2] Upload Media
   [3] Edit Content

   [Y/n]: Y

📋 Step 5/6: Surface detected gotchas prominently?
   [1] ⚠️ Don't use --force in production
   [2] ⚠️ WPEngine blocks SCP transfers
   [3] ⚠️ Chunk files > 50KB for transfer

   [Y/n]: Y

📋 Step 6/6: Create templates from examples?
   [1] Basic post update example
   [2] Media upload with chunking
   ...

   [Y/n/s]: s

   Select templates to create:
   [✓] 1. Basic post update example
   [✓] 2. Media upload with chunking
   [ ] 3. Shortcode replacement (too specific)

🎯 Generating skill structure...
   ✅ Created scripts/ with 2 wrappers
   ✅ Created workflows in SKILL.md
   ✅ Surfaced 5 gotchas prominently
   ✅ Created 2 templates in assets/
   ✅ Condensed references/ with progressive disclosure

📊 Validation results:
   ✅ All commands have wrappers or references
   ✅ Gotchas surfaced (not buried)
   ✅ Templates embody best practices
   ✅ Knowledge vs Action separated
   ✅ --help integration present
   ⚠️  Token efficiency: Not yet measured (run after first test)

✅ Skill created: /path/to/wordpress-cli/

Next steps:
1. Review generated SKILL.md
2. Customize script error handling
3. Test with sample scenarios
4. Measure token efficiency
5. Run validation: python scripts/validate_doc_skill.py wordpress-cli/
```

---

## crawl4ai-cli Integration

**When documentation URLs provided:**

```python
# In init_from_docs.py
if args.url:
    print(f"📡 Fetching documentation from {args.url}...")

    # Use crawl4ai-cli to extract content
    import subprocess
    result = subprocess.run(
        ["crwl", args.url, "-o", "markdown"],
        capture_output=True,
        text=True
    )

    # Save to temp file for parsing
    temp_doc = f"/tmp/{skill_name}_scraped.md"
    with open(temp_doc, 'w') as f:
        f.write(result.stdout)

    # Add to docs list
    docs.append(temp_doc)

    print(f"✅ Fetched and saved to {temp_doc}")
```

**Advanced crawl4ai usage:**

```python
# For API documentation with structured extraction
if args.api_url:
    print(f"📡 Extracting API endpoints from {args.api_url}...")

    # Create extraction schema for API docs
    schema = {
        "name": "APIExtractor",
        "baseSelector": ".api-endpoint",
        "fields": [
            {"name": "method", "selector": ".method", "type": "text"},
            {"name": "path", "selector": ".path", "type": "text"},
            {"name": "description", "selector": ".description", "type": "text"}
        ]
    }

    # Save schema
    with open("/tmp/api_schema.json", 'w') as f:
        json.dump(schema, f)

    # Extract with crawl4ai
    subprocess.run([
        "crwl", args.api_url,
        "-e", "extract_css.yml",
        "-s", "/tmp/api_schema.json",
        "-o", "json"
    ])
```

---

## Validation Criteria (Doc-Specific)

### 1. All Commands Referenced or Wrapped

**Check:** Every detected command either:
- Has a script wrapper in `scripts/`, OR
- Is documented in `references/` with usage examples

**Validation:**
```python
def validate_command_coverage(parsing_results, skill_dir):
    commands = parsing_results['commands']
    scripts = os.listdir(f"{skill_dir}/scripts")
    references = read_file(f"{skill_dir}/references/commands.md")

    missing = []
    for cmd in commands:
        has_script = any(cmd['name'].replace(' ', '_') in s for s in scripts)
        has_reference = cmd['name'] in references

        if not (has_script or has_reference):
            missing.append(cmd['name'])

    return missing  # Should be empty
```

### 2. Gotchas Surfaced (Not Buried)

**Check:** Detected gotchas appear:
- In SKILL.md "Common Pitfalls" section (within first 200 lines)
- NOT buried in references/ or at end of file

**Validation:**
```python
def validate_gotcha_surfacing(parsing_results, skill_md_path):
    gotchas = parsing_results['gotchas']
    skill_content = read_file(skill_md_path)

    # Find "Common Pitfalls" or "⚠️" section
    lines = skill_content.split('\n')
    gotcha_section_line = None

    for i, line in enumerate(lines):
        if 'Common Pitfall' in line or '⚠️' in line:
            gotcha_section_line = i
            break

    if gotcha_section_line is None:
        return False, "No gotcha section found"

    if gotcha_section_line > 200:
        return False, f"Gotcha section buried at line {gotcha_section_line}"

    # Verify all high-severity gotchas are mentioned
    high_severity = [g for g in gotchas if g['severity'] == 'high']
    for gotcha in high_severity:
        if gotcha['warning'] not in skill_content:
            return False, f"Missing gotcha: {gotcha['warning']}"

    return True, "All gotchas surfaced properly"
```

### 3. Templates Embody Best Practices

**Check:** Generated templates:
- Include error handling from gotchas
- Follow detected workflow patterns
- Reference helper scripts when appropriate

**Validation:**
```python
def validate_templates(parsing_results, assets_dir):
    templates = os.listdir(f"{assets_dir}/templates")
    gotchas = parsing_results['gotchas']

    issues = []

    for template in templates:
        template_content = read_file(f"{assets_dir}/templates/{template}")

        # Check for error handling patterns from gotchas
        for gotcha in gotchas:
            if gotcha['severity'] == 'high':
                # Template should avoid the warned pattern
                if gotcha['bad_pattern'] in template_content:
                    issues.append(f"{template}: Uses warned pattern '{gotcha['bad_pattern']}'")

        # Check for script references when appropriate
        if 'subprocess' in template_content:
            # Should reference helper scripts
            if 'scripts/' not in template_content:
                issues.append(f"{template}: Could use helper script instead of direct subprocess")

    return issues  # Should be empty
```

### 4. Knowledge vs Action Separated

**Check:**
- `references/` contains knowledge (tables, schemas, reference data)
- `scripts/` contains actions (executable code)
- SKILL.md contains workflows and gotchas (actionable guidance)

**Validation:**
```python
def validate_separation(skill_dir):
    skill_md = read_file(f"{skill_dir}/SKILL.md")
    references = os.listdir(f"{skill_dir}/references")

    issues = []

    # SKILL.md should not contain large reference tables
    if count_table_lines(skill_md) > 50:
        issues.append("SKILL.md has large reference tables (move to references/)")

    # references/ should not contain executable examples
    for ref_file in references:
        content = read_file(f"{skill_dir}/references/{ref_file}")
        if '#!/usr/bin/env' in content:
            issues.append(f"{ref_file}: Contains executable code (move to scripts/)")

    return issues  # Should be empty
```

### 5. --help Integration for CLI Tools

**Check:** If skill involves CLI commands:
- Scripts include `get_help()` function
- Scripts run `{command} --help` before first use
- Help output referenced in error messages

**Validation:**
```python
def validate_help_integration(parsing_results, scripts_dir):
    if not any(c['type'] == 'cli' for c in parsing_results['commands']):
        return True, "No CLI commands detected"

    scripts = os.listdir(scripts_dir)
    issues = []

    for script in scripts:
        content = read_file(f"{scripts_dir}/{script}")

        # Check for get_help() function
        if 'def get_help()' not in content:
            issues.append(f"{script}: Missing get_help() function")

        # Check for --help flag handling
        if '--help' not in content:
            issues.append(f"{script}: No --help flag support")

    return issues  # Should be empty
```

---

## Template Structure

### Generated SKILL.md Template

```markdown
---
name: {skill-name}
description: {auto-generated from first workflow + detected commands}. Use when {auto-generated from use cases}. Keywords: {detected commands + gotcha terms}.
---

# {Skill Display Name}

**Announce:** "I'm using the {skill-name} skill to {primary use case}."

## Overview

{Auto-generated summary of what this skill does}

## When to Use

**Use this skill when:**
{Auto-generated from detected workflows}

**Don't use for:**
{Auto-generated from gotchas or user input}

## ⚠️ Common Pitfalls

{Auto-generated from detected gotchas, surfaced prominently}

## Quick Start

{Auto-generated from detected workflows}

### Step 1: {Workflow Name}

{Extracted steps with script references}

## Helper Scripts

{Auto-generated list of created scripts}

### {Script Name}

```bash
python scripts/{script_name}.py --help
```

{Script description}

## Common Patterns

{Auto-generated from detected examples}

## Troubleshooting

{Auto-generated from gotchas + common errors}

## Detailed Documentation

For comprehensive references:
- See [references/{detected-reference-1}.md] for {description}
- See [references/{detected-reference-2}.md] for {description}

## Real-World Example

{Auto-generated from first detected example}
```

---

## Success Metrics

### Efficiency Gains

**Time savings:**
- Before: 2-4 hours to create skill from docs (manual extraction)
- After: 30-60 minutes (parse → review → approve → done)
- Target: **50-70% time reduction**

**Error reduction:**
- Before: Miss 20-30% of gotchas, 10-15% of commands
- After: Catch 95%+ of gotchas, 100% of commands
- Target: **90%+ accuracy**

### Quality Improvements

**Measured by:**
1. **Command coverage**: 100% of detected commands have wrappers or references
2. **Gotcha surfacing**: 100% of high-severity gotchas in first 200 lines
3. **Token efficiency**: ≥50% savings over manual documentation reference
4. **--help integration**: 100% of CLI tools have get_help() functions
5. **Progressive disclosure**: References/ used for content > 300 lines

---

## Implementation Phases

### Phase 1: Core Parsing & Detection (Week 1)
- `parse_docs.py` - Multi-format parser
- `detect_commands.py` - CLI/API detection
- `detect_workflows.py` - Procedure extraction
- `detect_gotchas.py` - Warning detection
- `detect_examples.py` - Code sample extraction

**Deliverable:** Working parser that categorizes doc content

### Phase 2: Scaffolding & Generation (Week 2)
- `generate_script_stubs.py` - Script wrapper generation
- `extract_workflows.py` - SKILL.md workflow creation
- `surface_gotchas.py` - Gotcha section creation
- `generate_templates.py` - Asset template creation
- `condense_references.py` - Progressive disclosure

**Deliverable:** Automated scaffolding that generates skill structure

### Phase 3: Orchestration & Approval (Week 3)
- `init_from_docs.py` - Main orchestrator
- Interactive approval prompts
- crawl4ai-cli integration for URLs
- Semi-automated workflow (suggest → approve)

**Deliverable:** Working end-to-end skill creation from docs

### Phase 4: Validation & Testing (Week 4)
- `validate_doc_skill.py` - Doc-specific validation
- Test with 3-5 existing skills (wordpress-management, etc.)
- Measure efficiency gains and quality improvements
- Iterate based on feedback

**Deliverable:** Production-ready skill-creator-from-docs

---

## Open Questions

1. **Parser accuracy**: How well can we detect workflows vs gotchas vs examples?
   - **Answer**: Start with regex patterns, refine with LLM classification if needed

2. **Script generation scope**: Generate full implementations or stubs only?
   - **Answer**: Stubs with error handling templates, user customizes

3. **Approval granularity**: How interactive should semi-automated flow be?
   - **Answer**: Default to Y (approve all), allow selective with -s flag

4. **crawl4ai schema**: Pre-built schemas for common doc sites, or always custom?
   - **Answer**: Start with generic, build library of presets over time

5. **Token efficiency**: How to measure without running full scenarios?
   - **Answer**: Estimate based on references/ size vs inline documentation

---

## Next Steps

1. ✅ **Design review** - Approve this design document
2. **Prototype parser** - Build parse_docs.py with multi-format support
3. **Test detection** - Run against wordpress-management docs, measure accuracy
4. **Build orchestrator** - Create init_from_docs.py with approval flow
5. **Validate approach** - Create 1-2 skills from docs, compare to manual
6. **Iterate and productionize** - Refine based on real usage

---

**End of Design Document**
