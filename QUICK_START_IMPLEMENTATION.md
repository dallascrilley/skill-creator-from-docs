# Quick Start: Implementing skill-creator-from-docs

**For**: When you're ready to build this specialized skill creator
**Context**: Complete design in DESIGN.md, validation in VALIDATION_CRITERIA.md

---

## Implementation Roadmap

### Option 1: Full Implementation (4 weeks)
Build all phases sequentially with validation at each step.

### Option 2: MVP Implementation (1 week)
Build minimal viable product with core features only.

### Option 3: Prototype First (2-3 days)
Test feasibility with quick prototype before committing to full build.

---

## Recommended: Start with Prototype

**Why**: Validate parsing accuracy before building full system

### Prototype Scope (2-3 days)

**Goal**: Prove that automated detection works with real docs

**Build:**
1. `parse_docs.py` - Markdown parser only
2. `detect_commands.py` - CLI command detection
3. `detect_gotchas.py` - Warning extraction
4. Test script - Run against wordpress-management docs

**Success criteria:**
- Detect 90%+ of commands correctly
- Find all high-severity gotchas
- Categorize workflows vs reference content

**If successful** → Proceed to Phase 1 (full parser)
**If struggles** → Refine detection patterns or add LLM classification

### Prototype Implementation

**Step 1: Create parse_docs.py**

```python
#!/usr/bin/env python3
"""
Documentation Parser - Prototype

Parses markdown files and detects patterns:
- Commands (CLI syntax, API endpoints)
- Workflows (sequential procedures)
- Gotchas (warnings, errors)
- Examples (code blocks)
- References (tables, lists)
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import json


@dataclass
class Command:
    name: str
    syntax: str
    source_file: str
    line_number: int
    type: str  # 'cli' or 'api'


@dataclass
class Workflow:
    name: str
    steps: List[str]
    source_file: str
    line_number: int


@dataclass
class Gotcha:
    warning: str
    severity: str  # 'high', 'medium', 'low'
    fix: str
    source: str
    source_file: str
    line_number: int


class DocumentationParser:
    """Parse documentation and detect patterns."""

    def __init__(self):
        self.commands = []
        self.workflows = []
        self.gotchas = []
        self.examples = []
        self.references = []

    def parse_file(self, file_path: str):
        """Parse a markdown file."""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            # Detect commands
            self._detect_commands(line, file_path, i)

            # Detect gotchas
            self._detect_gotchas(line, file_path, i)

        # Detect workflows (multi-line)
        self._detect_workflows(lines, file_path)

    def _detect_commands(self, line: str, file_path: str, line_num: int):
        """Detect CLI commands and API endpoints."""

        # CLI patterns
        cli_patterns = [
            r'```bash\n(.+?)\n',  # Bash code blocks
            r'`([a-z-]+\s+[a-z-]+.*?)`',  # Inline commands
            r'^\$\s+(.+)$',  # Shell prompt
        ]

        for pattern in cli_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                cmd = Command(
                    name=match.split()[0] if match.split() else match,
                    syntax=match.strip(),
                    source_file=file_path,
                    line_number=line_num,
                    type='cli'
                )
                self.commands.append(cmd)

    def _detect_gotchas(self, line: str, file_path: str, line_num: int):
        """Detect warnings and common errors."""

        # Gotcha indicators
        indicators = [
            (r'⚠️|WARNING|IMPORTANT|CAUTION', 'high'),
            (r"Don't|Never|Avoid|Do not", 'high'),
            (r'Note:|Tip:|Remember:', 'medium'),
            (r'Common error|Known issue|Limitation', 'high'),
        ]

        for pattern, severity in indicators:
            if re.search(pattern, line, re.IGNORECASE):
                # Extract full warning (this line + context)
                gotcha = Gotcha(
                    warning=line.strip(),
                    severity=severity,
                    fix='',  # Extract from next lines in full impl
                    source=file_path,
                    source_file=file_path,
                    line_number=line_num
                )
                self.gotchas.append(gotcha)

    def _detect_workflows(self, lines: List[str], file_path: str):
        """Detect sequential procedures (multi-line)."""

        current_workflow = None
        steps = []

        for i, line in enumerate(lines, 1):
            # Start of numbered list
            if re.match(r'^\d+\.\s+', line):
                if current_workflow is None:
                    # Find workflow name (previous heading)
                    for j in range(i-1, max(0, i-10), -1):
                        if lines[j].startswith('##'):
                            current_workflow = lines[j].strip('# \n')
                            break

                step = re.sub(r'^\d+\.\s+', '', line).strip()
                steps.append(step)

            # End of numbered list
            elif steps and not line.strip():
                if current_workflow and steps:
                    workflow = Workflow(
                        name=current_workflow,
                        steps=steps,
                        source_file=file_path,
                        line_number=i - len(steps)
                    )
                    self.workflows.append(workflow)

                current_workflow = None
                steps = []

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON output."""
        return {
            'commands': [asdict(c) for c in self.commands],
            'workflows': [asdict(w) for w in self.workflows],
            'gotchas': [asdict(g) for g in self.gotchas],
            'summary': {
                'total_commands': len(self.commands),
                'total_workflows': len(self.workflows),
                'total_gotchas': len(self.gotchas),
                'high_severity_gotchas': len([g for g in self.gotchas if g.severity == 'high'])
            }
        }


def main():
    parser = argparse.ArgumentParser(description='Parse documentation files')
    parser.add_argument('files', nargs='+', help='Documentation files to parse')
    parser.add_argument('-o', '--output', help='Output JSON file', default='parsing-results.json')

    args = parser.parse_args()

    doc_parser = DocumentationParser()

    for file_path in args.files:
        print(f"Parsing {file_path}...")
        doc_parser.parse_file(file_path)

    results = doc_parser.to_dict()

    # Print summary
    print("\n" + "="*60)
    print("PARSING RESULTS")
    print("="*60)
    print(f"Commands detected: {results['summary']['total_commands']}")
    print(f"Workflows detected: {results['summary']['total_workflows']}")
    print(f"Gotchas detected: {results['summary']['total_gotchas']}")
    print(f"  High severity: {results['summary']['high_severity_gotchas']}")
    print("="*60 + "\n")

    # Save to JSON
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to {args.output}")


if __name__ == '__main__':
    main()
```

**Step 2: Test with wordpress-management**

```bash
# Create prototype directory
mkdir -p /Users/dallascrilley/PAI/.claude/skills/skill-creator-from-docs/prototype

# Copy parser
cp parse_docs.py prototype/

# Run against wordpress-management
cd prototype
python parse_docs.py \
  /Users/dallascrilley/PAI/.claude/skills/wordpress-management/SKILL.md \
  -o wordpress-results.json

# Review results
cat wordpress-results.json | jq '.summary'
cat wordpress-results.json | jq '.gotchas[] | select(.severity == "high")'
cat wordpress-results.json | jq '.commands[] | .name' | sort | uniq
```

**Step 3: Evaluate Accuracy**

```bash
# Manual verification
echo "Expected commands:"
grep -E '^\s*```bash|^\$|^`[a-z]' \
  /Users/dallascrilley/PAI/.claude/skills/wordpress-management/SKILL.md | wc -l

echo "Detected commands:"
cat wordpress-results.json | jq '.summary.total_commands'

# Check gotchas
echo "High-severity gotchas detected:"
cat wordpress-results.json | jq '.gotchas[] | select(.severity == "high") | .warning'

# Compare to manual review
echo "Did we catch: 'WPEngine blocks SCP'? 'Chunk files > 50KB'? 'Backup before editing'?"
```

**Step 4: Refine or Proceed**

**If 90%+ accuracy:**
→ Proceed to Phase 1 (full implementation)

**If 70-89% accuracy:**
→ Refine patterns, add more detection rules, try again

**If < 70% accuracy:**
→ Consider LLM-based classification instead of regex patterns

---

## MVP Implementation (Week 1)

**If prototype succeeds**, build minimal viable product:

### MVP Scope

**Core features:**
1. Parse markdown files
2. Detect commands, workflows, gotchas
3. Generate basic script stubs (no --help yet)
4. Generate SKILL.md template with detected patterns
5. Simple validation (command coverage only)

**Excluded from MVP:**
- JSON/YAML/HTML parsing (markdown only)
- crawl4ai-cli integration (URLs)
- Interactive approval flow (auto-approve all)
- Full validation suite (just command coverage)
- Template generation (assets/)

**Deliverable**: Working tool that creates basic skill from markdown docs

### MVP Implementation Steps

**Day 1: Enhance Parser**
- Multi-file support
- Better workflow detection
- Example extraction
- Reference content detection

**Day 2: Script Generation**
- `generate_script_stubs.py` - Basic template
- Test with wordpress-management commands

**Day 3: SKILL.md Generation**
- `generate_skill_md.py` - Template with detected patterns
- Workflow sections
- Gotcha section

**Day 4: Orchestration**
- `init_from_docs.py` - Combine all steps
- Auto-approve mode (no interaction)
- Test end-to-end

**Day 5: Validation & Polish**
- `validate_doc_skill.py` - Command coverage check
- Test with 2-3 real skills
- Fix bugs, refine output

### MVP Test

**Create wordpress-cli from wordpress-management docs:**

```bash
python scripts/init_from_docs.py wordpress-cli \
  --docs /path/to/wordpress-management/SKILL.md \
  --auto-approve

# Expected output:
# ✅ Detected 12 commands
# ✅ Detected 3 workflows
# ✅ Detected 5 gotchas
# ✅ Generated 12 script stubs
# ✅ Created SKILL.md (350 lines)
# ✅ Validation: 12/12 commands have scripts
```

**Compare:**
- Original: wordpress-management (manual, suboptimal)
- Generated: wordpress-cli (automated, follows patterns)

**Measure:**
- Time saved (manual: 4 hours, automated: 20 minutes)
- Quality (command coverage, gotcha surfacing, structure)

---

## Full Implementation (4 weeks)

**If MVP succeeds**, proceed with full feature set:

### Phase 1: Complete Parser (Week 1)
- Multi-format support (MD, JSON, YAML, HTML)
- LLM classification for ambiguous patterns
- URL scraping via crawl4ai-cli
- Detailed extraction (params, flags, examples)

### Phase 2: Advanced Generation (Week 2)
- Script stubs with --help integration
- Error handling templates
- Template generation (assets/)
- Progressive disclosure (references/)

### Phase 3: Interactive Workflow (Week 3)
- Approval prompts for each category
- Selective mode (-s flag)
- Preview before generation
- Customization options

### Phase 4: Production Ready (Week 4)
- Full validation suite (7 checks)
- Comprehensive testing
- Documentation and examples
- Integration with skill-creator

---

## Decision Points

### Before Starting Prototype
- [ ] Review DESIGN.md
- [ ] Approve validation criteria
- [ ] Confirm approach makes sense

### After Prototype (Day 3)
- [ ] 90%+ detection accuracy?
  - Yes → Proceed to MVP
  - No → Refine or reconsider

### After MVP (Day 7)
- [ ] Tool creates usable skills?
  - Yes → Proceed to full implementation
  - No → Identify gaps, fix MVP

### After Phase 2 (Week 2)
- [ ] Generated skills better than manual?
  - Yes → Continue
  - No → Revisit approach

---

## Success Criteria

**Prototype success:**
- Detects 90%+ of commands from markdown
- Finds all high-severity gotchas
- Categorizes workflows correctly

**MVP success:**
- Creates skill from markdown in < 5 minutes
- Generated skill passes basic validation
- Command coverage: 100%

**Full implementation success:**
- 50-70% time savings vs manual
- 95%+ gotcha detection
- Passes all 7 validation checks
- Works with multiple doc formats

---

## Quick Commands Reference

**Prototype:**
```bash
# Parse docs
python prototype/parse_docs.py docs/*.md -o results.json

# Review
cat results.json | jq '.summary'
```

**MVP:**
```bash
# Create skill from docs
python scripts/init_from_docs.py skill-name \
  --docs ./docs.md \
  --auto-approve

# Validate
python scripts/validate_doc_skill.py skill-name/
```

**Full:**
```bash
# Interactive mode
python scripts/init_from_docs.py skill-name \
  --docs ./docs.md \
  --url https://example.com/docs \
  --api-spec ./api.json

# Selective approval
python scripts/init_from_docs.py skill-name \
  --docs ./docs.md \
  -s  # Prompt for each category
```

---

## Next Action

**Choose your path:**

1. **Prototype first** (recommended)
   - 2-3 days, low risk
   - Validates approach
   - Start: Create prototype/parse_docs.py

2. **MVP directly** (if confident)
   - 1 week, medium risk
   - Skip prototype validation
   - Start: Build full parser

3. **Full implementation** (maximum features)
   - 4 weeks, high commitment
   - All features from day 1
   - Start: Phase 1 planning

**Recommendation**: Start with prototype to validate detection accuracy before committing to full build.

---

**Ready to start?**

```bash
# Create prototype directory
mkdir -p /Users/dallascrilley/PAI/.claude/skills/skill-creator-from-docs/prototype

# Start building parse_docs.py
# (Template provided above)
```

---

**End of Quick Start Implementation Guide**
