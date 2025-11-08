#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import argparse
import sys
import os
import re
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)
    
    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"
    
    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"
    
    frontmatter = match.group(1)
    
    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter"
    
    # Extract name for validation
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"

    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"

    return True, "Skill is valid!"

def main():
    parser = argparse.ArgumentParser(
        description='Quick validation script for skills - minimal version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a skill directory
  python quick_validate.py ./my-skill/

  # Show this help message
  python quick_validate.py --help

This script performs basic validation:
  - Checks for SKILL.md file
  - Validates YAML frontmatter format
  - Checks required fields (name, description)
  - Validates naming conventions
  - Returns clear success/error messages
        """
    )

    parser.add_argument(
        'skill_directory',
        help='Path to skill directory to validate'
    )

    args = parser.parse_args()
    
    valid, message = validate_skill(args.skill_directory)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()