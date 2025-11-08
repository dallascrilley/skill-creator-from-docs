#!/usr/bin/env python3
"""
Unit tests for skill_md_generator.py
"""

import json
from pathlib import Path

import pytest

from skill_md_generator import (
    SkillMDGenerator,
    SkillMD
)


class TestSkillMD:
    """Tests for SkillMD dataclass."""

    def test_skill_md_creation(self):
        """Test creating SkillMD."""
        skill_md = SkillMD(
            frontmatter="---\nname: test\n---",
            overview="## Overview\nTest tool overview",
            quick_start="## Quick Start\nQuick start guide",
            workflows="## Workflows\nWorkflow details",
            templates_ref="## Templates\nTemplate info",
            guardrails_ref="## Guardrails\nGuardrail info",
            troubleshooting_ref="## Troubleshooting\nTroubleshooting guide",
            see_also="## See Also\nRelated resources"
        )

        assert "name: test" in skill_md.frontmatter
        assert "Overview" in skill_md.overview
        assert "Quick Start" in skill_md.quick_start
        assert "See Also" in skill_md.see_also

    def test_skill_md_compile(self):
        """Test compiling SkillMD to full markdown."""
        skill_md = SkillMD(
            frontmatter="---\nname: test\n---",
            overview="## Overview\nContent",
            quick_start="## Quick Start\nContent",
            workflows="## Workflows\nContent",
            templates_ref="## Templates\nContent",
            guardrails_ref="## Guardrails\nContent",
            troubleshooting_ref="## Troubleshooting\nContent",
            see_also="## See Also\nContent"
        )

        compiled = skill_md.compile()

        assert "---\nname: test\n---" in compiled
        assert "## Overview" in compiled
        assert "## Quick Start" in compiled
        assert "## Workflows" in compiled
        assert "## Templates" in compiled
        assert "## See Also" in compiled


class TestSkillMDGenerator:
    """Tests for SkillMDGenerator class."""

    def test_generator_initialization(self):
        """Test creating SkillMDGenerator instance."""
        generator = SkillMDGenerator(verbose=False)
        assert generator is not None
        assert generator.verbose is False

    def test_generate_frontmatter(self):
        """Test generating skill frontmatter."""
        generator = SkillMDGenerator(verbose=False)

        workflows = [{'name': 'Basic Workflow', 'frequency': 'common'}]
        pitfalls = [{'description': 'Error A', 'severity': 'high'}]

        frontmatter = generator.generate_frontmatter(
            'test-tool',
            'cli',
            workflows,
            pitfalls
        )

        assert '---' in frontmatter
        assert 'name:' in frontmatter
        assert 'test-tool' in frontmatter or 'cli' in frontmatter.lower()
        assert 'description:' in frontmatter

    def test_generate_overview(self):
        """Test generating overview section."""
        generator = SkillMDGenerator(verbose=False)

        workflows = [{'name': 'Basic Workflow', 'frequency': 'common'}]

        overview = generator.generate_overview('test-tool', 'cli', workflows)

        # Overview generates title and introduction, not a section header
        assert 'test-tool' in overview
        assert '##' in overview  # Has some section headers
        assert 'When to Use' in overview or 'What This Skill Provides' in overview

    def test_generate_quick_start(self):
        """Test generating quick start section."""
        generator = SkillMDGenerator(verbose=False)

        examples = [
            {
                'title': 'Basic Example',
                'language': 'bash',
                'code': 'test-tool run --input file.txt',
                'context': 'Basic usage'
            }
        ]

        templates = None  # No templates for this test

        quick_start = generator.generate_quick_start('test-tool', examples, templates)

        assert '## Quick Start' in quick_start
        assert 'test-tool' in quick_start
        assert '```bash' in quick_start or '```' in quick_start

    def test_generate_workflows_section(self):
        """Test generating workflows section."""
        generator = SkillMDGenerator(verbose=False)

        workflows = [
            {
                'name': 'Basic Processing',
                'description': 'Process a file',
                'steps': ['Step 1', 'Step 2'],
                'frequency': 'common'
            },
            {
                'name': 'Batch Processing',
                'description': 'Process multiple files',
                'steps': ['Step 1', 'Step 2', 'Step 3'],
                'frequency': 'occasional'
            }
        ]

        section = generator.generate_workflows_section(workflows)

        assert '## Common Workflows' in section or '##' in section
        assert 'Basic Processing' in section
        assert 'Batch Processing' in section
        assert 'Step 1' in section

    def test_generate_templates_reference(self):
        """Test generating templates reference section."""
        generator = SkillMDGenerator(verbose=False)

        templates_metadata = {
            'templates': [
                {
                    'name': 'cli_basic',
                    'type': 'basic',
                    'language': 'bash',
                    'placeholders': ['INPUT_FILE', 'OUTPUT_FILE']
                },
                {
                    'name': 'cli_advanced',
                    'type': 'advanced',
                    'language': 'bash',
                    'placeholders': ['CONFIG']
                }
            ],
            'total_templates': 2
        }

        section = generator.generate_templates_reference(templates_metadata)

        assert '## Available Templates' in section or '##' in section
        assert 'cli_basic' in section
        assert 'cli_advanced' in section
        assert 'basic' in section or 'advanced' in section

    def test_generate_guardrails_reference(self):
        """Test generating guardrails reference section."""
        generator = SkillMDGenerator(verbose=False)

        pitfalls = [
            {'description': 'Error A', 'severity': 'high'},
            {'description': 'Error B', 'severity': 'medium'}
        ]

        guardrails_metadata = {
            'layers': {
                'inline_warnings': 5,
                'validation_script': 'scripts/validate_prereqs.sh',
                'checklist': 'checklists/pre-flight.md',
                'setup_script': 'scripts/setup.sh'
            }
        }

        section = generator.generate_guardrails_reference(pitfalls, guardrails_metadata)

        assert '## Guardrails' in section
        assert 'validate_prereqs.sh' in section or 'validation' in section.lower()
        assert 'checklist' in section.lower() or 'pre-flight' in section.lower()

    def test_generate_troubleshooting_reference(self):
        """Test generating troubleshooting reference section."""
        generator = SkillMDGenerator(verbose=False)

        assets_metadata = {
            'assets': {
                'troubleshooting': 'docs/troubleshooting.md',
                'quick_reference': 'docs/quick-reference.md'
            }
        }

        section = generator.generate_troubleshooting_reference(assets_metadata)

        assert '## Troubleshooting' in section or '## Resources' in section
        assert 'troubleshooting.md' in section or 'troubleshooting' in section.lower()

    def test_generate_skill_md(self, sample_analysis):
        """Test complete SKILL.md generation."""
        generator = SkillMDGenerator(verbose=False)

        # Minimal metadata for complete generation
        templates_meta = {
            'templates': [{'name': 'basic', 'type': 'basic', 'language': 'bash'}],
            'total_templates': 1
        }
        guardrails_meta = {
            'layers': {
                'inline_warnings': 3,
                'validation_script': 'validate.sh',
                'checklist': 'checklist.md',
                'setup_script': 'setup.sh'
            }
        }
        assets_meta = {
            'assets': {
                'troubleshooting': 'troubleshooting.md'
            }
        }

        skill_md = generator.generate_skill_md(
            sample_analysis,
            templates_meta,
            guardrails_meta,
            assets_meta
        )

        assert isinstance(skill_md, SkillMD)
        assert skill_md.frontmatter
        assert skill_md.overview
        assert skill_md.quick_start
        assert skill_md.workflows
        assert skill_md.templates_ref
        assert skill_md.guardrails_ref

    def test_generate_skill_md_compiles(self, sample_analysis):
        """Test generated SKILL.md compiles to valid markdown."""
        generator = SkillMDGenerator(verbose=False)

        skill_md = generator.generate_skill_md(sample_analysis, None, None, None)
        compiled = skill_md.compile()

        assert isinstance(compiled, str)
        assert len(compiled) > 0
        assert '---' in compiled  # Has frontmatter
        assert '##' in compiled  # Has sections

    def test_save_skill_md(self, temp_output_dir, sample_analysis):
        """Test saving SKILL.md to disk."""
        generator = SkillMDGenerator(verbose=False)

        skill_md = generator.generate_skill_md(sample_analysis, None, None, None)
        skill_file = temp_output_dir / 'SKILL.md'
        generator.save_skill_md(skill_md, str(skill_file))

        # Check file created
        assert skill_file.exists()

        # Check content
        content = skill_file.read_text()
        assert '---' in content
        assert 'name:' in content

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        generator = SkillMDGenerator(verbose=True)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        generator = SkillMDGenerator(verbose=False)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestSkillMDGeneratorIntegration:
    """Integration tests for SKILL.md generator."""

    def test_full_generation_workflow(self, sample_analysis, temp_output_dir):
        """Test complete generation workflow from analysis to saved SKILL.md."""
        generator = SkillMDGenerator(verbose=False)

        # Create minimal metadata
        templates_meta = {'templates': [], 'total_templates': 0}
        guardrails_meta = {'layers': {}}
        assets_meta = {'assets': {}}

        # Generate SKILL.md
        skill_md = generator.generate_skill_md(
            sample_analysis,
            templates_meta,
            guardrails_meta,
            assets_meta
        )

        # Verify all sections present
        assert skill_md.frontmatter
        assert skill_md.overview
        assert skill_md.quick_start

        # Save
        skill_file = temp_output_dir / 'SKILL.md'
        generator.save_skill_md(skill_md, str(skill_file))

        # Verify file
        assert skill_file.exists()

        content = skill_file.read_text()
        compiled = skill_md.compile()
        assert content == compiled

    def test_skill_md_with_all_metadata(self, sample_analysis, temp_output_dir):
        """Test SKILL.md generation with complete metadata."""
        generator = SkillMDGenerator(verbose=False)

        templates_meta = {
            'templates': [
                {'name': 'basic', 'type': 'basic', 'language': 'bash'}
            ],
            'total_templates': 1
        }
        guardrails_meta = {
            'tool_name': 'test-tool',
            'layers': {
                'inline_warnings': 3,
                'validation_script': 'validate.sh',
                'checklist': 'checklist.md',
                'setup_script': 'setup.sh'
            }
        }
        assets_meta = {
            'tool_name': 'test-tool',
            'assets': {
                'troubleshooting': 'troubleshooting.md',
                'quick_reference': 'quick-ref.md'
            }
        }

        skill_md = generator.generate_skill_md(
            sample_analysis,
            templates_meta,
            guardrails_meta,
            assets_meta
        )

        compiled = skill_md.compile()

        # Should contain all major sections
        assert '---' in compiled
        assert '## Overview' in compiled or '##' in compiled
        assert '## Quick Start' in compiled or 'Quick Start' in compiled

        # Save and verify
        skill_file = temp_output_dir / 'SKILL.md'
        generator.save_skill_md(skill_md, str(skill_file))
        assert skill_file.exists()

    def test_skill_md_structure(self, sample_analysis):
        """Test SKILL.md has proper structure."""
        generator = SkillMDGenerator(verbose=False)

        skill_md = generator.generate_skill_md(sample_analysis, None, None, None)
        compiled = skill_md.compile()

        # Check structure
        lines = compiled.split('\n')

        # Should start with frontmatter
        assert lines[0] == '---'

        # Should have markdown content after frontmatter
        assert any('##' in line for line in lines)
