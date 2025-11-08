# Skill Compliance Checklist ✅

**Purpose**: Pre-publish verification checklist (use before committing)  
**If you're new**: Read [00_START_HERE.md](00_START_HERE.md) first  
**For detailed guidance**: See [references/comprehensive_checklist.md](references/comprehensive_checklist.md)  
**For best practices**: See [references/best_practices_checklist.md](references/best_practices_checklist.md)

**Print this page and check off items as you build your skill.**

---

## PRE-BUILD CHECKLIST

Before starting a new skill, verify:

- [ ] Read [00_START_HERE.md](00_START_HERE.md) for workflow overview
- [ ] Read [references/research_protocol.md](references/research_protocol.md) for mandatory research workflow
- [ ] Read [SKILL.md](SKILL.md) for complete process
- [ ] Checked skill doesn't already exist
- [ ] Checked official Anthropic skills: https://github.com/anthropics/skills
- [ ] Identified target use cases (3-5 concrete examples)
- [ ] Verified this is atomic (one domain, not a bundle)
- [ ] Created TodoWrite checklist from [SKILL.md](SKILL.md) process

---

## RESEARCH CHECKLIST

**Mandatory research workflow (no exceptions):**

- [ ] **Query Perplexity MCP** (≥2 queries with `--recency 365`)
  - [ ] Common commands/endpoints query
  - [ ] Authentication/CLI query
  - [ ] Captured latest versions, endpoints, auth requirements
- [ ] **Analyze GitHub repository** (≥1 repo, ≥3 lessons/patterns)
  - [ ] Found actively maintained repo (commits within 24 months)
  - [ ] Reviewed README + key implementation files
  - [ ] Documented ≥3 lessons/patterns/takeaways with file paths
- [ ] **Created research log**: `python scripts/init_skill.py <name> --path <path> --create-research-log`
- [ ] **Built working example** from scratch
- [ ] **Documented all errors** encountered and fixes
- [ ] **Identified token savings** vs manual setup (≥50% target)

---

## INITIALIZATION CHECKLIST

- [ ] **Initialized from universal template** (recommended: full automation):
  ```bash
  python scripts/init_skill.py <skill-name> --path <path> \
    --template skill-skeleton --auto-fill --create-research-log
  ```
- [ ] **Template structure verified** (SKILL.md, README.md, directories)
- [ ] **All [TODO:] markers identified** for replacement
- [ ] **Reviewed section markers** in SKILL.md (HTML comments indicate CORE vs optional sections)
- [ ] **Deleted optional sections** marked with `<!-- DELETE if ... -->` that don't apply
- [ ] **Kept core sections** (Quick Start, Critical Rules, Common Patterns)

---

## YAML FRONTMATTER CHECKLIST

`SKILL.md` frontmatter is complete and correct:

- [ ] **name**: Present, lowercase hyphen-case (e.g., `my-skill-name`)
- [ ] **name**: Matches directory name exactly
- [ ] **name**: Max 64 characters
- [ ] **description**: Present and comprehensive (3+ sentences, <1024 chars)
- [ ] **description**: Uses third-person ("This skill should be used when..." not "Use this skill when...")
- [ ] **description**: Includes "Use when" scenarios
- [ ] **description**: Includes keywords (technologies, use cases, error messages)
- [ ] **license**: Present (e.g., `MIT` or `Complete terms in LICENSE.txt`)

**Example:**
```yaml
---
name: my-skill-name
description: |
  This skill provides comprehensive knowledge for [technology]. It should be used when
  building projects with [use case], configuring [feature], or encountering [error].

  Keywords: technology, use-case, error-message, related-tech
license: MIT
---
```

---

## SKILL.MD BODY CHECKLIST

Skill instructions are clear and actionable:

- [ ] **< 500 lines** total (use `references/` if larger)
- [ ] **< 5000 tokens** total (run `analyze_conciseness.py`)
- [ ] **Imperative/infinitive form** ("To do X, run Y" not "You should")
- [ ] **NOT second person** (avoid "you should")
- [ ] **Quick start section** (< 5 minutes to first result)
- [ ] **Step-by-step instructions** with code examples
- [ ] **Configuration examples** with actual values
- [ ] **Critical rules section** ("Always Do" / "Never Do")
- [ ] **Common issues section** with sources (GitHub issues, etc.)
- [ ] **Dependencies clearly listed**
- [ ] **References to bundled resources** (scripts/, references/, assets/)
- [ ] **Official documentation links** included
- [ ] **Package versions documented** with "Last Verified" date
- [ ] **No placeholder text** ([TODO:], FIXME, etc.) - All template placeholders replaced
- [ ] **Optional sections removed** (deleted sections marked `<!-- DELETE if ... -->` that don't apply)
- [ ] **No hedge words** (basically, essentially, typically, generally)

---

## BUNDLED RESOURCES CHECKLIST

Resources are properly organized:

- [ ] **scripts/**: Executable code placed here (Python, Bash, etc.)
  - [ ] Scripts have explicit error handling with fallbacks
  - [ ] Scripts have proper permissions (chmod +x)
  - [ ] Scripts documented with usage examples
- [ ] **references/**: Documentation files placed here (schemas, guides)
  - [ ] Table of contents for files > 100 lines
  - [ ] Referenced directly from SKILL.md (one level deep)
- [ ] **assets/**: Output files placed here (templates, images, fonts)
  - [ ] Templates are complete and tested
  - [ ] No hardcoded paths
- [ ] **All resources referenced** in SKILL.md body
- [ ] **No hardcoded secrets** or credentials
- [ ] **Template boilerplate deleted** (removed unused placeholder files from scripts/, references/, assets/)
- [ ] **Optional SKILL.md sections deleted** (removed sections marked `<!-- DELETE if ... -->` that don't apply)

---

## README.MD CHECKLIST

Quick reference is complete (if complex skill):

- [ ] **Status badge present** (Production Ready / Beta / Experimental)
- [ ] **Last Updated date** current
- [ ] **Production tested evidence** included (URL, screenshot, repo link)
- [ ] **Auto-trigger keywords comprehensive**
  - [ ] Primary keywords (3-5 exact tech names)
  - [ ] Secondary keywords (5-10 related terms)
  - [ ] Error-based keywords (2-5 common errors)
- [ ] **"What This Skill Does"** section clear
- [ ] **"Known Issues Prevented"** table with sources
- [ ] **"When to Use / Not Use"** sections present
- [ ] **Token efficiency metrics** documented
- [ ] **Quick usage example** included

---

## EVALUATION-DRIVEN DEVELOPMENT (EDD) CHECKLIST

**CRITICAL:** Create evaluations BEFORE extensive documentation.

- [ ] **Baseline testing** completed (ran Claude WITHOUT skill)
- [ ] **3-5 test scenarios** created from concrete examples
- [ ] **Gaps documented** (information, efficiency, quality)
- [ ] **Success criteria defined** for each scenario
- [ ] **Minimal documentation added** addressing only identified gaps
- [ ] **Re-tested** after additions
- [ ] **Scenarios pass consistently** (>90% success rate)

---

## TOKEN EFFICIENCY CHECKLIST

Skill provides measurable value:

- [ ] **Manual setup tokens measured** (before skill)
- [ ] **With-skill tokens measured** (using skill)
- [ ] **Token savings ≥ 50%** (required threshold)
- [ ] **Errors encountered documented** (manual vs skill)
- [ ] **Error prevention = 100%** (all known errors prevented)
- [ ] **Metrics documented** in README.md or SKILL.md
- [ ] **Ran `analyze_conciseness.py`** and addressed feedback

**Typical Metrics**:
```
Manual:  ~12,000 tokens, 2-3 errors
Skill:   ~4,500 tokens, 0 errors
Savings: ~62%, 100% error prevention
```

---

## TESTING CHECKLIST

Skill works in practice:

- [ ] **Skill files in correct location**
- [ ] **Tested auto-discovery**: Claude suggests skill when relevant
- [ ] **Built example project** using skill templates/assets
- [ ] **All templates work** without errors
- [ ] **All scripts execute** successfully
- [ ] **Configuration files valid**
- [ ] **Package versions correct**
- [ ] **Multi-model testing**:
  - [ ] Tested with Haiku (enough guidance?)
  - [ ] Tested with Sonnet (clear and efficient?)
  - [ ] Tested with Opus (avoids over-explaining?)
- [ ] **Production build succeeds** (if applicable)
- [ ] **Deployed example** (if applicable)

---

## VALIDATION CHECKLIST

Automated and manual validation:

- [ ] **Quick validation**: `python scripts/quick_validate.py <skill-dir>`
- [ ] **Full validation**: `python scripts/validate_skill.py --full-check <skill-dir>`
- [ ] **All validation checks pass**
- [ ] **Compared against** [references/best_practices_checklist.md](references/best_practices_checklist.md)
- [ ] **Reviewed** [references/core_principles.md](references/core_principles.md) compliance
- [ ] **Compared against official Anthropic standards**: https://github.com/anthropics/skills/blob/main/agent_skills_spec.md
- [ ] **Referenced working examples** in `examples/` directory
- [ ] **No deprecated patterns** used
- [ ] **No non-standard frontmatter fields** (except allowed-tools, metadata)
- [ ] **Writing style consistent** (imperative, third-person)

---

## QUALITY GATES CHECKLIST

Before committing (DO NOT SKIP):

- [ ] **Frontmatter complete** (name + description with trigger terms)
- [ ] **SKILL.md < 500 lines** (use references/ if larger)
- [ ] **Tested locally** (skill actually works when Claude uses it)
- [ ] **No [TODO:] markers** left in committed files
- [ ] **Read entire SKILL.md out loud** (catches awkward phrasing)
- [ ] **Built example in fresh directory** (no dependencies on existing setup)
- [ ] **No errors in console** during development
- [ ] **No warnings** about deprecated packages
- [ ] **Git status clean** (no untracked files)
- [ ] **Skill name matches directory name**
- [ ] **All relative paths correct** (forward slashes)
- [ ] **No debug code** or console.log statements
- [ ] **All links work**

---

## PACKAGING CHECKLIST

Prepare for distribution:

- [ ] **Ran `package_skill.py <skill-dir>`**
- [ ] **Package created successfully**
- [ ] **Package contains all required files**
- [ ] **Validation report reviewed**

---

## DOCUMENTATION CHECKLIST

All required documentation present:

- [ ] **SKILL.md complete**
- [ ] **README.md complete** (if complex skill)
- [ ] **LICENSE field** in frontmatter
- [ ] **Research log** in `planning/research-logs/<skill-name>.md`
- [ ] **Templates tested** and documented
- [ ] **Scripts documented** with usage examples
- [ ] **References accurate** and current
- [ ] **Links to official docs** work
- [ ] **Version numbers current**
- [ ] **"Last Updated" date** accurate

---

## FINAL SIGN-OFF

I certify that:

- [ ] ✅ All checklists above are complete
- [ ] ✅ Skill tested and working in realistic scenarios
- [ ] ✅ Compliant with official Anthropic standards
- [ ] ✅ Documentation accurate and current
- [ ] ✅ Token efficiency ≥ 50%
- [ ] ✅ Zero errors from documented issues
- [ ] ✅ Multi-model testing complete (Haiku, Sonnet, Opus)
- [ ] ✅ All validation checks pass
- [ ] ✅ Ready for production use

**Skill Name**: ______________________
**Date**: ______________________
**Builder**: ______________________
**Verified By**: ______________________

---

**If all boxes checked: SHIP IT! 🚀**

**If any boxes unchecked**: Go back and complete those items before committing.

---

## Quick Links

- [00_START_HERE.md](00_START_HERE.md) - Navigation hub
- [SKILL.md](SKILL.md) - Complete creation process
- [QUICK_WORKFLOW.md](QUICK_WORKFLOW.md) - 5-minute workflow
- [templates/README.md](templates/README.md) - Template customization guide
- [references/comprehensive_checklist.md](references/comprehensive_checklist.md) - Detailed phase checklist
- [references/best_practices_checklist.md](references/best_practices_checklist.md) - Best practices reference
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- [examples/](examples/) - Working skill examples

---

## Minimum Quality Gates

If time-constrained, these are ABSOLUTE MINIMUM:

1. ✅ **Frontmatter Complete**: name + description with trigger terms
2. ✅ **< 500 Lines**: SKILL.md body under 500 lines
3. ✅ **Tested Locally**: Skill actually works when Claude uses it
4. ✅ **Token Savings ≥ 50%**: Measured improvement over manual approach
5. ✅ **No Placeholders**: No [TODO:], FIXME, or unfinished content
6. ✅ **Validation Passes**: `validate_skill.py --full-check` succeeds
7. ✅ **3+ Scenarios**: Tested with at least 3 realistic scenarios

**If any of these fail, DO NOT PACKAGE. Fix and re-test.**
