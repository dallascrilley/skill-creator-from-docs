# Documentation-Driven Skill Validation Criteria

**Purpose**: Specialized validation checks for skills created from documentation sources

**Standard skill-creator validation** still applies (YAML frontmatter, < 500 lines, token efficiency ≥50%, etc.)

**Additional doc-specific validation:**

---

## 1. Command Coverage (100%)

**Requirement**: Every detected command must have either:
- Script wrapper in `scripts/`, OR
- Reference documentation in `references/`

**Why**: Ensures Claude has access to all documented functionality

**Check:**
```python
for command in detected_commands:
    has_wrapper = exists(f"scripts/{command_to_script_name(command)}.py")
    has_reference = command in read_file("references/commands.md")
    assert has_wrapper or has_reference, f"Missing: {command}"
```

**Failure example**: wordpress-management mentioned `wp cache flush` but had no script or reference

---

## 2. Gotcha Surfacing (Prominent Display)

**Requirement**: All high-severity gotchas must appear:
- Within first 200 lines of SKILL.md
- In dedicated "⚠️ Common Pitfalls" or "Gotchas" section
- NOT buried in references/ or at end of file

**Why**: Prevents Claude from making documented mistakes

**Check:**
```python
skill_lines = read_file("SKILL.md").split('\n')
gotcha_section = find_section("Common Pitfall|⚠️|Gotcha", skill_lines)

assert gotcha_section < 200, f"Gotchas buried at line {gotcha_section}"

for gotcha in high_severity_gotchas:
    assert gotcha['warning'] in skill_lines[:gotcha_section + 50]
```

**Good example (crawl4ai-cli)**:
```markdown
## Workflow Requirements (line 402)

**⚠️ MANDATORY: Always follow this workflow for new sites:**
```

**Bad example (wordpress-management)**:
```markdown
## Tips & Troubleshooting (line 161)  # Buried too deep

**Always use wp-cli for operations:**
Deterministic, scriptable, no session timeouts.
```

---

## 3. --help Integration (CLI Tools Only)

**Requirement**: If skill involves CLI commands:
- Scripts include `get_help()` function that runs `{command} --help`
- Scripts accept `--help-command` flag
- Error messages reference help output

**Why**: Ensures Claude always has access to latest command documentation

**Check:**
```python
if has_cli_commands:
    for script in scripts_dir:
        content = read_file(f"scripts/{script}")
        assert "def get_help()" in content
        assert "--help" in content or "--help-command" in content
```

**Good template:**
```python
def get_help():
    """Run wp post --help to get latest documentation."""
    subprocess.run(["wp", "post", "--help"])

parser.add_argument("--help-command", action="store_true",
                   help="Show wp post --help output")
```

**Missing from**: wordpress-management scripts

---

## 4. Knowledge vs Action Separation

**Requirement**:
- **references/**: Static knowledge (tables, schemas, reference data, > 50 lines)
- **scripts/**: Executable actions (Python scripts with error handling)
- **SKILL.md**: Workflows and gotchas (< 500 lines total, actionable guidance)
- **assets/**: Templates and example outputs

**Why**: Implements progressive disclosure, keeps SKILL.md concise

**Check:**
```python
# SKILL.md should not have large reference tables
table_lines = count_table_lines(read_file("SKILL.md"))
assert table_lines < 50, f"SKILL.md has {table_lines} table lines (move to references/)"

# references/ should not have executable code
for ref_file in references_dir:
    content = read_file(f"references/{ref_file}")
    assert "#!/usr/bin" not in content, f"{ref_file} has executable code"
```

**Good example (crawl4ai-cli)**:
```
SKILL.md (470 lines) - workflows + gotchas
references/
  ├── config-reference.md (full config options)
  ├── css-schema-guide.md (selector patterns)
  └── troubleshooting.md (detailed solutions)
```

**Bad example (wordpress-management)**:
```
SKILL.md (226 lines) - includes shortcode reference inline
No references/ directory - missed progressive disclosure opportunity
```

---

## 5. Template Best Practices

**Requirement**: Generated templates must:
- Avoid warned patterns from gotchas
- Include error handling
- Reference helper scripts when appropriate
- Follow detected workflow patterns

**Why**: Templates teach Claude correct usage patterns

**Check:**
```python
for template in assets/templates:
    content = read_file(template)

    # Should avoid gotcha patterns
    for gotcha in gotchas:
        assert gotcha['bad_pattern'] not in content

    # Should use helper scripts, not direct commands
    if 'subprocess.run([' in content:
        assert 'scripts/' in content or '# Direct call justified' in content
```

**Good template:**
```bash
#!/bin/bash
# Use helper script for complex operations
python scripts/wp_post_update.py --post-id 123 --content-file new-content.txt
```

**Bad template:**
```bash
#!/bin/bash
# Direct command without error handling (gotcha: can corrupt content)
ssh user@host "wp post update 123 --post_content='...'"
```

---

## 6. Workflow Completeness

**Requirement**: Each detected workflow must include:
- All steps documented
- Prerequisites listed
- Expected outputs shown
- Error states handled

**Why**: Ensures Claude can execute end-to-end without getting stuck

**Check:**
```python
for workflow in detected_workflows:
    workflow_section = find_section(workflow['name'], skill_md)

    # Should have numbered steps
    assert re.findall(r'^\d+\.', workflow_section)

    # Should show expected outputs
    assert '# Returns:' in workflow_section or 'Output:' in workflow_section

    # Should handle errors
    assert 'Error:' in workflow_section or 'If fails' in workflow_section
```

**Good example (crawl4ai-cli)**:
```markdown
### Pattern: News Monitoring

1. Extract articles
2. Validate extraction  # ← Error handling step
3. Generate summary

# Returns: articles_{timestamp}.json
```

**Incomplete example**:
```markdown
### Upload Image

1. Split image
2. Transfer chunks
3. Import to WordPress
# ← Missing: What if import fails? What's the output format?
```

---

## 7. URL Source Attribution

**Requirement**: If docs were scraped from URLs (crawl4ai-cli):
- Source URLs listed in SKILL.md or README
- Scrape date/version documented
- Update instructions provided

**Why**: Enables skill maintenance when docs change

**Check:**
```python
if scraped_from_urls:
    readme = read_file("README.md") or read_file("SKILL.md")
    for url in source_urls:
        assert url in readme, f"Missing source attribution: {url}"
    assert "Last updated:" in readme or "Scraped on:" in readme
```

**Good attribution:**
```markdown
## Documentation Sources

- [Stripe API Reference](https://stripe.com/docs/api) - Scraped 2025-11-07
- [Stripe Best Practices](https://stripe.com/docs/best-practices) - Scraped 2025-11-07

To update: `crwl https://stripe.com/docs/api --bypass-cache -o markdown > references/api-reference.md`
```

---

## Summary Checklist

**Doc-driven skills must pass ALL standard validation PLUS:**

- [ ] **Command Coverage**: 100% of detected commands have wrappers or references
- [ ] **Gotcha Surfacing**: High-severity gotchas in first 200 lines
- [ ] **--help Integration**: CLI scripts include get_help() function
- [ ] **Knowledge/Action Separation**: SKILL.md < 500 lines, references/ used for bulk content
- [ ] **Template Best Practices**: Avoid gotcha patterns, use helper scripts
- [ ] **Workflow Completeness**: All steps, prerequisites, outputs, error handling
- [ ] **URL Attribution**: Source URLs and scrape dates documented (if applicable)

---

## Validation Script Usage

```bash
# Standard validation
python scripts/validate_skill.py --full-check my-skill/

# Doc-specific validation
python scripts/validate_doc_skill.py my-skill/

# Both
python scripts/validate_skill.py --full-check my-skill/ && \
python scripts/validate_doc_skill.py my-skill/
```

**validate_doc_skill.py output:**
```
Running documentation-driven skill validation...

✅ Command Coverage: 12/12 commands referenced
✅ Gotcha Surfacing: 5 gotchas surfaced at line 45
✅ --help Integration: 3/3 CLI scripts include get_help()
✅ Knowledge/Action Separation: SKILL.md 380 lines, references/ used
⚠️  Template Best Practices: 1 template uses direct subprocess (consider helper script)
✅ Workflow Completeness: 3/3 workflows complete
✅ URL Attribution: 2 source URLs documented

Overall: 6/7 checks passed (1 warning)
```

---

**End of Validation Criteria**
