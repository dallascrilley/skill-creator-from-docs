#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--template <template-type>]

Templates:
    skill-skeleton     - Universal template with [TODO: ...] placeholders (all optional sections)
    minimal-skeleton     - Simplified template for straightforward skills (core sections only)

Examples:
    init_skill.py my-new-skill --path skills/public --template skill-skeleton
    init_skill.py my-new-skill --path skills/public --template minimal-skeleton --auto-fill
    init_skill.py my-new-skill --path skills/public --template skill-skeleton --auto-fill --create-research-log
"""

import argparse
import sys
import shutil
from pathlib import Path
import datetime as _datetime
import textwrap
import re
from typing import List, Tuple, Sequence


# Available template types
TEMPLATE_TYPES = [
    'skill-skeleton',  # Universal template with [TODO: ...] placeholders (all optional sections)
    'minimal-skeleton'  # Simplified template for straightforward skills (core sections only)
]

# Get the templates directory (relative to this script)
SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR.parent / 'templates'


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def slug_to_display_name(slug: str) -> str:
    """Convert skill slug to human-friendly display name."""
    return slug.replace('-', ' ').title()


def apply_replacements(path: Path, replacements: List[Tuple[str, str, str]]) -> List[str]:
    """
    Apply placeholder replacements to a file.

    Args:
        path: File path to modify
        replacements: List of (placeholder, replacement, label) tuples

    Returns:
        List of labels for placeholders that were not found
    """
    missing: List[str] = []

    if not path.exists():
        return [f"File not found: {path.name}"]

    content = path.read_text(encoding='utf-8')
    updated = content

    for placeholder, replacement, label in replacements:
        if placeholder in updated:
            updated = updated.replace(placeholder, replacement, 1)
        else:
            missing.append(label)

    if updated != content:
        path.write_text(updated, encoding='utf-8')

    return missing


def create_research_log(repo_root: Path, skill_name: str, display_name: str, today: str) -> Path:
    """
    Create research log file for skill development tracking.

    Args:
        repo_root: Root of skill-creator repository
        skill_name: Hyphenated skill slug
        display_name: Human-friendly skill name
        today: ISO date string (YYYY-MM-DD)

    Returns:
        Path to created research log file
    """
    log_dir = repo_root / 'planning' / 'research-logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"{skill_name}.md"

    if log_path.exists():
        print(f"⚠️  Research log already exists: {log_path}")
        return log_path

    content = textwrap.dedent(f'''\
        # {display_name} Research Log

        - Created: {today}
        - Skill slug: {skill_name}

        ## Summary

        Capture the user problem this skill solves and the value proposition.

        ## Key Sources

        - Link to official docs, blog posts, and working examples.

        ## Experiments

        Document any test projects, command transcripts, or reproduction steps.

        ## Follow-Ups

        - Confirm latest package versions
        - Note open questions or risks to resolve before shipping
        ''')

    log_path.write_text(content, encoding='utf-8')
    return log_path


def count_todos(root: Path) -> int:
    """
    Count remaining [TODO:] markers in skill directory.

    Args:
        root: Skill directory path

    Returns:
        Total count of [TODO:] markers found
    """
    total = 0
    for candidate in root.rglob('*'):
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            continue
        total += text.count('[TODO:')
    return total


def validate_skill_name(name: str) -> None:
    """Validate skill name format."""
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        print("❌ Error: skill_name must be lowercase, alphanumeric, and hyphen-separated")
        print("   Example: react-hook-form-zod")
        sys.exit(1)


def init_from_template(
    skill_name: str,
    path: str,
    template_type: str,
    repo_root: Path,
    auto_fill: bool = False,
    display_name: str | None = None,
    status: str = 'Beta',
    quick_start_minutes: int = 5,
    create_research_log: bool = False
) -> Path | None:
    """
    Initialize a new skill from a specific template.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        template_type: Type of template to use
        repo_root: Root of skill-creator repository
        auto_fill: Enable automatic placeholder replacement
        display_name: Human-friendly skill name (default: title-cased slug)
        status: Status label for SKILL.md and README.md (default: Beta)
        quick_start_minutes: Duration in minutes for Quick Start section (default: 5)
        create_research_log: Create research log file

    Returns:
        Path to created skill directory, or None if error
    """
    # Validate skill name
    validate_skill_name(skill_name)

    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Check if template exists
    template_dir = TEMPLATES_DIR / template_type
    if not template_dir.exists():
        print(f"❌ Error: Template not found: {template_dir}")
        print(f"   Available templates: {', '.join(TEMPLATE_TYPES)}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Copy template files
    try:
        # Copy SKILL.md.template as SKILL.md, or SKILL.md directly
        template_skill_md = template_dir / 'SKILL.md.template'
        if not template_skill_md.exists():
            template_skill_md = template_dir / 'SKILL.md'
        if template_skill_md.exists():
            shutil.copy2(template_skill_md, skill_dir / 'SKILL.md')
            print("✅ Created SKILL.md from template")
        else:
            print(f"❌ Error: Template SKILL.md or SKILL.md.template not found")
            shutil.rmtree(skill_dir)
            return None

        # Copy scripts/ directory if it exists
        template_scripts = template_dir / 'scripts'
        if template_scripts.exists():
            shutil.copytree(template_scripts, skill_dir / 'scripts')
            print(f"✅ Copied scripts/ directory")

        # Copy references/ directory if it exists
        template_references = template_dir / 'references'
        if template_references.exists():
            shutil.copytree(template_references, skill_dir / 'references')
            print(f"✅ Copied references/ directory")
        else:
            # Create empty references directory
            (skill_dir / 'references').mkdir(exist_ok=True)
            print(f"✅ Created empty references/ directory")

        # Copy assets/ directory if it exists
        template_assets = template_dir / 'assets'
        if template_assets.exists():
            shutil.copytree(template_assets, skill_dir / 'assets')
            print(f"✅ Copied assets/ directory")

        # Copy README.md if it exists
        template_readme = template_dir / 'README.md'
        if template_readme.exists():
            shutil.copy2(template_readme, skill_dir / 'README.md')
            print("✅ Created README.md from template")

    except Exception as e:
        print(f"❌ Error copying template files: {e}")
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        return None

    # Apply metadata replacements if requested
    if auto_fill:
        display = (display_name.strip() if display_name else slug_to_display_name(skill_name))
        today = _datetime.date.today().isoformat()

        # Build replacement lists
        skill_replacements: List[Tuple[str, str, str]] = [
            ('name: [TODO: lowercase-hyphen-case-name]', f'name: {skill_name}', 'SKILL.md frontmatter name'),
            ('# [TODO: Skill Display Name]', f'# {display}', 'SKILL.md title'),
            ('**Status**: [TODO: Production Ready / Beta / Experimental]', f'**Status**: {status}', 'SKILL.md status'),
            ('**Last Updated**: [TODO: YYYY-MM-DD]', f'**Last Updated**: {today}', 'SKILL.md last updated'),
            ('## Quick Start ([TODO: X] Minutes)', f'## Quick Start ({quick_start_minutes} Minutes)', 'SKILL.md quick start'),
        ]

        readme_replacements: List[Tuple[str, str, str]] = [
            ('# [TODO: Skill Name]', f'# {display}', 'README.md title'),
            ('**Status**: [TODO: Production Ready / Beta / Experimental] ✅', f'**Status**: {status} ✅', 'README.md status'),
            ('**Last Updated**: [TODO: YYYY-MM-DD]', f'**Last Updated**: {today}', 'README.md last updated'),
        ]

        # Apply replacements
        missing_skill = apply_replacements(skill_dir / 'SKILL.md', skill_replacements)
        missing_readme = apply_replacements(skill_dir / 'README.md', readme_replacements)

        # Report results
        all_missing = missing_skill + missing_readme
        if all_missing:
            print(f"⚠️  Some placeholders not found: {', '.join(all_missing)}")
        else:
            print('✅ Applied metadata replacements to SKILL.md and README.md')

        # Count remaining TODOs
        todo_count = count_todos(skill_dir)
        print(f'📝 Remaining [TODO:] markers: {todo_count}')

    # Create research log if requested
    if create_research_log:
        display = (display_name.strip() if display_name else slug_to_display_name(skill_name))
        today = _datetime.date.today().isoformat()
        log_path = create_research_log(repo_root, skill_name, display, today)
        print(f'✅ Created research log: {log_path}')

    # Print next steps
    print(f"\n✅ Skill '{skill_name}' initialized from '{template_type}' template")
    print(f"   Location: {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to replace all [TODO: ...] placeholders")
    print("2. Delete sections in SKILL.md that don't apply to your skill")
    print("3. See the template README.md for customization guidance:")
    print(f"   {template_dir / 'README.md'}")
    print("4. Customize scripts and reference files as needed")
    print("5. Run validator: python scripts/validate_skill.py --full-check .")

    return skill_dir


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created references/api_reference.md")

        # Create assets/ directory with example asset placeholder
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ Created assets/example_asset.txt")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print("3. Run the validator when ready to check the skill structure")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new skill from template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic initialization (universal template)
  python init_skill.py my-skill --path ./skills/ --template skill-skeleton

  # Minimal template for simple skills
  python init_skill.py my-skill --path ./skills/ --template minimal-skeleton --auto-fill

  # Universal template with auto-fill
  python init_skill.py my-skill --path ./skills/ --template skill-skeleton --auto-fill

  # Customize metadata
  python init_skill.py my-skill --path ./skills/ --template skill-skeleton \\
    --auto-fill --display-name "My Custom Skill" --status "Production Ready" \\
    --quick-start-minutes 10

  # Create research log for planning
  python init_skill.py my-skill --path ./skills/ --template skill-skeleton --create-research-log

  # Full workflow: auto-fill + research log
  python init_skill.py my-skill --path ./skills/ --template skill-skeleton \\
    --auto-fill --create-research-log

The script will:
  - Create skill directory with standardized structure
  - Copy template files with working examples
  - Optionally replace [TODO: ...] placeholders (--auto-fill)
  - Optionally create research log (--create-research-log)
  - Provide coherent starting point for customization

Skill name requirements:
  - Hyphen-case identifier (e.g., 'data-analyzer')
  - Lowercase letters, digits, and hyphens only
  - Must match directory name exactly
        """
    )

    parser.add_argument(
        'skill_name',
        help='Name for the new skill (lowercase with hyphens)'
    )

    parser.add_argument(
        '--path',
        required=True,
        help='Directory path where to create the skill'
    )

    parser.add_argument(
        '--template',
        default='skill-skeleton',
        choices=TEMPLATE_TYPES,
        help='Template to use (default: skill-skeleton)'
    )

    parser.add_argument(
        '--auto-fill',
        action='store_true',
        help='Automatically replace [TODO: ...] placeholders with provided values'
    )

    parser.add_argument(
        '--display-name',
        dest='display_name',
        help='Human-friendly skill name (default: title-cased slug)'
    )

    parser.add_argument(
        '--status',
        default='Beta',
        help='Status label for SKILL.md and README.md (default: Beta)'
    )

    parser.add_argument(
        '--quick-start-minutes',
        type=int,
        default=5,
        help='Duration in minutes for Quick Start section (default: 5)'
    )

    parser.add_argument(
        '--create-research-log',
        action='store_true',
        help='Create planning/research-logs/<skill-name>.md with starter template'
    )

    parser.add_argument(
        '--skip-metadata',
        action='store_true',
        help='Skip metadata replacement (opposite of --auto-fill, for backward compatibility)'
    )

    args = parser.parse_args()

    print(f"🚀 Initializing skill: {args.skill_name}")
    print(f"   Location: {args.path}")
    print(f"   Template: {args.template}")
    print()

    # Calculate repo root once
    repo_root = Path(__file__).resolve().parent.parent

    # Determine if auto_fill should be enabled
    auto_fill = args.auto_fill and not args.skip_metadata

    # Initialize skill from template with new parameters
    result = init_from_template(
        args.skill_name,
        args.path,
        args.template,
        repo_root,
        auto_fill=auto_fill,
        display_name=args.display_name,
        status=args.status,
        quick_start_minutes=args.quick_start_minutes,
        create_research_log=args.create_research_log
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
