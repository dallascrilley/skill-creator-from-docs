# Quick Workflow: Build a Skill in 5 Minutes

**Purpose**: Fast-track workflow for experienced builders (5-minute path)  
**If you're new**: Read [00_START_HERE.md](00_START_HERE.md) first  
**If you need detailed steps**: See [SKILL.md](SKILL.md)

**Goal**: Create a production-ready skill from scratch as fast as possible.

**Prerequisites**: Read [00_START_HERE.md](00_START_HERE.md) once

---

## The 5-Minute Workflow

### Step 1: Initialize from Template (30 seconds)

```bash
# Navigate to where you want to create the skill
cd /path/to/skills/

# For simple skills (recommended for quick workflow)
python /path/to/skill-creator/scripts/init_skill.py my-skill-name \
  --path . --template minimal-skeleton --auto-fill

# For complex skills (if you need optional sections)
python /path/to/skill-creator/scripts/init_skill.py my-skill-name \
  --path . --template skill-skeleton --auto-fill --create-research-log

cd my-skill-name/
```

**Done when**: You have a `my-skill-name/` directory with SKILL.md and README.md

---

### Step 2: Fill Remaining TODOs in SKILL.md (2 minutes)

Open `SKILL.md` and fill remaining [TODO:] markers:

1. **Description** (in YAML frontmatter):
   ```yaml
   description: |
     This skill provides... [write 3-5 sentences]
     
     Use when: [scenarios]
     
     Keywords: [tech, errors, use-cases]
   ```

2. **Core Instructions**:
   - Quick Start section (how to use in <5 min)
   - Critical Rules (Always Do / Never Do)
   - Common patterns

**Done when**: All [TODO:] markers replaced with real content

---

### Step 3: Add Keywords to README.md (30 seconds)

Open `README.md` and add auto-trigger keywords:
- Primary: Exact technology names
- Secondary: Related terms
- Errors: Common error messages

**Done when**: Keywords cover all ways someone might mention this skill

---

### Step 4: Validate (30 seconds)

```bash
# Quick validation
python /path/to/skill-creator/scripts/quick_validate.py .

# Full validation (if time permits)
python /path/to/skill-creator/scripts/validate_skill.py --full-check .
```

**Done when**: Validation passes (or warnings are acceptable)

---

### Step 5: Test Discovery (30 seconds)

Ask Claude Code to use the skill:
```
"Use the my-skill-name skill to help me with [task]"
```

**Done when**: Claude discovers and uses the skill

---

## Detailed Workflow (For First-Time Builders)

### Phase 1: Research (30-60 minutes)

**Mandatory for first-time builders.** Skip only if you're already an expert in the domain AND have verified current package versions.

1. **Query Perplexity MCP** (required)
   ```bash
   perplexity_search_web "<platform> common commands 2025" --recency 365
   perplexity_search_web "<platform> authentication cli" --recency 365
   ```

2. **Analyze GitHub repository**
   - Find actively maintained repo (recent commits within 24 months)
   - Extract ≥3 lessons/patterns/takeaways
   - Document file paths where patterns found

3. **Create research log**
   ```bash
   python /path/to/skill-creator/scripts/init_skill.py my-skill-name \
     --path . --create-research-log
   ```
   - Document: sources, versions, issues found
   - Store in `planning/research-logs/my-skill-name.md`

4. **Build working example**
   - Start from scratch
   - Document every error you hit
   - Save working example

**Done when**: You have a working example and research log

---

### Phase 2: Initialize & Customize (10-20 minutes)

1. **Initialize from template**
   ```bash
   python /path/to/skill-creator/scripts/init_skill.py my-skill-name \
     --path . --template skill-skeleton --auto-fill --create-research-log
   ```

2. **Update frontmatter**
   - `name`: Already filled by --auto-fill
   - `description`: 3+ sentences, third-person, with keywords
   - `license`: MIT (or your choice)

3. **Fill SKILL.md sections**
   - Quick Start (< 5 min to first result)
   - Critical Rules (what to do/avoid)
   - Known Issues (with GitHub links)
   - Configuration examples
   - Common patterns

4. **Add README keywords**
   - Primary (3-5): Exact tech names
   - Secondary (5-10): Related terms
   - Errors (2-5): Common error messages

5. **Add resources** (if applicable)
   - `scripts/`: Executable code
   - `references/`: Documentation
   - `assets/`: Templates, images

6. **Delete template boilerplate**
   - Remove placeholder files you won't use
   - Clean up example scripts/assets if not needed

**Done when**: All [TODO:] markers replaced with real content

---

### Phase 3: Validate & Test (5-10 minutes)

1. **Run validation**
   ```bash
   # Quick check
   python /path/to/skill-creator/scripts/quick_validate.py .
   
   # Full validation
   python /path/to/skill-creator/scripts/validate_skill.py --full-check .
   ```

2. **Test discovery**
   - Open Claude Code
   - Mention the technology
   - Claude should suggest your skill

3. **Test templates** (if you added assets/)
   - Copy any templates from `assets/`
   - Build a project using them
   - Verify everything works

4. **Verify checklist**
   - Open [references/comprehensive_checklist.md](references/comprehensive_checklist.md)
   - Check off each item
   - Fix any that fail

**Done when**: All validation passes and skill is discoverable

---

### Phase 4: Measure & Iterate (5-10 minutes)

1. **Measure token efficiency**
   ```bash
   python /path/to/skill-creator/scripts/analyze_conciseness.py .
   ```
   - Document baseline vs with-skill tokens
   - Ensure ≥50% savings

2. **Test with multiple models**
   - Test with Haiku (enough guidance?)
   - Test with Sonnet (clear and efficient?)
   - Test with Opus (avoids over-explaining?)

3. **Package for distribution** (optional)
   ```bash
   python /path/to/skill-creator/scripts/package_skill.py .
   ```

**Done when**: Token efficiency measured, all models tested

---

## Time Estimates

| Task | First Time | Experienced | Notes |
|------|-----------|-------------|-------|
| Research | 30-60 min | Skip | Only needed once per domain |
| Initialize | 30 sec | 30 sec | `init_skill.py` handles it |
| Fill frontmatter | 2-5 min | 1-2 min | Faster with --auto-fill |
| Write instructions | 10-20 min | 5-10 min | Depends on complexity |
| Add keywords | 2 min | 1 min | Easy |
| Validate | 2-3 min | 1 min | Automated |
| Test discovery | 2-3 min | 1 min | Quick check |
| Measure efficiency | 5 min | 2 min | Optional but recommended |
| **Total** | **1-2 hours** | **15-20 min** | Faster after first skill |

---

## Quick Command Reference

```bash
# Initialize skill (with auto-fill and research log)
python /path/to/skill-creator/scripts/init_skill.py my-skill-name \
  --path . --template skill-skeleton --auto-fill --create-research-log

# Quick validation
python /path/to/skill-creator/scripts/quick_validate.py <skill-dir>

# Full validation
python /path/to/skill-creator/scripts/validate_skill.py --full-check <skill-dir>

# Analyze token usage
python /path/to/skill-creator/scripts/analyze_conciseness.py <skill-dir>

# Package skill
python /path/to/skill-creator/scripts/package_skill.py <skill-dir>

# Check package versions (if applicable)
npm view <package> version
```

---

## Common Shortcuts

### Experienced Builder Shortcuts

If you're building your 3rd+ skill, you can:

1. **Skip research** if you know the domain
2. **Copy similar skill** instead of template
   ```bash
   cp -r examples/document-skills/pdf/ my-new-skill/
   # Then find-replace to update
   ```
3. **Skip README** if skill is simple (just frontmatter matters)
4. **Skip test project** if templates are straightforward

### Using Existing Skills as Templates

Best examples to copy from (in `examples/`):

| Copy This | When Building |
|-----------|---------------|
| `document-skills/pdf/` | Document processing skill |
| `document-skills/docx/` | Office document skill |
| `slack-gif-creator/` | Creative tool skill |
| `webapp-testing/` | Testing/automation skill |

---

## Workflow Decision Tree

```
Do you know the domain well?
  ├─ YES → Skip research, go straight to initialize
  └─ NO  → Research first (30-60 min)

Is this your first skill?
  ├─ YES → Follow detailed workflow
  └─ NO  → Use 5-minute workflow

Is skill similar to existing skill?
  ├─ YES → Copy that skill and modify
  └─ NO  → Use init_skill.py with skill-skeleton template

Do you have working templates?
  ├─ YES → Add to assets/ directory
  └─ NO  → Skip assets/ for now

Do you have reference docs?
  ├─ YES → Add to references/ directory
  └─ NO  → Skip references/ for now

Do you have scripts?
  ├─ YES → Add to scripts/ directory
  └─ NO  → Skip scripts/ for now
```

---

## Quality Gates

Don't skip these, even when rushing:

1. ✅ **Frontmatter complete** (name + description + keywords)
2. ✅ **Validation passes** (`validate_skill.py --full-check`)
3. ✅ **No [TODO:] markers** left in committed files
4. ✅ **Tested discovery** (Claude can find and use skill)

Everything else can be improved later.

---

## What If Something Goes Wrong?

### Skill not discovered
- Verify frontmatter YAML is valid (run `validate_skill.py`)
- Add more keywords to description
- Check SKILL.md is < 500 lines
- Ensure `name` matches directory name exactly

### Validation fails
- Read error messages from `validate_skill.py`
- Check [references/troubleshooting.md](references/troubleshooting.md)
- Compare to working examples in `examples/`

### Can't think of good keywords
- Look at errors people search for
- Check Stack Overflow questions
- Review official docs examples
- See [references/auto_activation_patterns.md](references/auto_activation_patterns.md)

### Stuck on description
- Start with: "This skill provides..."
- Add: "Use when..."
- List: "Keywords:"
- See examples in `examples/` directory

### Templates don't work
- Test them in fresh directory
- Check for hardcoded paths
- Verify package versions current
- Run `validate_skill.py` to check structure

---

## Integration with Main Workflow

This quick workflow aligns with the main [SKILL.md](SKILL.md) process:

```
Step 1: Research & Plan      → Phase 1: Research
Step 2: Initialize          → Phase 2: Initialize & Customize
Step 3: Build Resources     → Phase 2: Add resources
Step 4: Write Content       → Phase 2: Customize
Step 5: Validate & Measure  → Phase 3: Validate & Test
Step 6: Test & Iterate      → Phase 4: Measure & Iterate
```

---

## Next Steps

After building your first skill:

1. Read [references/troubleshooting.md](references/troubleshooting.md)
2. Review [references/best_practices_checklist.md](references/best_practices_checklist.md)
3. Study working skills in `examples/` directory
4. Build second skill (will be much faster!)

---

**Remember**: The goal is production-ready skills, not perfect documentation. Ship it, then improve it!

**Most important**: Make sure Claude can discover and use the skill. Everything else is secondary.

**For complete process**: See [SKILL.md](SKILL.md) for detailed step-by-step guidance with quality checkpoints.
