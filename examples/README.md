# Skill Examples

This directory contains real-world examples of Claude Code skills demonstrating various patterns and use cases.

## Purpose

These examples serve as reference implementations showing:
- Different skill structures (simple vs complex)
- Resource organization (scripts/, references/, assets/)
- Frontmatter patterns and descriptions
- Common workflow patterns
- Various domains and use cases

## Compressed Format

To reduce repository size, these examples contain:
- **SKILL.md** - The complete skill file (always present)
- **README.md** - Describes any scripts, templates, or other resources that would be included
- **LICENSE.txt** - License information (where applicable)

The README.md in each example explains what scripts, templates, references, or assets the full skill would contain, providing the same educational value without storing the actual files.

## Examples by Category

### Document Processing
- **docx/** - Microsoft Word document manipulation (Python scripts, OOXML schemas)
- **pdf/** - PDF processing and form filling (Python scripts, validation tools)
- **pptx/** - PowerPoint creation and manipulation (Python scripts, OOXML schemas, HTML conversion)
- **xlsx/** - Excel spreadsheet operations (Python scripts, formula calculation)

### Creative Tools
- **algorithmic-art/** - Generate algorithmic art in HTML5 Canvas (JavaScript templates)
- **canvas-design/** - Rich canvas designs with custom fonts (81 font files)
- **slack-gif-creator/** - Create animated GIFs for Slack (Python core + 13 templates)
- **theme-factory/** - Generate color themes for presentations (10 theme presets)

### API & Integration
- **artifacts-builder/** - Build and package Claude Code artifacts (shell scripts)
- **webapp-testing/** - Automated web app testing (Python Playwright examples)

### Communication
- **brand-guidelines/** - Corporate brand guidance for AI-generated content
- **internal-comms/** - Company communication templates (4 example types)

### Template
- **template-skill/** - Minimal skill template for reference

## Usage Patterns

### Simple Skills (Instruction-Only)
- **brand-guidelines** - Pure instruction, no bundled resources
- **template-skill** - Minimal structure

### Skills with Scripts
- **pdf**, **docx**, **pptx**, **xlsx** - Executable Python scripts for automation
- **artifacts-builder**, **webapp-testing** - Shell and Python automation

### Skills with Templates
- **algorithmic-art** - JavaScript and HTML templates
- **slack-gif-creator** - Python animation templates
- **theme-factory** - Theme configuration files

### Skills with Assets
- **canvas-design** - 81 font files (.ttf) for canvas rendering
- **theme-factory** - PDF showcase and theme definitions

### Skills with Examples
- **internal-comms** - Example outputs for different communication types
- **webapp-testing** - Example test scripts for common scenarios

## Learning From Examples

When creating a new skill, find a similar example:

**Document processing?** → Look at `document-skills/pdf/`  
**API integration?** → Look at `artifacts-builder/`  
**Creative tool?** → Look at `algorithmic-art/` or `canvas-design/`  
**Testing/automation?** → Look at `webapp-testing/`  
**Communication?** → Look at `internal-comms/` or `brand-guidelines/`

## File Size Reduction

Original examples contained:
- 81 font files (canvas-design)
- 78 OOXML schema files (docx/pptx)
- 26 Python scripts across examples
- 13 Python templates (slack-gif-creator)
- 10 theme files (theme-factory)
- Multiple reference docs and examples

Compressed to:
- SKILL.md files only
- README.md describing removed content
- ~95% size reduction while preserving educational value

## Restoration

If you need the actual scripts, templates, or assets from these examples for your own skill development, you can:

1. Recreate based on the descriptions in README.md
2. Check commit history for the original files
3. Reference the SKILL.md which often contains inline examples

## Quality Standards

All examples follow:
- YAML frontmatter with name and description
- < 500 lines in SKILL.md
- Imperative voice instructions
- Clear resource references
- Progressive disclosure where needed

See [SKILL.md](../SKILL.md) for the complete skill creation process.

