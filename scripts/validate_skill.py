#!/usr/bin/env python3
"""
Skill validation script following Anthropic best practices.

Usage:
    python validate_skill.py --check-init <skill-dir>       # Check initialization
    python validate_skill.py --check-structure <skill-dir>  # Check structure
    python validate_skill.py --check-content <skill-dir>    # Check content quality
    python validate_skill.py --full-check <skill-dir>       # Complete validation

Checks:
    - Frontmatter format (name ≤ 64 chars, description ≤ 1024 chars)
    - Naming conventions (gerund form recommended)
    - Description quality (specific, includes triggers)
    - Progressive disclosure (SKILL.md < 500 lines recommended)
    - Writing style (imperative/infinitive form)
    - File organization (scripts/, references/, assets/)
    - Resource references (correct paths, files exist)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any


class ValidationResult:
    """Represents the result of a validation check."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(f"❌ {message}")

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(f"⚠️  {message}")

    def add_pass(self, message: str):
        """Add a passed check message."""
        self.passed.append(f"✅ {message}")

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    def print_results(self, show_passed: bool = False):
        """Print all results."""
        if self.errors:
            print("\n🔴 ERRORS:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n🟡 WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if show_passed and self.passed:
            print("\n🟢 PASSED:")
            for passed in self.passed:
                print(f"  {passed}")


class SkillValidator:
    """Validates skills following Anthropic best practices."""

    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.skill_md_path = skill_dir / "SKILL.md"
        self.result = ValidationResult()

    def check_init(self) -> ValidationResult:
        """Check basic initialization."""
        print("🔍 Checking initialization...")

        # Check skill directory exists
        if not self.skill_dir.exists():
            self.result.add_error(f"Skill directory does not exist: {self.skill_dir}")
            return self.result
        else:
            self.result.add_pass(f"Skill directory exists: {self.skill_dir}")

        # Check SKILL.md exists
        if not self.skill_md_path.exists():
            self.result.add_error(f"SKILL.md not found in {self.skill_dir}")
            return self.result
        else:
            self.result.add_pass("SKILL.md exists")

        # Basic structure
        self._check_structure_basic()

        return self.result

    def check_structure(self) -> ValidationResult:
        """Check directory and file structure."""
        print("🔍 Checking structure...")

        # Run init check first
        self.check_init()
        if self.result.has_errors():
            return self.result

        # Check frontmatter
        self._check_frontmatter()

        # Check directory organization
        self._check_directories()

        # Check file references
        self._check_file_references()

        return self.result

    def check_content(self) -> ValidationResult:
        """Check content quality."""
        print("🔍 Checking content quality...")

        # Run structure check first
        self.check_structure()
        if self.result.has_errors():
            return self.result

        # Check description quality
        self._check_description_quality()

        # Check naming conventions
        self._check_naming()

        # Check writing style
        self._check_writing_style()

        # Check progressive disclosure
        self._check_progressive_disclosure()

        # Check for examples
        self._check_examples()

        # Phase 2 enhancements
        self._check_conciseness()
        self._check_degrees_of_freedom()
        self._check_script_error_handling()
        self._check_evaluation_references()

        return self.result

    def full_check(self) -> ValidationResult:
        """Run complete validation."""
        print("🔍 Running full validation...")
        print("=" * 60)

        self.check_content()  # This cascades through all checks

        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        summary_lines = []
        if self.result.errors:
            summary_lines.append(f"❌ {len(self.result.errors)} error(s)")
        if self.result.warnings:
            summary_lines.append(f"⚠️  {len(self.result.warnings)} warning(s)")
        if self.result.passed:
            summary_lines.append(f"✅ {len(self.result.passed)} check(s) passed")

        print(", ".join(summary_lines))

        return self.result

    def _read_skill_md(self) -> Tuple[Dict[str, str], str]:
        """Read and parse SKILL.md into frontmatter and body."""
        content = self.skill_md_path.read_text()

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)

        if not frontmatter_match:
            return {}, content

        frontmatter_text = frontmatter_match.group(1)
        body = frontmatter_match.group(2)

        # Parse frontmatter
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter, body

    def _check_structure_basic(self):
        """Check basic file structure."""
        # Check for common directories
        scripts_dir = self.skill_dir / "scripts"
        references_dir = self.skill_dir / "references"
        assets_dir = self.skill_dir / "assets"

        # These are optional, just note if they exist
        if scripts_dir.exists():
            self.result.add_pass("scripts/ directory found")
        if references_dir.exists():
            self.result.add_pass("references/ directory found")
        if assets_dir.exists():
            self.result.add_pass("assets/ directory found")

    def _check_frontmatter(self):
        """Check frontmatter format and constraints."""
        frontmatter, _ = self._read_skill_md()

        if not frontmatter:
            self.result.add_error("SKILL.md missing YAML frontmatter (should start with ---)")
            return
        else:
            self.result.add_pass("YAML frontmatter found")

        # Check required fields
        if 'name' not in frontmatter:
            self.result.add_error("Frontmatter missing required field: name")
        else:
            name = frontmatter['name']

            # Check name length
            if len(name) > 64:
                self.result.add_error(f"Name exceeds 64 characters: {len(name)} chars")
            else:
                self.result.add_pass(f"Name length OK: {len(name)}/64 chars")

            # Check name format (lowercase with hyphens)
            if not re.match(r'^[a-z0-9-]+$', name):
                self.result.add_warning(
                    f"Name '{name}' should use lowercase alphanumeric with hyphens only"
                )
            else:
                self.result.add_pass("Name format is valid (lowercase with hyphens)")

        if 'description' not in frontmatter:
            self.result.add_error("Frontmatter missing required field: description")
        else:
            description = frontmatter['description']

            # Check description length
            if len(description) > 1024:
                self.result.add_error(f"Description exceeds 1024 characters: {len(description)} chars")
            elif len(description) < 50:
                self.result.add_warning(
                    f"Description is very short: {len(description)} chars (recommend 100-300)"
                )
            else:
                self.result.add_pass(f"Description length OK: {len(description)}/1024 chars")

    def _check_directories(self):
        """Check directory organization."""
        # Check for common directories
        scripts_dir = self.skill_dir / "scripts"
        references_dir = self.skill_dir / "references"
        assets_dir = self.skill_dir / "assets"

        # Check if scripts/ has files
        if scripts_dir.exists():
            script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
            if script_files:
                self.result.add_pass(f"Found {len(script_files)} script(s) in scripts/")
            else:
                self.result.add_warning("scripts/ directory exists but is empty")

        # Check if references/ has files
        if references_dir.exists():
            ref_files = list(references_dir.glob("*.md"))
            if ref_files:
                self.result.add_pass(f"Found {len(ref_files)} reference file(s) in references/")
            else:
                self.result.add_warning("references/ directory exists but is empty")

        # Check if assets/ has files
        if assets_dir.exists():
            asset_files = list(assets_dir.rglob("*"))
            asset_files = [f for f in asset_files if f.is_file()]
            if asset_files:
                self.result.add_pass(f"Found {len(asset_files)} asset(s) in assets/")
            else:
                self.result.add_warning("assets/ directory exists but is empty")

    def _check_file_references(self):
        """Check that referenced files exist."""
        _, body = self._read_skill_md()

        # Find markdown links to files
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, body)

        for link_text, link_path in matches:
            # Skip external URLs
            if link_path.startswith('http://') or link_path.startswith('https://'):
                continue

            # Check if file exists
            full_path = self.skill_dir / link_path
            if not full_path.exists():
                self.result.add_error(
                    f"Referenced file does not exist: {link_path}"
                )
            else:
                self.result.add_pass(f"File reference valid: {link_path}")

    def _check_description_quality(self):
        """Check description quality and specificity."""
        frontmatter, _ = self._read_skill_md()

        if 'description' not in frontmatter:
            return  # Already caught in frontmatter check

        description = frontmatter['description']

        # Check for third-person voice
        second_person_patterns = [r'\byou\b', r'\byour\b', r'\byou\'re\b']
        for pattern in second_person_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                self.result.add_warning(
                    "Description should use third-person voice, not 'you/your'"
                )
                break
        else:
            self.result.add_pass("Description uses third-person voice")

        # Check for trigger terms
        if re.search(r'\buse when\b|\buse this when\b|\bshould be used when\b', description, re.IGNORECASE):
            self.result.add_pass("Description includes 'when to use' guidance")
        else:
            self.result.add_warning(
                "Description should include when to use the skill (trigger terms)"
            )

        # Check for specificity
        vague_terms = ['helps with', 'does stuff', 'processes data', 'works with']
        for term in vague_terms:
            if term.lower() in description.lower():
                self.result.add_warning(
                    f"Description contains vague term '{term}' - be more specific"
                )

    def _check_naming(self):
        """Check naming conventions."""
        frontmatter, _ = self._read_skill_md()

        if 'name' not in frontmatter:
            return  # Already caught in frontmatter check

        name = frontmatter['name']

        # Check for gerund form (ending in -ing)
        # Convert kebab-case to words
        words = name.split('-')

        # Check if any word ends in -ing (gerund form)
        has_gerund = any(word.endswith('ing') for word in words)

        if has_gerund:
            self.result.add_pass("Name uses gerund form (recommended)")
        else:
            self.result.add_warning(
                f"Consider using gerund form for name: e.g., 'processing-{words[0]}' instead of '{name}'"
            )

    def _check_writing_style(self):
        """Check for imperative/infinitive form in body."""
        _, body = self._read_skill_md()

        # Check for second-person instructions (should avoid)
        second_person_count = len(re.findall(r'\byou should\b|\byou can\b|\byou must\b|\byou need\b', body, re.IGNORECASE))

        if second_person_count > 5:
            self.result.add_warning(
                f"Found {second_person_count} instances of 'you should/can/must/need' - prefer imperative form"
            )
        elif second_person_count > 0:
            self.result.add_warning(
                f"Found {second_person_count} instances of second-person instructions - prefer imperative form"
            )
        else:
            self.result.add_pass("Writing style uses imperative form (no 'you should/can/must')")

    def _check_progressive_disclosure(self):
        """Check SKILL.md length and progressive disclosure."""
        _, body = self._read_skill_md()

        # Count lines in body
        lines = body.split('\n')
        line_count = len(lines)

        if line_count > 500:
            self.result.add_warning(
                f"SKILL.md body has {line_count} lines (recommend < 500). Consider moving content to references/"
            )
        else:
            self.result.add_pass(f"SKILL.md body length OK: {line_count} lines")

        # Check if references/ is used when body is large
        if line_count > 500:
            references_dir = self.skill_dir / "references"
            if not references_dir.exists() or not list(references_dir.glob("*.md")):
                self.result.add_warning(
                    "Large SKILL.md but no references/ directory - consider progressive disclosure"
                )

    def _check_examples(self):
        """Check if skill includes examples."""
        _, body = self._read_skill_md()

        # Look for example sections or code blocks
        has_examples = bool(
            re.search(r'## Example|### Example|```', body, re.IGNORECASE)
        )

        if has_examples:
            self.result.add_pass("Skill includes examples or code blocks")
        else:
            self.result.add_warning(
                "No examples found - consider adding usage examples for complex operations"
            )

    def _check_conciseness(self):
        """Check for common verbosity patterns (Phase 2 enhancement)."""
        _, body = self._read_skill_md()

        # Check for over-explanation of common concepts
        verbose_patterns = [
            (r'PDF \(Portable Document Format\)', 'Avoid defining PDF - Claude knows this'),
            (r'JSON \(JavaScript Object Notation\)', 'Avoid defining JSON - Claude knows this'),
            (r'API \(Application Programming Interface\)', 'Avoid defining API - Claude knows this'),
            (r'CSV \(Comma[- ]Separated Values?\)', 'Avoid defining CSV - Claude knows this'),
            (r'There are many ways to', 'Cut explanation of alternatives - be direct'),
            (r'You can also', 'Use imperative form instead'),
            (r'It is important to note that', 'Cut unnecessary preamble'),
            (r'basically', 'Remove hedge word "basically"'),
            (r'essentially', 'Remove hedge word "essentially"'),
        ]

        found_issues = []
        for pattern, message in verbose_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                found_issues.append(message)

        if found_issues:
            for issue in found_issues[:3]:  # Show first 3
                self.result.add_warning(f"Verbosity: {issue}")
            if len(found_issues) > 3:
                self.result.add_warning(f"Verbosity: ... and {len(found_issues) - 3} more issues")
        else:
            self.result.add_pass("No obvious verbosity patterns detected")

    def _check_degrees_of_freedom(self):
        """Check for appropriate specificity markers (Phase 2 enhancement)."""
        _, body = self._read_skill_md()

        issues = []

        # Look for mixed messages (MUST + flexibility language)
        has_must = bool(re.search(r'\b(MUST|must not|do not modify|in exact order)\b', body, re.IGNORECASE))
        has_flexible = bool(re.search(r'\b(you can also|feel free|optional|consider)\b', body, re.IGNORECASE))

        if has_must and has_flexible:
            issues.append("Mixed freedom signals: Contains both strict (MUST) and flexible (can also) language")

        # Check for low-freedom tasks without warnings
        strict_patterns = [
            r'in exact order',
            r'must pass',
            r'do not modify',
            r'MUST complete',
            r'DO NOT proceed'
        ]
        has_strict = any(re.search(p, body, re.IGNORECASE) for p in strict_patterns)
        has_warnings = bool(re.search(r'[⚠️❗]', body))

        if has_strict and not has_warnings:
            issues.append("Low-freedom instructions without ⚠️ warnings")

        if issues:
            for issue in issues:
                self.result.add_warning(f"Degrees of freedom: {issue}")
        else:
            self.result.add_pass("Degrees of freedom markers appear appropriate")

    def _check_script_error_handling(self):
        """Check scripts implement 'solve don't punt' pattern (Phase 2 enhancement)."""
        scripts_dir = self.skill_dir / "scripts"

        if not scripts_dir.exists():
            return  # No scripts to check

        python_scripts = list(scripts_dir.glob("*.py"))
        if not python_scripts:
            return

        issues = []

        for script in python_scripts:
            try:
                content = script.read_text()

                # Check for file operations without try/except
                has_file_ops = bool(re.search(r'\bopen\s*\(', content))
                has_try_except = bool(re.search(r'\btry\s*:', content))

                if has_file_ops and not has_try_except:
                    issues.append(f"{script.name}: File operations without try/except")

                # Check for bare except clauses
                if re.search(r'except\s*:', content):
                    issues.append(f"{script.name}: Bare except clause - catch specific exceptions")

                # Check for error messages
                has_exceptions = 'except' in content
                has_error_messages = bool(re.search(r'print\s*\(.*[❌💡]', content))

                if has_exceptions and not has_error_messages:
                    issues.append(f"{script.name}: Exceptions without helpful error messages")

            except Exception as e:
                self.result.add_warning(f"Could not read {script.name}: {e}")

        if issues:
            for issue in issues[:3]:  # Show first 3
                self.result.add_warning(f"Script quality: {issue}")
            if len(issues) > 3:
                self.result.add_warning(f"Script quality: ... and {len(issues) - 3} more issues")
        else:
            self.result.add_pass("Scripts follow 'solve don't punt' pattern")

    def _check_evaluation_references(self):
        """Check if skill references test scenarios/evaluations (Phase 2 enhancement)."""
        _, body = self._read_skill_md()

        eval_indicators = [
            'test scenario', 'evaluation', 'example usage',
            'test with', 'test case', 'baseline'
        ]

        has_evals = any(ind in body.lower() for ind in eval_indicators)

        if has_evals:
            self.result.add_pass("Skill references test scenarios or evaluations")
        else:
            self.result.add_warning(
                "No test scenario references found - consider documenting test cases (EDD)"
            )


def main():
    parser = argparse.ArgumentParser(
        description='Validate Claude Code skills following Anthropic best practices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check basic initialization
  python validate_skill.py --check-init ./my-skill/

  # Check directory structure
  python validate_skill.py --check-structure ./my-skill/

  # Check content quality
  python validate_skill.py --check-content ./my-skill/

  # Run complete validation
  python validate_skill.py --full-check ./my-skill/

  # Show this help message
  python validate_skill.py --help

Validation Checks:
  - Frontmatter format (name ≤ 64 chars, description ≤ 1024 chars)
  - Naming conventions (gerund form recommended)
  - Description quality (specific, includes triggers)
  - Progressive disclosure (SKILL.md < 500 lines recommended)
  - Writing style (imperative/infinitive form)
  - File organization (scripts/, references/, assets/)
  - Resource references (correct paths, files exist)
        """
    )
    parser.add_argument(
        '--check-init',
        metavar='SKILL_DIR',
        help='Check basic initialization (SKILL.md, frontmatter)'
    )
    parser.add_argument(
        '--check-structure',
        metavar='SKILL_DIR',
        help='Check directory and file structure'
    )
    parser.add_argument(
        '--check-content',
        metavar='SKILL_DIR',
        help='Check content quality and best practices'
    )
    parser.add_argument(
        '--full-check',
        metavar='SKILL_DIR',
        help='Run complete validation (all checks)'
    )

    args = parser.parse_args()

    # Determine which check to run
    if args.check_init:
        skill_dir = Path(args.check_init)
        validator = SkillValidator(skill_dir)
        result = validator.check_init()
    elif args.check_structure:
        skill_dir = Path(args.check_structure)
        validator = SkillValidator(skill_dir)
        result = validator.check_structure()
    elif args.check_content:
        skill_dir = Path(args.check_content)
        validator = SkillValidator(skill_dir)
        result = validator.check_content()
    elif args.full_check:
        skill_dir = Path(args.full_check)
        validator = SkillValidator(skill_dir)
        result = validator.full_check()
    else:
        parser.print_help()
        sys.exit(1)

    # Print results
    result.print_results(show_passed=True)

    # Exit with appropriate code
    if result.has_errors():
        print("\n❌ Validation failed with errors")
        sys.exit(1)
    elif result.warnings:
        print("\n⚠️  Validation passed with warnings")
        sys.exit(0)
    else:
        print("\n✅ Validation passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
