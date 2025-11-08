# Skill Creator from Documentation - Comprehensive Methodology

## 🎯 PURPOSE: TRANSFORMING DOCUMENTATION INTO PRODUCTION-READY SKILLS

**This is the Python automation system for creating skills from documentation. It provides a sequential, 6-phase pipeline for standalone execution without requiring Claude Code to be active.**

## ⚡ EXECUTION MODEL: SEQUENTIAL AUTOMATION

### This System (skill-creator-from-docs)
**Sequential Python Pipeline**

```bash
python scripts/create_skill.py docs.md --skill-name tool
```

- **Architecture:** Sequential 6-phase pipeline
- **Execution:** Phases run one after another (Phase 1 → 2 → 3 → 4 → 5 → 6)
- **Parallelization:** None - reliable, predictable, deterministic
- **Requirements:** Python 3.8+, no Claude API calls for core functionality
- **Use when:** Want automation without active Claude Code session

### For Agent-Powered Execution
**Use the `doc-to-skill` skill in Claude Code instead**

When you need parallel agent execution for 2-5x speedup:
- Activate the `doc-to-skill` skill in Claude Code
- It spawns parallel agents using Task tool
- See `~/.claude/skills/doc-to-skill/SKILL.md` for details

---

## 📚 WHAT THIS GUIDE COVERS

This comprehensive methodology document explains:
- Documentation analysis methodology
- Component brainstorming framework
- Template-driven artifact generation
- Skill structure best practices
- Testing and validation workflows
- Real-world examples and patterns

## 📚 WHAT IS A DOCUMENTATION-BASED SKILL?

### Definition

A documentation-based skill is a PAI skill created by:
1. Analyzing tool/CLI/API documentation
2. Extracting common workflows and patterns
3. Identifying pitfalls and best practices
4. Creating helper scripts to automate error-prone steps
5. Designing templates for common configurations
6. Building guardrails to prevent common mistakes
7. Packaging everything into a comprehensive skill

### Documentation-Based Skills vs Manual Skills

**Documentation-Based Skills:**
- Systematic analysis of tool docs
- Helper scripts for automation
- Templates for quick setup
- Validation to prevent errors
- Comprehensive troubleshooting
- Examples from docs + LLM analysis

**Manual Skills:**
- Written from experience
- May lack automation
- Fewer templates and helpers
- Ad-hoc troubleshooting
- Examples from personal use

**Goal:** Make documentation-based skills as good as (or better than) manual skills by adding LLM-powered analysis and automation.

## 🏗️ THE SIX-PHASE METHODOLOGY

### Overview

```
Phase 1: Documentation Gathering
    ↓
Phase 2: Documentation Analysis
    ↓
Phase 3: Skill Design Brainstorming
    ↓
Phase 4: Artifact Creation
    ↓
Phase 5: SKILL.md Creation
    ↓
Phase 6: Integration & Testing
```

Each phase has specific deliverables and validation checkpoints.

---

## PHASE 1: DOCUMENTATION GATHERING

### Goal
Collect complete, clean documentation in markdown format.

### Input Methods

#### Method 1: Direct Markdown Input

User provides markdown documentation directly.

**When to use:**
- Documentation is already in markdown
- User has local docs
- Small, focused documentation

**Process:**
1. Accept markdown content
2. Verify completeness
3. Ask for missing sections if needed

**Example:**
```
User: "Here's the ripgrep documentation: [markdown content]"
Claude: "Thanks! I have the documentation. Let me analyze it..."
```

#### Method 2: URL Extraction (crawl4ai-cli)

Extract documentation from URLs using the crawl4ai-cli skill.

**When to use:**
- Online documentation
- Multiple pages to combine
- HTML documentation to convert

**Process:**
1. Identify documentation URLs
2. Use crawl4ai-cli to extract markdown:
   ```bash
   crwl https://docs.tool.com/guide -o markdown > docs.md
   ```
3. For multi-page docs, extract each page:
   ```bash
   crwl https://docs.tool.com/intro -o markdown > intro.md
   crwl https://docs.tool.com/usage -o markdown > usage.md
   crwl https://docs.tool.com/config -o markdown > config.md
   ```
4. Combine into single document

**Example:**
```
User: "Create a skill for ast-grep from https://ast-grep.github.io"
Claude: "I'll extract the documentation using crawl4ai..."
```

#### Method 3: Mixed Approach

Combine crawled content with user-provided context.

**When to use:**
- Official docs + user experience
- Documentation gaps + user knowledge
- Quick start from URLs + deep context from user

**Process:**
1. Extract base documentation
2. Ask user for context:
   - Common pitfalls they've encountered
   - Workflows they use frequently
   - Configuration patterns they recommend
3. Merge extracted docs with user insights

**Example:**
```
User: "Create a skill for ffmpeg. Docs are at https://ffmpeg.org/documentation.html but I can tell you common mistakes"
Claude: "Perfect! I'll extract the official docs and then get your insights..."
```

### Deliverable

Complete documentation in markdown format, organized by section:
- Tool overview
- Installation/setup
- Basic usage
- Advanced features
- Configuration options
- Examples
- Troubleshooting
- API/CLI reference

### Validation Checkpoint

Before proceeding to Phase 2:
- [ ] Documentation is complete and readable
- [ ] All major sections are present
- [ ] Examples are included
- [ ] Configuration options documented
- [ ] Common operations covered

---

## PHASE 2: DOCUMENTATION ANALYSIS

### Goal
Systematically extract structure, patterns, workflows, and gotchas from documentation.

### Analysis Framework

#### 1. Tool Overview Analysis

**Extract:**
- **Primary purpose**: What problem does this tool solve?
- **Key capabilities**: What are the main features?
- **Use cases**: When would someone use this tool?
- **Target audience**: Who is this tool for?

**Questions to answer:**
- What's the one-sentence description?
- What makes this tool unique?
- What are the top 3 capabilities?

**Example (ast-grep):**
```
Primary purpose: Code structural search and transformation
Key capabilities:
  - Pattern-based code search
  - AST-aware transformations
  - Multi-language support
Use cases: Refactoring, code analysis, linting
Target audience: Developers working with large codebases
```

#### 2. Command/API Pattern Analysis

**Extract:**
- **Command structure**: How are commands formed?
- **Flag patterns**: Common flag combinations
- **Parameter types**: What kinds of inputs?
- **Output formats**: What does it produce?

**For CLIs, answer:**
- What's the basic command syntax?
- What are required vs optional flags?
- What flag combinations are common?
- What's the default behavior?

**For APIs, answer:**
- What's the authentication method?
- What are the main endpoints?
- What's the request/response format?
- What are required vs optional parameters?

**Example (ripgrep):**
```
Command structure: rg [OPTIONS] PATTERN [PATH...]
Common flags:
  - -i (case insensitive)
  - -l (list files only)
  - -n (show line numbers)
  - -A/-B/-C (context lines)
Common combinations:
  - rg -i "pattern" (case-insensitive search)
  - rg -l "pattern" (find files containing pattern)
  - rg -n "pattern" -A 3 (show line numbers + 3 lines after)
```

#### 3. Workflow Analysis

**Extract:**
- **Standard workflows**: Multi-step processes from docs
- **Task sequences**: Common operation orders
- **Dependencies**: What needs to happen first?

**Look for:**
- "Getting started" sections
- "Quick start" guides
- Tutorial workflows
- Multi-step examples

**Document each workflow:**
1. Name and purpose
2. Prerequisites
3. Step-by-step process
4. Expected output
5. Common variations

**Example (Docker):**
```
Workflow: Build and Deploy Container

Prerequisites:
- Dockerfile exists
- Docker installed
- Registry credentials (if pushing)

Steps:
1. Build image: docker build -t myapp:1.0 .
2. Test locally: docker run -p 8080:80 myapp:1.0
3. Tag for registry: docker tag myapp:1.0 registry.com/myapp:1.0
4. Push to registry: docker push registry.com/myapp:1.0
5. Deploy: docker run -d -p 80:80 registry.com/myapp:1.0

Expected output: Container running on port 80

Variations:
- Development: Skip push, run locally
- Production: Add volume mounts, environment vars
```

#### 4. Pitfalls & Gotchas Analysis

**Critical section! This drives guardrails and validation.**

**Extract:**
- **Explicit warnings** from docs ("Warning:", "Note:", "Important:")
- **Common mistakes** sections
- **Prerequisites** often forgotten
- **Error-prone areas** mentioned
- **Version-specific issues**
- **Platform differences**

**LLM Analysis - Anticipate additional pitfalls:**
- What could go wrong with this command?
- What prerequisites might be missed?
- What's confusing about this API?
- What parameter combinations are invalid?
- What's the recovery process for errors?

**Document each pitfall:**
1. Description (what goes wrong)
2. Cause (why it happens)
3. Detection (how to spot it)
4. Prevention (how to avoid it)
5. Solution (how to fix it)

**Example (Python package installation):**
```
Pitfall: Installing in wrong Python environment

Description: Package installed but import fails
Cause: Multiple Python versions, wrong venv
Detection: `which python` != expected path
Prevention: Always activate venv first, verify with `which python`
Solution:
  1. Deactivate current env
  2. Activate correct env
  3. Verify with `which python`
  4. Reinstall package

Guardrail to create:
- Setup script that verifies Python version
- Validation script that checks installation
- Mandatory workflow: Verify env → Install → Test import
```

#### 5. Best Practices Analysis

**Extract:**
- **Recommended approaches** from docs
- **Performance tips**
- **Security considerations**
- **Maintainability advice**

**Look for:**
- "Best practices" sections
- "Recommendations"
- "Performance" tips
- "Security" notes
- Optimization suggestions

**Example (Git):**
```
Best Practices:

1. Commit messages
   - Use present tense
   - First line < 50 chars
   - Blank line before body
   - Explain why, not what

2. Branching
   - feature/* for features
   - bugfix/* for fixes
   - Don't commit to main directly

3. History
   - Keep commits atomic
   - Rebase before merge
   - Don't rewrite public history
```

### Analysis Deliverable Structure

Create a structured analysis document:

```markdown
# [Tool Name] Documentation Analysis

## 1. Tool Overview
[Summary from analysis]

## 2. Command/API Patterns
### Basic Syntax
[Command structure]

### Common Flags/Options
[Frequently used flags]

### Flag Combinations
[Common patterns]

## 3. Workflows
### Workflow 1: [Name]
- Prerequisites: [list]
- Steps: [numbered list]
- Expected output: [description]

### Workflow 2: [Name]
[Same structure]

## 4. Pitfalls & Gotchas
### Pitfall 1: [Name]
- Description: [what goes wrong]
- Cause: [why]
- Detection: [how to spot]
- Prevention: [how to avoid]
- Solution: [how to fix]

### Pitfall 2: [Name]
[Same structure]

## 5. Best Practices
### Category 1: [Name]
- Practice 1
- Practice 2

### Category 2: [Name]
- Practice 1
- Practice 2

## 6. Configuration Patterns
[Common config approaches]

## 7. Key Examples
[Critical examples from docs]
```

### Validation Checkpoint

Before proceeding to Phase 3:
- [ ] Tool overview is clear and concise
- [ ] Command/API patterns identified
- [ ] At least 3 workflows documented
- [ ] Pitfalls extracted and analyzed
- [ ] Best practices captured
- [ ] Configuration patterns noted
- [ ] Key examples collected

---

## PHASE 3: SKILL DESIGN BRAINSTORMING

### Goal
Design all skill components that will make the tool easy and safe to use.

### Component Categories

#### 1. Helper Scripts Design

**Purpose:** Automate error-prone or repetitive tasks.

**Brainstorming process:**

1. **Review pitfalls** - What manual steps cause errors?
2. **Review workflows** - What multi-step processes repeat?
3. **Review prerequisites** - What setup is required?

**Common helper scripts:**

**Setup/Installation Scripts:**
- Purpose: First-time tool setup
- Checks: Verify installation, dependencies, config
- Example: `setup.sh`

**Validation Scripts:**
- Purpose: Verify configurations or outputs
- Checks: Schema validation, required fields, format
- Example: `validate_config.py`

**Generator Scripts:**
- Purpose: Create configs/templates interactively
- Features: Prompts, validation, examples
- Example: `generate_config.py`

**Inspection/Debug Scripts:**
- Purpose: Troubleshoot issues
- Features: Verbose output, diagnostic checks
- Example: `inspect_state.sh`

**For each helper script, define:**
```
Name: [script name]
Purpose: [what it does]
Inputs: [what it takes]
Outputs: [what it produces]
Prevents: [what mistakes it avoids]
Template: [python or bash]

Logic outline:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

**Example (for a validation script):**
```
Name: validate_extraction.py
Purpose: Validate scraped data has required fields and correct format
Inputs: JSON file path, required fields list
Outputs: Validation report (pass/fail + details)
Prevents: Processing incomplete/malformed data

Logic outline:
1. Load JSON file
2. Check each record for required fields
3. Validate field types
4. Count records
5. Report missing/invalid data
6. Exit with status code (0 = pass, 1 = fail)

Template: helper-script.py.template
```

#### 2. Config Templates Design

**Purpose:** Provide ready-to-use configuration presets.

**Brainstorming process:**

1. **Review configuration options** from docs
2. **Identify common scenarios** (basic, advanced, specific use cases)
3. **Extract meaningful presets**

**Common template types:**

**Basic/Minimal:**
- Simplest working configuration
- Defaults for most use cases
- Heavily commented

**Advanced/Full-Featured:**
- All major options shown
- Production-ready settings
- Performance optimized

**Scenario-Specific:**
- Tailored to specific use cases
- Example: "dynamic content", "API extraction", "batch processing"

**For each template, define:**
```
Name: [template name]
Scenario: [when to use]
Key settings: [critical options]
Comments: [explanations needed]

Template structure:
[Actual config structure with placeholders]
```

**Example:**
```
Name: crawler_dynamic.yml
Scenario: JavaScript-heavy sites with lazy loading
Key settings:
  - scan_full_page: true (infinite scroll)
  - delay_before_return_html: 2.0 (wait for JS)
  - wait_until: networkidle (wait for network)

Template structure:
# Dynamic Content Configuration
# Use for: JavaScript-heavy sites, infinite scroll, lazy loading
cache_mode: "bypass"        # Force fresh crawl
wait_until: "networkidle"   # Wait for network activity to stop
page_timeout: 60000         # Max wait time (60s)
delay_before_return_html: 2.0  # Wait 2s after load for JS
scan_full_page: true        # Scroll to bottom for infinite scroll
scroll_delay: 0.5           # Time between scrolls
```

#### 3. Guardrails Design

**Purpose:** Prevent common mistakes through enforced workflows.

**Brainstorming process:**

1. **Review all pitfalls**
2. **Identify preventable errors**
3. **Design workflow requirements**

**Guardrail types:**

**Mandatory Workflows:**
- Mark as ⚠️ MANDATORY in SKILL.md
- Multi-step processes that must be followed in order
- Include "why this prevents failures"

**Prerequisite Checks:**
- Built into helper scripts
- Verify requirements before proceeding
- Clear error messages if missing

**Validation Gates:**
- Run validation before next step
- Prevent bad input propagation
- Stop early on errors

**For each guardrail, define:**
```
Type: [Mandatory workflow | Prerequisite check | Validation gate]
Purpose: [What mistake it prevents]
Trigger: [When it applies]
Implementation: [How to enforce]

Workflow/Check:
[Step-by-step or code check]

Error message: [Clear message if violated]
```

**Example:**
```
Type: Mandatory Workflow
Purpose: Prevent scraping wrong elements (navigation instead of content)
Trigger: First time scraping any new website

Workflow:
1. Inspect page first (Chrome MCP or inspect script)
2. Verify selectors target correct elements
3. Extract with validated schema
4. Run validation script on output
5. Only proceed if validation passes

Implementation:
- Mark as ⚠️ MANDATORY in SKILL.md
- Create inspect_page.sh script
- Create validate_extraction.py script
- Document in "Workflow Requirements" section

Why this prevents failures:
- Step 1 identifies correct selectors (prevents scraping navigation)
- Step 4 catches schema errors early (saves time before processing large datasets)
```

#### 4. Checklists Design

**Purpose:** Ensure nothing is forgotten.

**Checklist types:**

**First-Time Setup Checklist:**
- Installation verification
- Dependency installation
- Initial configuration
- Test run

**Pre-Execution Checklist:**
- Prerequisites met
- Configuration valid
- Environment ready
- Dry-run successful

**Troubleshooting Checklist:**
- Common issues to check
- Diagnostic steps
- Solution patterns

**Example (First-Time Setup):**
```
## First-Time Setup Checklist

- [ ] Tool is installed (`which tool`)
- [ ] Dependencies are installed (list them)
- [ ] Configuration file exists
- [ ] Configuration is valid (`validate_config.py`)
- [ ] Test run succeeds (`tool --version`)
- [ ] Example command works (`tool test-command`)
```

#### 5. Reference Structure Design

**Purpose:** Organize detailed documentation.

**Decide what goes where:**

**SKILL.md (quick reference):**
- Tool overview
- Quick start (minimal example)
- Core tasks (most common operations)
- Proven patterns (working examples)
- Troubleshooting table (quick fixes)
- Helper scripts list
- Workflow requirements (mandatory steps)
- Common workflows
- Tips

**references/ directory (detailed docs):**

**cli-reference.md / api-reference.md:**
- Complete flag/option documentation
- All parameters explained
- Return values / exit codes
- Edge cases

**config-reference.md:**
- All configuration options
- Default values
- Option interactions
- Environment variables

**patterns.md:**
- Detailed multi-step workflows
- Complete examples with explanations
- Variations and alternatives
- Integration patterns

**troubleshooting.md:**
- Common issues with full context
- Diagnostic procedures
- Detailed solutions
- Known bugs/limitations

**For each reference doc, define:**
```
File: [filename]
Purpose: [what it covers]
Sections: [major sections]
Cross-references: [links to other docs]
```

### Brainstorming Deliverable Structure

Create a skill design document:

```markdown
# [Tool Name] Skill Design

## Directory Structure
[Planned directory tree]

## Helper Scripts

### Script 1: [name]
- Purpose: [description]
- Inputs: [list]
- Outputs: [list]
- Prevents: [mistake]
- Logic: [outline]

### Script 2: [name]
[Same structure]

## Config Templates

### Template 1: [name]
- Scenario: [when to use]
- Key settings: [list]
- Structure: [outline]

### Template 2: [name]
[Same structure]

## Guardrails

### Guardrail 1: [name]
- Type: [type]
- Purpose: [description]
- Implementation: [how]

### Guardrail 2: [name]
[Same structure]

## Checklists

### First-Time Setup
[Checklist items]

### Pre-Execution
[Checklist items]

### Troubleshooting
[Checklist items]

## Reference Structure

### SKILL.md Sections
[List of sections]

### references/ Files
[List of reference docs]

## Key Principles for This Skill
[Specific principles based on tool characteristics]
```

### Validation Checkpoint

Before proceeding to Phase 4:
- [ ] At least 3 helper scripts designed
- [ ] At least 2 config templates designed
- [ ] At least 2 guardrails defined
- [ ] Checklists created
- [ ] Reference structure planned
- [ ] All designs prevent identified pitfalls

---

## PHASE 4: ARTIFACT CREATION

### Goal
Generate all skill components using templates and design specifications.

### Artifact Creation Workflow

#### Step 1: Create Directory Structure

```bash
mkdir -p ~/.claude/skills/[tool-name]/{references,scripts,templates}
```

#### Step 2: Generate Helper Scripts

**For each helper script in design:**

1. **Choose template**
   - Python scripts: `templates/helper-script.py.template`
   - Bash scripts: `templates/helper-script.sh.template`

2. **Fill in template variables**

Template variables:
```
{{SCRIPT_NAME}} - Script filename without extension
{{SCRIPT_DESCRIPTION}} - One-line description
{{SCRIPT_PURPOSE}} - Detailed purpose explanation
{{USAGE_PATTERN}} - How to invoke (e.g., "[OPTIONS] INPUT")
{{EXAMPLES}} - Usage examples
{{ARGUMENT_DEFINITIONS}} - argparse argument definitions (Python) or case statement (Bash)
{{MAIN_LOGIC}} - Core script logic
{{HELPER_FUNCTIONS}} - Supporting functions
{{ADDITIONAL_IMPORTS}} - Extra import statements (Python)
{{DEPENDENCY_CHECKS}} - Dependency verification (Bash)
```

3. **Implement custom logic**

Add tool-specific logic based on design outline:
- Input validation
- Processing steps
- Output generation
- Error handling

4. **Add helpful features**

- Verbose/debug mode
- Dry-run mode
- Color-coded output
- Progress indicators
- Clear error messages

**Example (validation script):**
```python
#!/usr/bin/env python3
"""
validate_extraction.py - Validate extracted data structure

Validates JSON extraction output to ensure required fields are present
and data types are correct.

Usage:
    python validate_extraction.py DATA.json [OPTIONS]

Examples:
    python validate_extraction.py data.json --required-fields=title,url
    python validate_extraction.py data.json --min-records=10
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def main():
    parser = argparse.ArgumentParser(
        description="Validate extracted data structure"
    )
    parser.add_argument("file", help="JSON file to validate")
    parser.add_argument("--required-fields", help="Comma-separated required fields")
    parser.add_argument("--min-records", type=int, help="Minimum record count")

    args = parser.parse_args()

    try:
        data = load_json(args.file)
        validate_structure(data)

        if args.required_fields:
            fields = args.required_fields.split(",")
            validate_required_fields(data, fields)

        if args.min_records:
            validate_record_count(data, args.min_records)

        print("✅ Validation passed")
        sys.exit(0)

    except ValidationError as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

def load_json(filepath: str) -> List[Dict]:
    """Load and parse JSON file"""
    # Implementation...

def validate_structure(data: List[Dict]) -> None:
    """Validate basic data structure"""
    # Implementation...

def validate_required_fields(data: List[Dict], fields: List[str]) -> None:
    """Check all records have required fields"""
    # Implementation...

def validate_record_count(data: List[Dict], min_count: int) -> None:
    """Verify minimum record count"""
    # Implementation...

if __name__ == "__main__":
    main()
```

5. **Make executable**
```bash
chmod +x scripts/[script-name].sh
chmod +x scripts/[script-name].py
```

#### Step 3: Create Config Templates

**For each config template in design:**

1. **Use config template**: `templates/config-template.yml.template`

2. **Fill in variables**:
```
{{CONFIG_NAME}} - Configuration name
{{CONFIG_DESCRIPTION}} - What this config is for
{{TOOL_COMMAND}} - Command that uses this config
{{CONFIG_FLAG}} - Flag to pass config (e.g., -C, --config)
{{CONFIG_SECTIONS}} - Config sections with options
```

3. **Add explanatory comments**

For each option:
- What it does
- Default value
- When to change it
- Related options

4. **Include usage example**

Show how to use this config:
```yaml
# Usage:
#   tool --config basic_config.yml input.txt
```

**Example (dynamic config):**
```yaml
# Dynamic Content Configuration
# For JavaScript-heavy sites, infinite scroll, or lazy-loaded content
#
# Usage:
#   crwl https://example.com -C crawler_dynamic.yml -o markdown

# Cache Settings
cache_mode: "bypass"  # Force fresh crawl (don't use cached version)

# Page Loading
wait_until: "networkidle"   # Wait for network activity to stop
page_timeout: 60000         # Maximum wait time in milliseconds (60 seconds)
delay_before_return_html: 2.0  # Additional delay after page load (seconds)

# Scrolling (for infinite scroll / lazy loading)
scan_full_page: true        # Automatically scroll to bottom
scroll_delay: 0.5           # Delay between scroll steps (seconds)

# Cleanup
remove_overlay_elements: true  # Remove popups, modals, etc.

# Output
verbose: true              # Show detailed progress
```

#### Step 4: Write Reference Docs

**For each reference doc in design:**

Create detailed documentation in `references/` directory.

**cli-reference.md / api-reference.md:**
```markdown
# [Tool Name] Complete Reference

## Command Structure
[Syntax explanation]

## Flags / Options

### --flag-name
**Syntax:** `--flag-name [VALUE]`
**Type:** [string|integer|boolean]
**Default:** [default value]
**Description:** [What it does]

**Examples:**
```bash
tool --flag-name value
```

**Notes:**
- [Important notes]
- [Interactions with other flags]

[Repeat for all flags]

## Exit Codes
[If applicable]

## Environment Variables
[If applicable]
```

**config-reference.md:**
```markdown
# [Tool Name] Configuration Reference

## Configuration File Format
[Format explanation]

## Configuration Options

### section_name

#### option_name
**Type:** [string|integer|boolean|object]
**Default:** `default_value`
**Description:** [What it does]

**Allowed values:**
- `value1` - [Description]
- `value2` - [Description]

**Example:**
```yaml
section_name:
  option_name: value
```

**Notes:**
- [Important notes]
- [Related options]

[Repeat for all options]
```

**patterns.md:**
```markdown
# [Tool Name] Proven Patterns

## Pattern 1: [Name]

**Use case:** [When to use this pattern]

**Prerequisites:**
- [Requirement 1]
- [Requirement 2]

**Workflow:**
```bash
# Step 1: [Description]
command1

# Step 2: [Description]
command2

# Step 3: [Description]
command3
```

**Expected output:**
[What you should see]

**Variations:**
- [Variation 1]: [How to adapt]
- [Variation 2]: [How to adapt]

**Troubleshooting:**
- If [problem], then [solution]

---

[Repeat for each pattern]
```

**troubleshooting.md:**
```markdown
# [Tool Name] Troubleshooting

## Issue 1: [Description]

**Symptoms:**
- [Symptom 1]
- [Symptom 2]

**Cause:**
[Why this happens]

**Diagnosis:**
```bash
# Check 1
diagnostic-command-1

# Check 2
diagnostic-command-2
```

**Solution:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Prevention:**
[How to avoid this issue]

---

[Repeat for each issue]
```

#### Step 5: Create scripts/README.md

Document all helper scripts:

```markdown
# [Tool Name] Helper Scripts

This directory contains helper scripts that simplify common [tool] workflows.

## Available Scripts

### setup.sh
**Purpose:** First-time installation and verification

**Usage:**
```bash
./scripts/setup.sh
```

**What it does:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

### validate_config.py
**Purpose:** [Description]

**Usage:**
```bash
python scripts/validate_config.py CONFIG_FILE
```

**Options:**
- `--option`: [Description]

---

[Repeat for each script]

## Common Workflows

### Workflow 1: [Name]
```bash
# Step 1
./scripts/script1.sh

# Step 2
python scripts/script2.py input.txt

# Step 3
./scripts/script3.sh
```

## Troubleshooting

### Script fails with [error]
**Solution:** [How to fix]
```

### Validation Checkpoint

After artifact creation:
- [ ] All helper scripts created and executable
- [ ] All config templates created
- [ ] All reference docs created
- [ ] scripts/README.md created
- [ ] All files follow naming conventions
- [ ] All templates are valid (no syntax errors)

---

## PHASE 5: SKILL.md CREATION

### Goal
Write comprehensive SKILL.md file that serves as quick reference.

### SKILL.md Structure

Use the template: `templates/tool-skill-SKILL.md.template`

#### Section 1: YAML Frontmatter

```yaml
---
name: tool-name
description: [Clear description]. Use when [use cases]. Keywords - [keywords].
---
```

**Description guidelines:**
- First sentence: What the tool does
- Second sentence: Key capabilities or methods
- Third sentence: USE WHEN triggers with examples
- Fourth sentence: Keywords for matching

**Example:**
```yaml
---
name: ast-grep
description: Structural code search and transformation using AST patterns. Supports pattern-based search, refactoring, and linting across multiple languages. USE WHEN user says 'search code structure', 'refactor code', 'AST-based search', 'structural code search', or needs syntax-aware code transformation. Keywords - ast-grep, sg, AST, structural search, code refactoring, pattern matching, syntax tree.
---
```

#### Section 2: Title and Overview

```markdown
# [Tool Name] Guide

[One-paragraph overview of what the tool does and why it's useful]

For detailed configuration options, see [references/config-reference.md](references/config-reference.md).
```

#### Section 3: Prerequisites (if needed)

```markdown
## Prerequisites

**IMPORTANT:** [Critical prerequisites]

### First-Time Setup

**Option 1: Automated Setup (Recommended)**

Run the included setup script to verify installation and configure everything automatically:

```bash
cd ~/.claude/skills/[tool-name]/scripts
./setup.sh
```

**Option 2: Manual Setup**

If you prefer to set up manually:

```bash
# Step 1: [Description]
command1

# Step 2: [Description]
command2
```

**If [tool] is not installed:**

```bash
# Installation command
install-command
```
```

#### Section 4: Quick Start

```markdown
## Quick Start

```bash
# Basic usage
tool basic-command

# Common operation 1
tool command1 --flag value

# Common operation 2
tool command2 --flag value
```
```

#### Section 5: Core Tasks

```markdown
## Core Tasks

### Task 1: [Name]

```bash
# Description of what this does
tool command --flags

# Save to file
tool command --flags > output.txt
```

**Options:**
- `--flag1` - [Description]
- `--flag2` - [Description]

### Task 2: [Name]

[Same structure]
```

#### Section 6: Command Reference

```markdown
## Command Reference

**Common flags:**
- `-f <value>` - [Description]
- `-o <format>` - Output format
- `-v` - Verbose output

**See also:** [references/cli-reference.md](references/cli-reference.md) for complete documentation.
```

#### Section 7: Configuration Files

```markdown
## Configuration Files

### Basic Configuration

```yaml
# basic_config.yml
key: value
```

Usage: `tool -c basic_config.yml`

**See also:** [references/config-reference.md](references/config-reference.md) for all options.
```

#### Section 8: Proven Patterns

```markdown
## Proven Patterns

**⚠️ MANDATORY:** For ALL patterns below, follow the [workflow](#workflow-requirements).

### Pattern: [Name]

```bash
#!/bin/bash
# [Description]

# Step 1
command1

# Step 2
command2
```
```

#### Section 9: Troubleshooting

```markdown
## Troubleshooting

**Quick fixes for common issues:**

| Issue | Solution |
|-------|----------|
| [Issue 1] | [Quick fix] |
| [Issue 2] | [Quick fix] |

**For detailed solutions:** [references/troubleshooting.md](references/troubleshooting.md)
```

#### Section 10: Helper Scripts

```markdown
## Helper Scripts

**Setup and verify:**
```bash
./scripts/setup.sh
```

**Validate configuration:**
```bash
python scripts/validate_config.py config.yml
```

[List all scripts with brief descriptions]
```

#### Section 11: Workflow Requirements

```markdown
## Workflow Requirements

**⚠️ MANDATORY: Always follow this workflow for [context]:**

1. [Step 1] - [What to do]
2. [Step 2] - [What to do]
3. [Step 3] - [What to do]

**Why this prevents failures:**
- Step 1 [prevents mistake A]
- Step 2 [prevents mistake B]
```

#### Section 12: Common Workflows

```markdown
## Common Workflows

**1. First Time Setup:**
```bash
# Step 1
./scripts/setup.sh

# Step 2
tool --version
```

**2. [Workflow name]:**
```bash
# [Description]
```
```

#### Section 13: Tips

```markdown
## Tips

**[Category 1]:**
- Tip 1
- Tip 2

**[Category 2]:**
- Tip 1
- Tip 2

**See also:**
- [references/patterns.md](references/patterns.md) - Detailed workflows
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues
```

### Validation Checkpoint

After SKILL.md creation:
- [ ] YAML frontmatter complete with good description
- [ ] All sections present
- [ ] Examples in every section
- [ ] All file references valid
- [ ] Guardrails marked as ⚠️ MANDATORY
- [ ] Helper scripts documented
- [ ] Workflows explained
- [ ] Tips practical and specific

---

## PHASE 6: INTEGRATION & TESTING

### Goal
Integrate skill into PAI and validate it works correctly.

### Integration Steps

#### Step 1: Add to KAI.md

Update `~/.claude/global/KAI.md` in the `<available_skills>` section:

```xml
<skill>
<name>tool-name</name>
<description>Your skill description from SKILL.md frontmatter</description>
<location>user</location>
</skill>
```

**Important:** Use the EXACT description from SKILL.md frontmatter for consistency.

#### Step 2: Verify File Structure

```bash
tree ~/.claude/skills/[tool-name]
```

Expected structure:
```
tool-name/
├── SKILL.md
├── references/
│   ├── cli-reference.md
│   ├── config-reference.md
│   ├── patterns.md
│   └── troubleshooting.md
├── scripts/
│   ├── setup.sh
│   ├── [other scripts]
│   └── README.md
└── templates/
    ├── basic_config.yml
    └── [other templates]
```

### Testing Workflow

#### Test 1: Skill Activation

**Test natural language triggers:**

1. Start new Claude session
2. Try trigger phrases from description:
   - "Use [tool name]"
   - "[Use case from description]"
   - "[Keyword from description]"
3. Verify skill loads correctly

**If skill doesn't activate:**
- Check description has clear triggers
- Verify added to KAI.md correctly
- Try more explicit phrases

#### Test 2: Helper Scripts

**For each helper script:**

1. Navigate to scripts directory
2. Run script with `--help` or `-h`
3. Try with valid inputs
4. Try with invalid inputs (verify error handling)
5. Check exit codes

**Example:**
```bash
cd ~/.claude/skills/tool-name/scripts

# Test help
./setup.sh --help

# Test successful run
./setup.sh

# Test validation script
python validate_config.py ../templates/basic_config.yml

# Test with invalid input
python validate_config.py nonexistent.yml
```

#### Test 3: Config Templates

**For each template:**

1. Use with actual tool
2. Verify it works
3. Check all options are valid
4. Confirm comments are accurate

**Example:**
```bash
cd ~/.claude/skills/tool-name/templates

# Test basic config
tool --config basic_config.yml test-input

# Test advanced config
tool --config advanced_config.yml test-input
```

#### Test 4: File References

**Check all links work:**

```bash
cd ~/.claude/skills/tool-name

# Check references exist
test -f references/cli-reference.md && echo "✓ CLI reference exists"
test -f references/config-reference.md && echo "✓ Config reference exists"

# Check scripts exist
test -f scripts/setup.sh && echo "✓ Setup script exists"

# Check templates exist
test -f templates/basic_config.yml && echo "✓ Basic template exists"
```

#### Test 5: Workflow Validation

**Run through documented workflows:**

1. Follow "First-Time Setup" workflow
2. Try each "Proven Pattern"
3. Execute "Common Workflows"
4. Verify expected outputs

**Document any issues:**
- Steps that don't work
- Missing prerequisites
- Unclear instructions
- Incorrect examples

### Iteration Process

Based on testing, iterate:

1. **Fix broken references**
   - Update file paths
   - Verify all links

2. **Improve unclear sections**
   - Add more context
   - Include examples
   - Clarify steps

3. **Add missing components**
   - Scripts that would help
   - Templates for common cases
   - Additional guardrails

4. **Enhance examples**
   - More realistic use cases
   - Complete working examples
   - Expected outputs

### Final Validation

Before declaring skill complete:

- [ ] Skill activates with natural language
- [ ] All helper scripts work
- [ ] All config templates valid
- [ ] All file references resolve
- [ ] All workflows execute successfully
- [ ] Examples are accurate
- [ ] Documentation is clear
- [ ] No broken links
- [ ] Guardrails are effective
- [ ] User can follow docs without confusion

---

## 🎨 TEMPLATES USAGE GUIDE

### Template Variable Syntax

Templates use `{{VARIABLE_NAME}}` syntax for placeholders.

**Conditional sections:**
```
{{#IF_CONDITION}}
Content shown if condition is true
{{/IF_CONDITION}}
```

**Lists:**
```
{{ITEM_LIST}}
```

### Filling Templates

**Manual approach:**
1. Copy template to destination
2. Search/replace all `{{VARIABLES}}`
3. Remove conditional sections not needed
4. Fill in list sections

**Programmatic approach:**
```python
def fill_template(template_path, variables):
    with open(template_path) as f:
        content = f.read()

    for key, value in variables.items():
        content = content.replace(f"{{{{{key}}}}}", value)

    return content
```

### Template Customization

**Add tool-specific sections:**

Templates are starting points. Add sections for:
- Tool-specific features
- Unique configuration options
- Special workflows
- Domain-specific patterns

**Example:** Add "Authentication" section for API tools.

---

## 💡 BEST PRACTICES

### Documentation Analysis

1. **Read completely** before starting analysis
2. **Take notes** on patterns you see
3. **Look for implicit workflows** not explicitly documented
4. **Anticipate mistakes** beyond what docs mention
5. **Consider edge cases** and error scenarios

### Component Design

1. **Start simple** - Add complexity as needed
2. **Validate early** - Test scripts as you write them
3. **DRY principle** - Reuse logic across scripts
4. **User-friendly** - Clear messages, good defaults
5. **Fail fast** - Catch errors early with clear messages

### Skill Writing

1. **Progressive disclosure** - Quick start → Details
2. **Examples everywhere** - Every section needs examples
3. **Consistent formatting** - Follow template structure
4. **Cross-reference** - Link related sections
5. **Test as you write** - Verify examples work

### Testing

1. **Fresh start** - Test in new session
2. **Follow docs literally** - Don't assume knowledge
3. **Try to break it** - Invalid inputs, edge cases
4. **Real scenarios** - Use actual use cases
5. **Document issues** - Note everything that's unclear

---

## 🚨 COMMON PITFALLS

### Pitfall 1: Incomplete Documentation Analysis

**Symptom:** Missing critical workflows or pitfalls

**Cause:** Skimming docs instead of thorough analysis

**Solution:**
- Read all sections completely
- Take notes on every pattern
- Ask: "What could go wrong here?"
- Document implicit workflows

### Pitfall 2: Over-Engineering Helper Scripts

**Symptom:** Complex scripts that are hard to maintain

**Cause:** Trying to handle every edge case

**Solution:**
- Start with simple version
- Add features based on actual need
- Keep logic clear and readable
- Document complex parts well

### Pitfall 3: Template Overload

**Symptom:** Too many templates, user confused

**Cause:** Creating template for every variation

**Solution:**
- Stick to 2-4 key templates
- Use comments to show variations
- Document when to use each
- Make basic template really basic

### Pitfall 4: Weak Guardrails

**Symptom:** Users still making common mistakes

**Cause:** Guardrails not enforced strongly enough

**Solution:**
- Use ⚠️ MANDATORY prominently
- Explain "why this prevents failures"
- Build validation into scripts
- Make it hard to skip critical steps

### Pitfall 5: Stale Examples

**Symptom:** Examples don't work as shown

**Cause:** Not testing examples after writing

**Solution:**
- Run every example as you write it
- Use actual tool to verify
- Include expected output
- Update when tool changes

### Pitfall 6: Missing Context

**Symptom:** Users confused about when to use features

**Cause:** Assuming knowledge not stated

**Solution:**
- Explain prerequisites clearly
- State when to use each approach
- Provide context for options
- Link to background info

---

## 📊 QUALITY CHECKLIST

### Documentation Analysis Quality

- [ ] Complete tool overview extracted
- [ ] All command/API patterns documented
- [ ] Minimum 3 workflows identified
- [ ] All explicit warnings captured
- [ ] Anticipated pitfalls documented
- [ ] Best practices extracted
- [ ] Configuration patterns noted

### Skill Design Quality

- [ ] At least 3 helper scripts designed
- [ ] At least 2 config templates designed
- [ ] Critical guardrails identified
- [ ] Mandatory workflows defined
- [ ] Checklists created
- [ ] Reference structure planned

### Artifact Quality

- [ ] All helper scripts work correctly
- [ ] Scripts have clear error messages
- [ ] Config templates are valid
- [ ] Templates are well-commented
- [ ] Reference docs are complete
- [ ] scripts/README.md is clear

### SKILL.md Quality

- [ ] YAML frontmatter complete
- [ ] Description has clear triggers
- [ ] All template sections included
- [ ] Examples in every section
- [ ] All file references valid
- [ ] Guardrails marked MANDATORY
- [ ] Workflows explained clearly

### Integration Quality

- [ ] Added to KAI.md correctly
- [ ] Skill activates with natural language
- [ ] All file references work
- [ ] Helper scripts executable
- [ ] Config templates usable
- [ ] Workflows tested

---

## 🎯 SUCCESS CRITERIA

A skill is complete and production-ready when:

1. **Comprehensive**
   - Covers all major tool features
   - Includes common workflows
   - Documents pitfalls and solutions

2. **Automated**
   - Helper scripts for error-prone tasks
   - Validation prevents mistakes
   - Setup is largely automated

3. **Safe**
   - Guardrails prevent common mistakes
   - Mandatory workflows enforced
   - Prerequisites checked

4. **Clear**
   - Examples work as shown
   - Instructions are unambiguous
   - Structure is consistent

5. **Tested**
   - All scripts run successfully
   - All templates are valid
   - All workflows execute correctly

6. **Maintainable**
   - Well-organized structure
   - Clear documentation
   - Easy to update

---

## 📚 REAL-WORLD EXAMPLES

### Example 1: crawl4ai-cli Skill

**Tool:** crawl4ai CLI for web scraping

**Analysis highlights:**
- Common pitfall: Scraping navigation instead of content
- Critical workflow: Inspect → Extract → Validate
- Key feature: Dynamic content handling

**Helper scripts created:**
- `setup.sh` - Verify installation, setup Playwright
- `generate_schema.py` - Interactive schema builder
- `validate_extraction.py` - Validate scraped data
- `inspect_page.sh` - Inspect page before scraping

**Templates created:**
- `crawler_basic.yml` - Simple crawling
- `crawler_dynamic.yml` - JavaScript-heavy sites
- `extract_css.yml` - CSS extraction config
- `schema_simple.json` - Basic schema example

**Guardrails implemented:**
- ⚠️ MANDATORY: Inspect → Extract → Validate workflow
- Validation script catches schema errors early
- Setup script ensures prerequisites

**Result:** Users can scrape complex sites without common mistakes.

### Example 2: Git Workflow Skill (Hypothetical)

**Tool:** Git version control

**Analysis highlights:**
- Common pitfall: Committing to wrong branch
- Common pitfall: Pushing sensitive data
- Best practice: Atomic commits
- Critical workflow: Branch → Commit → Review → Merge

**Helper scripts to create:**
- `setup.sh` - Configure Git, verify installation
- `validate_commit.py` - Check commit message format, file content
- `branch_status.sh` - Show current branch, changes, upstream

**Templates to create:**
- `.gitignore_python` - Python project ignore file
- `.gitignore_node` - Node.js project ignore file
- `commit_message_template` - Conventional commit template

**Guardrails to implement:**
- ⚠️ MANDATORY: Check branch before commit
- Validation script scans for secrets
- Hook to run validation before commit

**SKILL.md sections:**
- Prerequisites: Git installed, configured
- Quick start: Clone, branch, commit, push
- Core tasks: Branching, committing, merging
- Proven patterns: Feature branch workflow, hotfix workflow
- Troubleshooting: Merge conflicts, detached HEAD

---

## 🔗 INTEGRATION WITH PAI ECOSYSTEM

### Relationship to Other Skills

**create-skill:**
- General skill creation framework
- skill-creator-from-docs extends it for documentation-based skills

**crawl4ai-cli:**
- Used in Phase 1 to extract documentation from URLs
- Example of well-structured documentation-based skill

**development:**
- May use generated skills during development
- Primary stack skills complement tool-specific skills

### Slash Command Integration

Consider creating slash commands for common skill operations:

```bash
# Example: /create-skill-from-url
#!/bin/bash
# Create skill from documentation URL
URL=$1
TOOL_NAME=$2

# Extract docs
crwl "$URL" -o markdown > "/tmp/${TOOL_NAME}_docs.md"

# Invoke skill creator
# (Claude processes with skill-creator-from-docs skill)
```

### Agent Integration in Generated Skills

**Note:** This section is about including agent references in the skills you CREATE, not about using agents to create skills (this Python system is sequential).

For complex tools, the generated skill can reference specialized agents:

```markdown
## Agent Configuration

For this skill, use:
- **Agent Type**: Tool Specialist
- **Training**: Focused on [tool] expertise
- **Use for**: Complex [tool] workflows requiring deep knowledge
```

**Example:** If creating a skill for a complex tool like Kubernetes, the generated skill can specify which PAI agents to use for Kubernetes-specific workflows.

---

## 🎓 LEARNING PATH

### For Claude (AI)

1. **Study existing skills**
   - Read crawl4ai-cli skill thoroughly
   - Analyze structure and patterns
   - Understand helper script value

2. **Practice documentation analysis**
   - Start with simple tools
   - Extract patterns systematically
   - Identify pitfalls proactively

3. **Build incrementally**
   - Start with basic skill structure
   - Add scripts one at a time
   - Test continuously

4. **Iterate based on usage**
   - Observe what users struggle with
   - Add helpers for pain points
   - Refine documentation

### For Users (Humans)

1. **Provide good documentation**
   - Official docs preferred
   - Include context about tool usage
   - Share known pitfalls

2. **Test thoroughly**
   - Try generated helpers
   - Validate examples
   - Report what's unclear

3. **Give feedback**
   - What scripts would help
   - What's missing from docs
   - What caused confusion

4. **Iterate together**
   - Refine based on real usage
   - Add missing components
   - Improve over time

---

## 📝 CONCLUSION

This methodology transforms documentation into production-ready skills that:

1. **Save time** - Helper scripts automate repetitive tasks
2. **Prevent mistakes** - Guardrails and validation catch errors
3. **Teach effectively** - Examples and patterns show best practices
4. **Scale knowledge** - Captures expertise in reusable form

**Key success factors:**
- Thorough documentation analysis
- Thoughtful component design
- Template-driven consistency
- Comprehensive testing
- Continuous iteration

**Remember:** The goal is to make tools easy and safe to use, not just to document them.

---

## 🔧 APPENDIX

### Template Reference

All templates in: `~/.claude/skills/skill-creator-from-docs/templates/`

- `tool-skill-SKILL.md.template` - Main skill structure
- `helper-script.py.template` - Python helper script
- `helper-script.sh.template` - Bash helper script
- `config-template.yml.template` - Configuration file
- `README-scripts.md.template` - Scripts directory README

### Example Analysis Documents

See `examples/` directory for complete analysis documents from real tools.

### Script Best Practices

**Error handling:**
```python
try:
    # Operation
except SpecificError as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    print("💡 Tip: [helpful suggestion]", file=sys.stderr)
    sys.exit(1)
```

**Validation:**
```python
def validate_input(value):
    if not value:
        raise ValueError("Input cannot be empty")
    if not meets_criteria(value):
        raise ValueError(f"Input must meet: {criteria}")
    return value
```

**User-friendly output:**
```bash
info() { echo -e "${BLUE}ℹ️  $*${NC}"; }
success() { echo -e "${GREEN}✅ $*${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $*${NC}"; }
error() { echo -e "${RED}❌ $*${NC}" >&2; }
```

### Config Template Patterns

**Basic pattern:**
```yaml
# Section name
# What this section controls

option_name: default_value  # What this option does
```

**With alternatives:**
```yaml
# Option with multiple valid values
mode: basic  # Options: basic, advanced, expert
```

**With examples:**
```yaml
# Example: For production use, set to "strict"
validation: lenient
```

---

**End of Methodology Document**
