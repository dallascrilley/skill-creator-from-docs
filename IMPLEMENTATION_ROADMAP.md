# skill-creator-from-docs — Implementation Roadmap

**Version:** 1.0
**Created:** 2025-01-08
**Status:** Planning Phase

---

## Executive Summary

This roadmap synthesizes SPECIFICATION.md and REUSABLE_COMPONENTS.md into a concrete, phased implementation plan for building the skill-creator-from-docs skill.

**Goal:** Automate creation of documentation-based Claude Code skills through a 9-phase workflow that extracts, synthesizes, and validates practical helpers from documentation.

**Timeline Estimate:** 4-6 weeks (based on complexity tiers below)

**Key Success Metrics:**
- Generate complete skill from docs in < 30 minutes
- Template synthesis accuracy ≥ 90%
- Guardrail coverage for 100% of documented pitfalls
- Validation pass rate ≥ 95%

---

## Implementation Phases

### Phase 0: Foundation Setup
**Duration:** 2-3 days
**Priority:** P0 (Blocker for all other work)

#### Objectives
Set up project structure and copy reusable components from skill-creator.

#### Tasks

**0.1: Directory Structure Setup** ⏱️ 1 hour
```bash
mkdir -p /Users/dallascrilley/PAI/.claude/skills/skill-creator-from-docs/{scripts,templates,references,examples,tests}
```

**Deliverables:**
- [ ] Base directory structure created
- [ ] .gitignore configured
- [ ] README.md stub created

---

**0.2: Copy Reusable Scripts** ⏱️ 2 hours

**From skill-creator → skill-creator-from-docs:**
```bash
# Copy validation and packaging scripts (use as-is)
cp skill-creator/scripts/validate_skill.py skill-creator-from-docs/scripts/
cp skill-creator/scripts/package_skill.py skill-creator-from-docs/scripts/
cp skill-creator/scripts/analyze_conciseness.py skill-creator-from-docs/scripts/
cp skill-creator/scripts/quick_validate.py skill-creator-from-docs/scripts/
```

**Deliverables:**
- [ ] 4 scripts copied and verified
- [ ] Test each script with --help flag
- [ ] Document any dependency requirements

**Dependencies:** None
**Success Criteria:** All scripts run with --help successfully

---

**0.3: Copy Reusable References** ⏱️ 1 hour

**Direct copies (no modification needed):**
```bash
cp skill-creator/references/core_principles.md skill-creator-from-docs/references/
cp skill-creator/references/token_efficiency.md skill-creator-from-docs/references/
cp skill-creator/references/multi_model_testing.md skill-creator-from-docs/references/
cp skill-creator/references/progressive_disclosure.md skill-creator-from-docs/references/
```

**Deliverables:**
- [ ] 4 reference docs copied
- [ ] Links verified (update if pointing to old skill-creator paths)

**Success Criteria:** All internal links resolve correctly

---

**0.4: Create Base Research Log Template** ⏱️ 1 hour

Create `templates/RESEARCH_LOG_TEMPLATE.md`:
```markdown
# Research Log: [TOOL-NAME]

**Created:** [DATE]
**Documentation Source:** [URL or Path]
**Tool Type:** [CLI/API/Library/Framework]
**Version:** [Extracted or Unknown]

## Phase 1: Documentation Acquisition
### Source Information
- Primary docs: [URL]
- Crawled pages: [count]
- Key pages identified: [list]

### Crawl Metadata
- Date: [timestamp]
- Tool used: crawl4ai-cli
- Success rate: [X/Y pages]

## Phase 2: Documentation Analysis
### Tool Type Classification
[CLI/API/Library/Framework] - [Reasoning]

### Workflow Patterns Identified
1. [Pattern name]: [Description]
2. ...

### Example Code Catalog
#### Example 1: [Title]
- Source: [URL#section]
- Type: [Basic usage/Advanced/Edge case]
- Code:
  ```[language]
  [verbatim code]
  ```

### Gap Analysis
- [ ] Gap: [Description] - Status: [To research/Documented/Resolved]

### Pitfall Warnings
- [Warning from docs] → [Guardrail strategy]

## Phase 3: Research & Clarification
### Research Queries (Perplexity MCP)
#### Query 1: [Search query]
- **Rationale:** [Why this research was needed]
- **Findings:** [Summary]
- **Source:** [URL]
- **Incorporation:** [Generally useful / Task-specific / Not used]

### Unresolved Gaps
- [Gap requiring human review]

## Phase 4: Template Synthesis
### Templates Created
- [template-name.ext]: [Purpose] - Synthesized from [examples X, Y, Z]

### Pattern Generalizations
- [Pattern]: Abstracted from [count] examples

## Phase 5-7: Asset Creation
[Document guardrails, support assets, tests created]

## Summary
- Total examples extracted: [count]
- Templates created: [count]
- Guardrails generated: [count]
- Research queries: [count]
- Unresolved items: [count]
```

**Deliverables:**
- [ ] RESEARCH_LOG_TEMPLATE.md created
- [ ] Validated with sample data

---

### Phase 1: Documentation Extraction System
**Duration:** 1 week
**Priority:** P0 (Core functionality)

#### Objectives
Build the automated documentation acquisition and analysis system.

#### Tasks

**1.1: Create doc_extractor.py** ⏱️ 1 day

**Purpose:** Orchestrate crawl4ai-cli or process markdown files

**Key Functions:**
```python
def extract_from_url(url: str, key_pages: list[str] = None) -> DocumentationCorpus:
    """Extract documentation from URL using crawl4ai-cli."""

def extract_from_markdown(file_path: str) -> DocumentationCorpus:
    """Process local markdown documentation."""

def save_raw_docs(corpus: DocumentationCorpus, output_dir: str):
    """Save raw documentation to research log."""

class DocumentationCorpus:
    source: str
    pages: list[Page]
    metadata: dict
```

**Integration Points:**
- Use `crawl4ai-cli` skill for URL extraction
- Ask user for key pages via AskUserQuestion tool
- Store in RESEARCH_LOG.md

**Deliverables:**
- [ ] doc_extractor.py implemented
- [ ] Unit tests for markdown processing
- [ ] Integration test with sample docs
- [ ] Error handling for crawl failures

**Dependencies:** crawl4ai-cli skill installed
**Success Criteria:** Extract crawl4ai docs successfully

---

**1.2: Create doc_analyzer.py** ⏱️ 2 days

**Purpose:** Analyze extracted documentation and identify patterns

**Key Functions:**
```python
def classify_tool_type(corpus: DocumentationCorpus) -> ToolType:
    """Determine if CLI, API, library, or framework."""

def extract_workflows(corpus: DocumentationCorpus) -> list[Workflow]:
    """Identify common usage patterns."""

def extract_examples(corpus: DocumentationCorpus) -> list[CodeExample]:
    """Collect all code examples verbatim."""

def identify_patterns(examples: list[CodeExample]) -> list[Pattern]:
    """Find patterns across multiple examples."""

def extract_pitfalls(corpus: DocumentationCorpus) -> list[Pitfall]:
    """Find warnings, common errors, gotchas."""

def analyze_gaps(corpus: DocumentationCorpus) -> GapAnalysis:
    """Identify ambiguities and missing information."""
```

**Analysis Heuristics:**
```python
# Tool type classification
CLI_INDICATORS = ["command", "flag", "--", "usage:", "options:"]
API_INDICATORS = ["endpoint", "request", "response", "POST", "GET"]
LIBRARY_INDICATORS = ["import", "class", "function", "module"]
FRAMEWORK_INDICATORS = ["scaffold", "generate", "project structure"]

# Pitfall detection
PITFALL_KEYWORDS = ["warning:", "note:", "important:", "⚠️", "gotcha", "common mistake"]

# Gap detection
GAP_INDICATORS = ["see documentation", "refer to", "advanced usage", "for more details"]
```

**Deliverables:**
- [ ] doc_analyzer.py implemented
- [ ] Heuristics validated on 3+ doc types
- [ ] Analysis output format documented
- [ ] Unit tests for each analyzer function

**Dependencies:** doc_extractor.py
**Success Criteria:** Correctly classify tool types ≥ 90% accuracy on test set

---

**1.3: Create gap_researcher.py** ⏱️ 2 days

**Purpose:** Use Perplexity MCP to research documentation gaps

**Key Functions:**
```python
def detect_research_triggers(gap_analysis: GapAnalysis) -> list[ResearchTrigger]:
    """Determine what needs research."""

def generate_research_queries(trigger: ResearchTrigger) -> list[str]:
    """Create Perplexity search queries."""

async def research_gap(query: str) -> ResearchFinding:
    """Execute Perplexity MCP search."""

def categorize_findings(findings: list[ResearchFinding]) -> dict:
    """Sort into 'generally useful' vs 'task-specific'."""

def update_research_log(findings: list[ResearchFinding], log_path: str):
    """Document research with rationale."""
```

**Research Trigger Logic:**
```python
TRIGGER_CONDITIONS = [
    "ambiguity_detected",        # Unclear documentation
    "roadblock_hit",             # LLM can't proceed
    "advanced_mentioned",        # Feature referenced but not explained
    "use_case_implied",          # Common pattern not documented
]
```

**Deliverables:**
- [ ] gap_researcher.py implemented
- [ ] Perplexity MCP integration tested
- [ ] Fallback to human review implemented
- [ ] Research log format validated

**Dependencies:** doc_analyzer.py, Perplexity MCP
**Success Criteria:** Successfully research and document 5 test gaps

---

### Phase 2: Template Synthesis Engine
**Duration:** 1 week
**Priority:** P0 (Core functionality)

#### Objectives
Build system to convert documentation examples into usable templates.

#### Tasks

**2.1: Create template_synthesizer.py** ⏱️ 3 days

**Purpose:** Transform examples into generalized, commented templates

**Key Functions:**
```python
def synthesize_template(
    examples: list[CodeExample],
    pattern: Pattern,
    tool_type: ToolType
) -> Template:
    """Create template from examples."""

def add_inline_comments(template: Template, context: AnalysisContext) -> Template:
    """Add parameter explanations."""

def create_variable_placeholders(template: Template) -> Template:
    """Replace specific values with ${PLACEHOLDER}."""

def add_default_values(template: Template, examples: list[CodeExample]) -> Template:
    """Insert sensible defaults from examples."""

def validate_template_syntax(template: Template) -> ValidationResult:
    """Test basic validity (non-blocking)."""

def generate_usage_examples(template: Template, examples: list[CodeExample]) -> str:
    """Create example usage documentation."""
```

**Template Synthesis Strategy:**
```python
# Step 1: Extract verbatim
extract_examples_verbatim(corpus)

# Step 2: Identify commonalities
common_structure = find_common_structure(examples)
variable_parts = find_variable_parts(examples)

# Step 3: Generalize
template = create_skeleton(common_structure)
template = add_placeholders(template, variable_parts)

# Step 4: Annotate
template = add_comments(template, parameter_docs)
template = add_defaults(template, example_values)

# Step 5: Validate
validation = test_syntax(template)
if validation.has_errors:
    log_validation_issues(validation)
```

**Deliverables:**
- [ ] template_synthesizer.py implemented
- [ ] Synthesis tested on CLI, API, library examples
- [ ] Template validation integrated
- [ ] Usage example generation working

**Dependencies:** doc_analyzer.py
**Success Criteria:** Generate valid templates from 3+ documentation sources

---

**2.2: Create Template Testing Framework** ⏱️ 2 days

**Purpose:** Generate test scripts for templates

**Key Functions:**
```python
def generate_template_tests(
    templates: list[Template],
    tool_type: ToolType
) -> TestSuite:
    """Create automated test scripts."""

def create_syntax_validator(template: Template) -> str:
    """Generate syntax check script."""

def create_execution_test(template: Template, safe_mode: bool = True) -> str:
    """Generate basic execution test."""

def create_validation_checklist(templates: list[Template]) -> str:
    """Generate manual verification checklist."""
```

**Test Generation Strategy:**
```bash
# For bash templates
#!/bin/bash
# test_[template-name].sh
set -euo pipefail

# Syntax validation
bash -n template.sh || { echo "Syntax error"; exit 1; }

# Placeholder check
grep -q '\${.*}' template.sh || { echo "No placeholders found"; exit 1; }

# Comment check
grep -q '^# ⚠️' template.sh || echo "Warning: No inline warnings"

echo "✅ Template validation passed"
```

**Deliverables:**
- [ ] Test generation implemented
- [ ] Test scripts for bash, python, config files
- [ ] Validation checklist generator
- [ ] Sample test suite validated

**Success Criteria:** Generate working tests for 5+ template types

---

### Phase 3: Guardrail System
**Duration:** 4-5 days
**Priority:** P0 (Core functionality)

#### Objectives
Build multi-layered guardrail generation system.

#### Tasks

**3.1: Create guardrail_generator.py** ⏱️ 3 days

**Purpose:** Generate all 4 layers of guardrails

**Key Functions:**
```python
# Layer 1: Inline Warnings
def generate_inline_warnings(pitfalls: list[Pitfall]) -> dict[str, str]:
    """Create inline comments for templates."""

# Layer 2: Pre-flight Scripts
def generate_validation_script(
    tool_type: ToolType,
    requirements: list[Requirement]
) -> str:
    """Create validate_prereqs.sh/py."""

# Layer 3: Checklists
def generate_checklist(
    workflows: list[Workflow],
    pitfalls: list[Pitfall]
) -> str:
    """Create pre-flight.md checklist."""

# Layer 4: Automated Boilerplates
def generate_setup_script(
    tool_type: ToolType,
    config: Configuration
) -> str:
    """Create setup.sh with error handling."""
```

**Guardrail Templates:**
```python
VALIDATION_SCRIPT_TEMPLATE = """
#!/bin/bash
# validate_prereqs.sh - Generated by skill-creator-from-docs

set -euo pipefail

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo "🔍 Validating prerequisites for {tool_name}..."

# Check 1: [Generated from requirements]
check_api_key() {
    if [ -z "${{API_KEY:-}}" ]; then
        echo -e "${{RED}}❌ API_KEY not set${{NC}}"
        echo "   Set with: export API_KEY='your-key'"
        return 1
    fi
    echo -e "${{GREEN}}✅ API_KEY configured${{NC}}"
    return 0
}

# Check 2: [Generated]
# ...

# Run all checks
checks_passed=0
checks_failed=0

check_api_key && ((checks_passed++)) || ((checks_failed++))
# ... run all checks

echo ""
if [ $checks_failed -eq 0 ]; then
    echo -e "${{GREEN}}✅ All $checks_passed checks passed${{NC}}"
    exit 0
else
    echo -e "${{RED}}❌ $checks_failed checks failed${{NC}}"
    exit 1
fi
"""

CHECKLIST_TEMPLATE = """
# Pre-Flight Checklist: {tool_name}

Run before executing {tool_name} commands.

## Prerequisites
{generated_prereqs}

## Configuration
{generated_config_items}

## Common Pitfalls
{generated_pitfall_checks}

## Validation
Run automated checks:
```bash
./scripts/validate_prereqs.sh
```
"""
```

**Deliverables:**
- [ ] guardrail_generator.py implemented
- [ ] All 4 layers generating correctly
- [ ] Generated scripts tested
- [ ] Checklist format validated

**Dependencies:** doc_analyzer.py, template_synthesizer.py
**Success Criteria:** Generate complete guardrail system for 3+ tool types

---

**3.2: Integrate Guardrails with Templates** ⏱️ 1 day

**Purpose:** Combine templates with their guardrails

**Tasks:**
- [ ] Inject inline warnings into templates
- [ ] Link templates to validation scripts
- [ ] Reference checklists in SKILL.md
- [ ] Test integrated workflow

**Success Criteria:** User can run template → validation → execution seamlessly

---

### Phase 4: Support Assets Generator
**Duration:** 3-4 days
**Priority:** P1 (High value, not blocking)

#### Objectives
Generate setup scripts, configs, troubleshooting docs, and quick references.

#### Tasks

**4.1: Create asset_generator.py** ⏱️ 2 days

**Key Functions:**
```python
def generate_setup_script(tool_type: ToolType, requirements: list) -> str:
    """Create installation/setup automation."""

def generate_config_template(tool_type: ToolType, examples: list) -> str:
    """Create configuration file templates."""

def generate_troubleshooting_tree(pitfalls: list[Pitfall]) -> str:
    """Create decision tree markdown."""

def generate_quick_reference(workflows: list[Workflow], commands: list) -> str:
    """Create cheatsheet."""
```

**Asset Templates:**
```python
SETUP_SCRIPT_TEMPLATE = """
#!/bin/bash
# setup.sh - Automated setup for {tool_name}

set -euo pipefail

echo "🚀 Setting up {tool_name}..."

# Step 1: Install dependencies
install_dependencies() {
    {generated_install_commands}
}

# Step 2: Configure environment
configure_environment() {
    {generated_config_steps}
}

# Step 3: Verify installation
verify_setup() {
    {generated_verification}
}

# Execute setup
install_dependencies
configure_environment
verify_setup

echo "✅ Setup complete! Run './scripts/validate_prereqs.sh' to verify."
"""

TROUBLESHOOTING_TREE_TEMPLATE = """
# Troubleshooting Decision Tree

## Error: {error_pattern}

**Symptoms:**
- {symptom_1}
- {symptom_2}

**Diagnosis:**
1. Check {check_1}
   - If yes → {solution_1}
   - If no → Continue to step 2

2. Check {check_2}
   - If yes → {solution_2}
   - If no → {escalation}

**Prevention:**
{generated_prevention_steps}
"""
```

**Deliverables:**
- [ ] asset_generator.py implemented
- [ ] All 4 asset types generating
- [ ] Assets tested with sample tools
- [ ] Documentation updated

**Success Criteria:** Generate complete asset set for CLI, API, library examples

---

### Phase 5: SKILL.md Generator
**Duration:** 3-4 days
**Priority:** P0 (Core deliverable)

#### Objectives
Create SKILL.md generation system with auto-population from analysis.

#### Tasks

**5.1: Create skill_md_generator.py** ⏱️ 2 days

**Key Functions:**
```python
def generate_frontmatter(
    tool_name: str,
    analysis: AnalysisContext,
    workflows: list[Workflow],
    pitfalls: list[Pitfall]
) -> str:
    """Auto-generate YAML frontmatter."""

def generate_overview(corpus: DocumentationCorpus) -> str:
    """Extract overview from docs."""

def generate_quick_start(templates: list[Template]) -> str:
    """Create quick start from simplest template."""

def generate_workflow_section(workflows: list[Workflow], templates: list[Template]) -> str:
    """Document common workflows."""

def generate_template_references(templates: list[Template]) -> str:
    """Create template documentation."""

def generate_troubleshooting_section(
    pitfalls: list[Pitfall],
    troubleshooting_tree: str
) -> str:
    """Link to troubleshooting resources."""

def compile_skill_md(sections: dict) -> str:
    """Combine all sections into final SKILL.md."""
```

**SKILL.md Generation Strategy:**
```python
# Auto-populate from analysis
frontmatter = generate_frontmatter(
    name=tool_name,
    description=extract_description(corpus),
    use_when=extract_use_cases(workflows),
    prevents=count_pitfalls(pitfalls),
    keywords=extract_keywords(corpus, workflows)
)

# Generate sections
overview = extract_from_docs(corpus, section="overview")
quick_start = create_from_template(templates[0])  # Simplest
workflows_section = document_workflows(workflows, templates)
templates_section = reference_templates(templates)
guardrails_section = reference_guardrails(scripts)
troubleshooting = link_to_tree(troubleshooting_tree)
research_notes = link_to_research_log()

# Compile
skill_md = compile_sections({
    "frontmatter": frontmatter,
    "overview": overview,
    "quick_start": quick_start,
    "workflows": workflows_section,
    "templates": templates_section,
    "guardrails": guardrails_section,
    "troubleshooting": troubleshooting,
    "research": research_notes
})
```

**Deliverables:**
- [ ] skill_md_generator.py implemented
- [ ] All sections auto-generating
- [ ] Progressive disclosure applied (< 500 lines)
- [ ] Generated SKILL.md validates

**Success Criteria:** Generate valid SKILL.md for 3+ documentation sources

---

**5.2: Create doc-based-skill-skeleton Template** ⏱️ 1 day

**Purpose:** Base template for generated skills

**Structure:**
```
templates/doc-based-skill-skeleton/
├── SKILL.md (with [AUTO-GENERATED] markers)
├── RESEARCH_LOG.md (from RESEARCH_LOG_TEMPLATE.md)
├── templates/
│   └── README.md
├── scripts/
│   └── README.md
├── checklists/
│   └── README.md
├── tests/
│   └── README.md
└── docs/
    └── README.md
```

**SKILL.md Template:**
```markdown
---
name: [AUTO: tool-name]
description: |
  [AUTO: from doc analysis]

  Use when: [AUTO: from workflows]

  Prevents [AUTO: count] documented issues: [AUTO: pitfall summary]

  Keywords: [AUTO: from docs + workflows]
---

# [AUTO: Tool Name] — [AUTO: Brief Description]

## Documentation Source
<!-- AUTO-GENERATED -->
- Original docs: [AUTO: URL]
- Crawled: [AUTO: date]
- Version: [AUTO: version or "See docs"]

## Overview
[AUTO: from docs intro/overview]

## Quick Start
[AUTO: simplest template]

## Common Workflows
[AUTO: workflow sections]

## Templates
[AUTO: template references]

## Guardrails & Validation
[AUTO: validation script references]

## Troubleshooting
[AUTO: decision tree link]

## Research Notes
See [RESEARCH_LOG.md](RESEARCH_LOG.md)
```

**Deliverables:**
- [ ] Template structure created
- [ ] All READMEs populated
- [ ] AUTO markers documented
- [ ] Test generation from template

**Success Criteria:** Template generates valid skill structure

---

### Phase 6: Orchestration & CLI
**Duration:** 3-4 days
**Priority:** P0 (User-facing interface)

#### Objectives
Create main orchestration script and user interface.

#### Tasks

**6.1: Extend init_skill.py** ⏱️ 2 days

**Purpose:** Add --from-docs flag and orchestration

**New Flags:**
```bash
python scripts/init_skill.py <skill-name> \
  --from-docs <url-or-markdown> \
  --doc-type <cli|api|library|auto> \
  --key-pages <page1,page2,...> \
  --auto-extract \
  --create-research-log \
  --template doc-based-skill-skeleton
```

**Orchestration Flow:**
```python
def create_skill_from_docs(
    skill_name: str,
    doc_source: str,
    doc_type: str = "auto",
    key_pages: list[str] = None,
    auto_extract: bool = True
):
    """Main orchestration function."""

    # Phase 1: Extract
    print("📥 Phase 1: Extracting documentation...")
    corpus = doc_extractor.extract(doc_source, key_pages)

    # Phase 2: Analyze
    print("🔍 Phase 2: Analyzing documentation...")
    analysis = doc_analyzer.analyze(corpus)

    # Phase 3: Research (if needed)
    if analysis.has_gaps:
        print("🔬 Phase 3: Researching gaps...")
        findings = gap_researcher.research(analysis.gaps)

    # Phase 4: Synthesize Templates
    print("🛠️  Phase 4: Synthesizing templates...")
    templates = template_synthesizer.synthesize(analysis.examples, analysis.patterns)

    # Phase 5: Generate Guardrails
    print("🛡️  Phase 5: Generating guardrails...")
    guardrails = guardrail_generator.generate(analysis.pitfalls, templates)

    # Phase 6: Create Support Assets
    print("📚 Phase 6: Creating support assets...")
    assets = asset_generator.generate(analysis, templates)

    # Phase 7: Generate Tests
    print("✅ Phase 7: Generating tests...")
    tests = test_generator.generate(templates, analysis)

    # Phase 8: Generate SKILL.md
    print("📝 Phase 8: Generating SKILL.md...")
    skill_md = skill_md_generator.generate(skill_name, analysis, templates, guardrails, assets)

    # Phase 9: Validate
    print("🔬 Phase 9: Validating skill...")
    validation = validate_skill(skill_dir)

    if validation.passed:
        print(f"✅ Skill '{skill_name}' created successfully!")
        print(f"   Location: {skill_dir}")
        print(f"   Templates: {len(templates)}")
        print(f"   Guardrails: {len(guardrails)}")
        print(f"   Next: Review RESEARCH_LOG.md and test templates")
    else:
        print(f"⚠️  Validation warnings: {validation.warnings}")
        print("   Skill created but review recommended")
```

**Deliverables:**
- [ ] init_skill.py extended with --from-docs
- [ ] Full orchestration implemented
- [ ] Progress reporting added
- [ ] Error handling for each phase

**Success Criteria:** Generate complete skill from URL in one command

---

**6.2: Create create_skill_from_docs.py (Standalone)** ⏱️ 1 day

**Purpose:** Dedicated script for doc-based skill creation

**Why separate from init_skill.py:**
- Different UX flow (interactive prompts)
- Specialized for documentation workflow
- Easier to maintain and test

**Interactive Flow:**
```python
def interactive_creation():
    """Interactive skill creation from docs."""

    # Step 1: Get documentation source
    doc_source = prompt("Documentation URL or markdown path: ")

    # Step 2: Specify key pages (optional)
    if is_url(doc_source):
        key_pages = prompt("Key pages (comma-separated, or skip): ", optional=True)

    # Step 3: Tool type (auto-detect or specify)
    tool_type = prompt("Tool type (cli/api/library/auto): ", default="auto")

    # Step 4: Skill name
    skill_name = prompt("Skill name: ", suggestion=infer_name(doc_source))

    # Step 5: Execute
    print("\n🚀 Creating skill from documentation...\n")
    create_skill_from_docs(skill_name, doc_source, tool_type, key_pages)
```

**Deliverables:**
- [ ] Standalone script created
- [ ] Interactive prompts implemented
- [ ] Same orchestration as init_skill.py --from-docs
- [ ] Help text and examples

**Success Criteria:** User can create skill interactively

---

### Phase 7: Testing & Validation
**Duration:** 1 week
**Priority:** P0 (Quality assurance)

#### Objectives
Comprehensive testing of the complete system.

#### Tasks

**7.1: Unit Tests** ⏱️ 2 days

**Coverage:**
- [ ] doc_extractor.py (markdown and URL processing)
- [ ] doc_analyzer.py (each analyzer function)
- [ ] gap_researcher.py (trigger detection, query generation)
- [ ] template_synthesizer.py (synthesis logic)
- [ ] guardrail_generator.py (all 4 layers)
- [ ] asset_generator.py (each asset type)
- [ ] skill_md_generator.py (section generation)

**Test Framework:**
```python
# tests/test_doc_analyzer.py
import pytest
from scripts.doc_analyzer import classify_tool_type, extract_workflows

def test_classify_cli_tool():
    corpus = load_fixture("cli_tool_docs.md")
    tool_type = classify_tool_type(corpus)
    assert tool_type == ToolType.CLI

def test_extract_workflows_from_examples():
    corpus = load_fixture("workflow_examples.md")
    workflows = extract_workflows(corpus)
    assert len(workflows) >= 3
    assert all(w.has_examples for w in workflows)
```

**Deliverables:**
- [ ] ≥ 80% code coverage
- [ ] All critical paths tested
- [ ] Test fixtures created
- [ ] CI integration (optional)

---

**7.2: Integration Tests** ⏱️ 2 days

**Test Scenarios:**

**Scenario 1: CLI Tool (crawl4ai-cli)**
```bash
# End-to-end test
python scripts/create_skill_from_docs.py \
  --skill-name test-crawl4ai \
  --from-docs https://crawl4ai.com/docs \
  --doc-type cli \
  --auto-extract

# Validate output
python scripts/validate_skill.py --full-check ~/.claude/skills/test-crawl4ai

# Test generated templates
cd ~/.claude/skills/test-crawl4ai/templates
./basic-usage.sh --help  # Should not error
```

**Scenario 2: API Documentation (Anthropic API)**
```bash
python scripts/create_skill_from_docs.py \
  --skill-name test-anthropic-api \
  --from-docs https://docs.anthropic.com/api \
  --doc-type api \
  --auto-extract
```

**Scenario 3: Python Library (requests)**
```bash
python scripts/create_skill_from_docs.py \
  --skill-name test-requests-lib \
  --from-docs path/to/requests_docs.md \
  --doc-type library
```

**Success Criteria for Each:**
- [ ] Skill generates without errors
- [ ] validate_skill.py passes
- [ ] Templates are syntactically valid
- [ ] Guardrails generated for documented pitfalls
- [ ] SKILL.md < 500 lines

**Deliverables:**
- [ ] 3+ end-to-end tests passing
- [ ] Test documentation
- [ ] Automated test runner

---

**7.3: User Acceptance Testing** ⏱️ 2 days

**Test with Real Documentation:**
- [ ] Generate skill for gh (GitHub CLI)
- [ ] Generate skill for uv (Python package manager)
- [ ] Generate skill for a REST API (Stripe, Twilio, etc.)

**Quality Checks:**
- [ ] Generated templates actually work
- [ ] Guardrails catch real issues
- [ ] SKILL.md is clear and useful
- [ ] Research log shows transparency

**Feedback Loop:**
- [ ] Collect issues from testing
- [ ] Prioritize fixes
- [ ] Iterate on templates and generation logic

---

### Phase 8: Documentation & Examples
**Duration:** 3-4 days
**Priority:** P1 (Essential for adoption)

#### Objectives
Create comprehensive documentation and example skills.

#### Tasks

**8.1: Write Main SKILL.md** ⏱️ 1 day

**Sections:**
```markdown
---
name: skill-creator-from-docs
description: |
  Automate creation of documentation-based Claude Code skills with templates,
  guardrails, and validation. Extracts workflows from docs (CLI/API/library),
  synthesizes usable templates, generates multi-layered guardrails, and produces
  complete skills in < 30 minutes.

  Use when: creating skills from documentation, automating skill boilerplate,
  extracting patterns from API/CLI docs, or building consistent skill quality.

  Keywords: skill creator, create from docs, documentation extraction, template
  synthesis, skill automation, crawl4ai integration, skill generation
---

# skill-creator-from-docs

Create high-quality Claude Code skills automatically from documentation.

## Quick Start

```bash
# Interactive mode
python scripts/create_skill_from_docs.py

# Direct mode
python scripts/init_skill.py my-skill-name \
  --from-docs https://tool-docs.com \
  --auto-extract
```

## How It Works

[9-phase workflow overview]

## Generated Skill Structure

[File structure explanation]

## Examples

See `examples/` for generated skills:
- crawl4ai-cli (CLI tool)
- stripe-api (REST API)
- requests-lib (Python library)

## Configuration

[Customization options]

## Troubleshooting

[Common issues and solutions]
```

**Deliverables:**
- [ ] Complete SKILL.md
- [ ] Follows skill-creator standards
- [ ] < 500 lines
- [ ] Validates successfully

---

**8.2: Create Reference Documentation** ⏱️ 1 day

**New References:**
- [ ] `doc_extraction_patterns.md` - How to identify tool types, extract patterns
- [ ] `template_synthesis_guide.md` - Example → template conversion strategies
- [ ] `automated_research_protocol.md` - Perplexity integration, trigger conditions

**Adapted References:**
- [ ] `research_protocol.md` - Adapt for automated extraction
- [ ] `detailed_process_steps.md` - Document 9-phase workflow
- [ ] `comprehensive_checklist.md` - Phase-based checklist for doc-based skills

**Deliverables:**
- [ ] 3 new reference docs
- [ ] 3 adapted references
- [ ] All cross-references updated

---

**8.3: Create Example Skills** ⏱️ 1-2 days

**Generate 3 Example Skills:**

**Example 1: crawl4ai-cli (Dogfooding)**
```bash
python scripts/create_skill_from_docs.py \
  --skill-name crawl4ai-example \
  --from-docs https://crawl4ai.com/docs \
  --doc-type cli
```

**Example 2: gh (GitHub CLI)**
```bash
python scripts/create_skill_from_docs.py \
  --skill-name gh-cli-example \
  --from-docs https://cli.github.com/manual \
  --doc-type cli
```

**Example 3: Anthropic API**
```bash
python scripts/create_skill_from_docs.py \
  --skill-name anthropic-api-example \
  --from-docs https://docs.anthropic.com/api \
  --doc-type api
```

**For Each Example:**
- [ ] Document generation process
- [ ] Highlight generated templates
- [ ] Show guardrails in action
- [ ] Include research log

**Deliverables:**
- [ ] 3 complete example skills
- [ ] examples/README.md with comparisons
- [ ] Lessons learned documented

---

### Phase 9: Polish & Release
**Duration:** 2-3 days
**Priority:** P1 (Final quality)

#### Objectives
Final refinements and preparation for use.

#### Tasks

**9.1: Performance Optimization** ⏱️ 1 day

**Targets:**
- [ ] Skill generation < 30 minutes for average docs
- [ ] Template synthesis < 5 minutes
- [ ] Validation < 30 seconds

**Optimizations:**
- [ ] Parallel processing for doc extraction
- [ ] Cache Perplexity results
- [ ] Optimize analyzer heuristics

---

**9.2: Error Handling & User Experience** ⏱️ 1 day

**Improvements:**
- [ ] Clear error messages for each phase
- [ ] Progress indicators during generation
- [ ] Helpful suggestions on failures
- [ ] Rollback on critical errors

**Example Error Handling:**
```python
try:
    corpus = doc_extractor.extract(url)
except CrawlError as e:
    print(f"❌ Failed to crawl {url}")
    print(f"   Reason: {e.message}")
    print(f"   Suggestion: Try providing markdown docs directly")
    print(f"   Command: python scripts/create_skill_from_docs.py --from-docs path/to/docs.md")
    sys.exit(1)
```

---

**9.3: Final Validation & Packaging** ⏱️ 1 day

**Checklist:**
- [ ] All scripts have --help text
- [ ] All scripts tested with edge cases
- [ ] Documentation complete and accurate
- [ ] Example skills validate successfully
- [ ] validate_skill.py passes on skill-creator-from-docs itself
- [ ] Token efficiency measured (should save ≥ 50% vs manual)
- [ ] Multi-model tested (Haiku, Sonnet, Opus)

**Package:**
```bash
python scripts/package_skill.py skill-creator-from-docs
```

---

## Dependencies & Prerequisites

### Required
- **Python ≥ 3.9** (for type hints and async)
- **crawl4ai-cli skill** (for URL documentation extraction)
- **Perplexity MCP** (for gap research)
- **PyYAML** (for SKILL.md frontmatter)
- **skill-creator scripts** (validate_skill.py, package_skill.py)

### Optional
- **tiktoken** (for token analysis)
- **pytest** (for unit tests)
- **black** / **ruff** (for code formatting)

### Installation
```bash
# Core dependencies
pip install pyyaml requests

# Optional dependencies
pip install tiktoken pytest black ruff

# MCP servers
# Follow setup guides for crawl4ai-cli and Perplexity MCP
```

---

## Success Metrics

### Phase-Level Metrics

**Phase 1: Documentation Extraction**
- [ ] Successfully crawl 3+ documentation sources
- [ ] Extract ≥ 90% of code examples
- [ ] Classify tool type correctly ≥ 90% of time

**Phase 2: Template Synthesis**
- [ ] Generate valid templates from ≥ 80% of examples
- [ ] Template comments cover ≥ 90% of parameters
- [ ] Syntax validation passes ≥ 95% of templates

**Phase 3: Guardrail Generation**
- [ ] Guardrail coverage for 100% of documented pitfalls
- [ ] Validation scripts execute without errors
- [ ] Checklists reference all critical prerequisites

**Phase 4-8: Support & Generation**
- [ ] SKILL.md < 500 lines
- [ ] All referenced files exist
- [ ] validate_skill.py passes
- [ ] Multi-model testing successful

### Overall Metrics

**Performance:**
- Generate complete skill in < 30 minutes
- Template synthesis < 5 minutes per template
- Validation < 30 seconds

**Quality:**
- Validation pass rate ≥ 95%
- Template accuracy ≥ 90%
- User satisfaction ≥ 4/5 (from UAT)

**Efficiency:**
- Token savings ≥ 50% vs manual skill creation
- Reduce skill creation time by ≥ 70%
- Eliminate 100% of documented pitfalls

---

## Risk Management

### High-Risk Items

**Risk 1: Documentation Variance**
- **Issue:** Real-world docs may not follow expected patterns
- **Mitigation:** Build extensive heuristics, fallback to human review
- **Contingency:** Provide manual override options

**Risk 2: Perplexity MCP Availability**
- **Issue:** Research phase depends on external service
- **Mitigation:** Implement fallback to user prompt
- **Contingency:** Allow skipping research phase

**Risk 3: Template Synthesis Complexity**
- **Issue:** Converting examples to templates is hard
- **Mitigation:** Start with simple patterns, iterate based on testing
- **Contingency:** Provide template editing UI

**Risk 4: Scope Creep**
- **Issue:** Feature requests during development
- **Mitigation:** Strict adherence to SPECIFICATION.md
- **Contingency:** Maintain "future enhancements" backlog

### Medium-Risk Items

- Validation script compatibility across platforms
- crawl4ai-cli API changes
- Performance on very large documentation sets

---

## Timeline Summary

| Phase | Duration | Priority | Dependencies |
|-------|----------|----------|--------------|
| 0: Foundation Setup | 2-3 days | P0 | None |
| 1: Doc Extraction | 1 week | P0 | Phase 0 |
| 2: Template Synthesis | 1 week | P0 | Phase 1 |
| 3: Guardrail System | 4-5 days | P0 | Phase 1, 2 |
| 4: Support Assets | 3-4 days | P1 | Phase 1, 2 |
| 5: SKILL.md Generator | 3-4 days | P0 | Phase 1-4 |
| 6: Orchestration & CLI | 3-4 days | P0 | Phase 1-5 |
| 7: Testing & Validation | 1 week | P0 | Phase 1-6 |
| 8: Documentation & Examples | 3-4 days | P1 | Phase 7 |
| 9: Polish & Release | 2-3 days | P1 | Phase 8 |

**Total Estimated Duration:** 4-6 weeks (depending on complexity and testing iterations)

**Critical Path:** Phases 0 → 1 → 2 → 3 → 5 → 6 → 7

---

## Next Steps

### Immediate Actions (This Week)

1. **Set up development environment**
   ```bash
   cd /Users/dallascrilley/PAI/.claude/skills/skill-creator-from-docs
   mkdir -p scripts templates references examples tests
   ```

2. **Copy reusable scripts from skill-creator**
   ```bash
   cp ../skill-creator/scripts/{validate_skill,package_skill,analyze_conciseness,quick_validate}.py scripts/
   ```

3. **Create RESEARCH_LOG_TEMPLATE.md**
   - Use template from Phase 0.4

4. **Begin Phase 1.1: doc_extractor.py**
   - Start with markdown processing (simpler)
   - Add URL extraction with crawl4ai-cli

### Short-term Goals (Week 2-3)

- Complete Phase 1 (Documentation Extraction)
- Complete Phase 2 (Template Synthesis)
- Begin Phase 3 (Guardrails)

### Medium-term Goals (Week 4-5)

- Complete Phases 3-6 (Guardrails through Orchestration)
- Begin comprehensive testing (Phase 7)

### Long-term Goals (Week 6+)

- Complete testing and documentation
- Polish and release
- Dogfood the skill to create more skills

---

## Questions & Decisions Needed

**Before Starting:**
- [ ] Confirm Perplexity MCP is set up and working
- [ ] Confirm crawl4ai-cli skill is available
- [ ] Review and approve this roadmap

**During Development:**
- How to handle versioned documentation? (e.g., React 18 vs 19)
- What's the fallback if crawl4ai fails? (Manual markdown input only?)
- Should we support private/authenticated documentation?

**Before Release:**
- Where to publish example skills?
- How to handle updates to skill-creator base?
- Version numbering strategy?

---

## Conclusion

This roadmap provides a comprehensive, phased approach to building skill-creator-from-docs. The plan balances:

- **Reuse** of proven components from skill-creator (~65%)
- **Innovation** in automated extraction and synthesis
- **Quality** through comprehensive testing and validation
- **Usability** via clear documentation and examples

**Key Success Factors:**
1. Strict adherence to SPECIFICATION.md
2. Iterative testing with real documentation
3. Clear error handling and user feedback
4. Comprehensive documentation

**Estimated Effort:** 4-6 weeks with focused development

**Next Action:** Begin Phase 0 (Foundation Setup) immediately.
