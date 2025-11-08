#!/usr/bin/env python3
"""
Unit tests for guardrail_generator.py
"""

import json
from pathlib import Path

import pytest

from guardrail_generator import (
    GuardrailGenerator,
    Guardrail,
    GuardrailSet
)


class TestGuardrail:
    """Tests for Guardrail dataclass."""

    def test_guardrail_creation(self):
        """Test creating a Guardrail."""
        guardrail = Guardrail(
            name="Test Check",
            description="Check test prerequisites",
            severity="high",
            check_type="prerequisite",
            auto_fixable=True,
            fix_command="install test-tool"
        )

        assert guardrail.name == "Test Check"
        assert guardrail.description == "Check test prerequisites"
        assert guardrail.severity == "high"
        assert guardrail.check_type == "prerequisite"
        assert guardrail.auto_fixable is True
        assert guardrail.fix_command == "install test-tool"

    def test_guardrail_defaults(self):
        """Test Guardrail with default values."""
        guardrail = Guardrail(
            name="Basic Check",
            description="Check basics",
            severity="low",
            check_type="validation"
        )

        assert guardrail.auto_fixable is False
        assert guardrail.fix_command == ""


class TestGuardrailSet:
    """Tests for GuardrailSet dataclass."""

    def test_guardrail_set_creation(self):
        """Test creating a GuardrailSet."""
        guardrail_set = GuardrailSet(
            tool_name="test-tool",
            tool_type="cli",
            inline_warnings={"high": ["Warning 1"], "medium": ["Warning 2"]},
            validation_script="#!/bin/bash\necho 'validate'",
            checklist="# Checklist\n- [ ] Check 1",
            setup_script="#!/bin/bash\necho 'setup'"
        )

        assert guardrail_set.tool_name == "test-tool"
        assert guardrail_set.tool_type == "cli"
        assert len(guardrail_set.inline_warnings["high"]) == 1
        assert "validate" in guardrail_set.validation_script
        assert "Checklist" in guardrail_set.checklist
        assert "setup" in guardrail_set.setup_script

    def test_guardrail_set_defaults(self):
        """Test GuardrailSet with default values."""
        guardrail_set = GuardrailSet(
            tool_name="test-tool",
            tool_type="api"
        )

        assert guardrail_set.inline_warnings == {}
        assert guardrail_set.validation_script == ""
        assert guardrail_set.checklist == ""
        assert guardrail_set.setup_script == ""
        assert guardrail_set.metadata == {}


class TestGuardrailGenerator:
    """Tests for GuardrailGenerator class."""

    def test_generator_initialization(self):
        """Test creating GuardrailGenerator instance."""
        generator = GuardrailGenerator(verbose=False)
        assert generator is not None
        assert generator.verbose is False

    def test_generate_inline_warnings_by_severity(self):
        """Test generating inline warnings categorized by severity."""
        generator = GuardrailGenerator(verbose=False)

        pitfalls = [
            {'description': 'Critical error', 'severity': 'critical'},
            {'description': 'High priority issue', 'severity': 'high'},
            {'description': 'Medium issue', 'severity': 'medium'},
            {'description': 'Low priority note', 'severity': 'low'}
        ]

        warnings = generator.generate_inline_warnings(pitfalls)

        assert 'critical' in warnings
        assert 'high' in warnings
        assert 'medium' in warnings
        assert 'low' in warnings
        assert len(warnings['critical']) == 1
        assert len(warnings['high']) == 1
        assert len(warnings['medium']) == 1
        assert len(warnings['low']) == 1

    def test_generate_inline_warnings_content(self):
        """Test inline warning content format."""
        generator = GuardrailGenerator(verbose=False)

        pitfalls = [
            {'description': 'File not found', 'severity': 'high'}
        ]

        warnings = generator.generate_inline_warnings(pitfalls)

        assert len(warnings['high']) == 1
        warning = warnings['high'][0]
        assert 'PITFALL' in warning
        assert 'File not found' in warning

    def test_identify_checks_common(self):
        """Test identifying common validation checks."""
        generator = GuardrailGenerator(verbose=False)

        checks = generator._identify_checks('cli', [], [])

        assert len(checks) > 0
        assert any('Command exists' in check['name'] for check in checks)

    def test_identify_checks_api(self):
        """Test API-specific validation checks."""
        generator = GuardrailGenerator(verbose=False)

        checks = generator._identify_checks('api', [], [])

        # Should include API-specific checks
        assert any('API key' in check['name'] for check in checks)

    def test_identify_checks_cli(self):
        """Test CLI-specific validation checks."""
        generator = GuardrailGenerator(verbose=False)

        checks = generator._identify_checks('cli', [], [])

        # Should include CLI-specific checks
        assert any('PATH' in check['name'] for check in checks)

    def test_identify_checks_from_pitfalls(self):
        """Test generating checks from pitfalls."""
        generator = GuardrailGenerator(verbose=False)

        pitfalls = [
            {'description': 'Permission denied error', 'severity': 'high'}
        ]

        checks = generator._identify_checks('cli', pitfalls, [])

        # Should include permission check
        assert any('Permission' in check['name'] for check in checks)

    def test_generate_validation_script(self):
        """Test generating validation script."""
        generator = GuardrailGenerator(verbose=False)

        script = generator.generate_validation_script(
            'test-tool',
            'cli',
            [],
            []
        )

        assert '#!/bin/bash' in script
        assert 'test-tool' in script
        assert 'checks_passed' in script
        assert 'checks_failed' in script

    def test_generate_validation_script_with_checks(self):
        """Test validation script includes check functions."""
        generator = GuardrailGenerator(verbose=False)

        pitfalls = [
            {'description': 'Missing file', 'severity': 'high'}
        ]

        script = generator.generate_validation_script(
            'test-tool',
            'cli',
            pitfalls,
            []
        )

        # Should contain check function definitions
        assert 'check_' in script
        assert '() {' in script

    def test_generate_checklist(self):
        """Test generating pre-flight checklist."""
        generator = GuardrailGenerator(verbose=False)

        checklist = generator.generate_checklist(
            'test-tool',
            'cli',
            [],
            []
        )

        assert '# Pre-Flight Checklist' in checklist
        assert 'test-tool' in checklist
        assert '## 📋 Prerequisites' in checklist
        assert '## ⚙️ Configuration' in checklist

    def test_generate_checklist_with_pitfalls(self):
        """Test checklist includes pitfalls."""
        generator = GuardrailGenerator(verbose=False)

        pitfalls = [
            {'description': 'File not found', 'severity': 'critical'},
            {'description': 'Invalid format', 'severity': 'medium'}
        ]

        checklist = generator.generate_checklist(
            'test-tool',
            'cli',
            pitfalls,
            []
        )

        assert 'File not found' in checklist
        assert 'Invalid format' in checklist
        assert '🔴' in checklist  # Critical marker
        assert '🟡' in checklist  # Medium marker

    def test_generate_checklist_api_specific(self):
        """Test API-specific checklist items."""
        generator = GuardrailGenerator(verbose=False)

        checklist = generator.generate_checklist(
            'test-api',
            'api',
            [],
            []
        )

        assert 'API credentials' in checklist
        assert 'Network connectivity' in checklist

    def test_generate_setup_script(self):
        """Test generating setup script."""
        generator = GuardrailGenerator(verbose=False)

        script = generator.generate_setup_script(
            'test-tool',
            'cli',
            []
        )

        assert '#!/bin/bash' in script
        assert 'test-tool' in script
        assert 'Step 1' in script
        assert 'Step 2' in script
        assert 'mkdir' in script

    def test_generate_setup_script_cli(self):
        """Test CLI-specific setup steps."""
        generator = GuardrailGenerator(verbose=False)

        script = generator.generate_setup_script(
            'test-tool',
            'cli',
            []
        )

        assert 'Install CLI tool' in script

    def test_generate_setup_script_api(self):
        """Test API-specific setup steps."""
        generator = GuardrailGenerator(verbose=False)

        script = generator.generate_setup_script(
            'test-api',
            'api',
            []
        )

        assert 'Configure API access' in script
        assert 'API_KEY' in script

    def test_generate_guardrails(self, sample_analysis):
        """Test complete guardrail generation workflow."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)

        assert isinstance(guardrails, GuardrailSet)
        assert guardrails.tool_name
        assert guardrails.tool_type
        assert isinstance(guardrails.inline_warnings, dict)
        assert guardrails.validation_script
        assert guardrails.checklist
        assert guardrails.setup_script

    def test_generate_guardrails_metadata(self, sample_analysis):
        """Test guardrails include metadata."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)

        assert 'generated_at' in guardrails.metadata
        assert 'pitfalls_count' in guardrails.metadata
        assert 'workflows_count' in guardrails.metadata

    def test_save_guardrails(self, temp_output_dir, sample_analysis):
        """Test saving guardrails to disk."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)
        generator.save_guardrails(guardrails, str(temp_output_dir))

        # Check directory structure
        assert (temp_output_dir / 'scripts').exists()
        assert (temp_output_dir / 'checklists').exists()

        # Check files created
        assert (temp_output_dir / 'inline_warnings.json').exists()
        assert (temp_output_dir / 'scripts' / 'validate_prereqs.sh').exists()
        assert (temp_output_dir / 'checklists' / 'pre-flight.md').exists()
        assert (temp_output_dir / 'scripts' / 'setup.sh').exists()
        assert (temp_output_dir / 'guardrails_metadata.json').exists()

    def test_save_guardrails_executable_permissions(self, temp_output_dir, sample_analysis):
        """Test scripts saved with executable permissions."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)
        generator.save_guardrails(guardrails, str(temp_output_dir))

        # Check scripts are executable
        validation_script = temp_output_dir / 'scripts' / 'validate_prereqs.sh'
        setup_script = temp_output_dir / 'scripts' / 'setup.sh'

        assert validation_script.stat().st_mode & 0o100  # Owner executable
        assert setup_script.stat().st_mode & 0o100

    def test_save_guardrails_metadata_content(self, temp_output_dir, sample_analysis):
        """Test guardrails metadata content."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)
        generator.save_guardrails(guardrails, str(temp_output_dir))

        metadata_file = temp_output_dir / 'guardrails_metadata.json'
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        assert metadata['tool_name'] == guardrails.tool_name
        assert metadata['tool_type'] == guardrails.tool_type
        assert 'layers' in metadata
        assert 'inline_warnings' in metadata['layers']
        assert 'validation_script' in metadata['layers']
        assert 'checklist' in metadata['layers']
        assert 'setup_script' in metadata['layers']

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        generator = GuardrailGenerator(verbose=True)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        generator = GuardrailGenerator(verbose=False)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestGuardrailGeneratorIntegration:
    """Integration tests for guardrail generator."""

    def test_full_generation_workflow(self, sample_analysis, temp_output_dir):
        """Test complete generation workflow from analysis to saved guardrails."""
        generator = GuardrailGenerator(verbose=False)

        # Generate guardrails
        guardrails = generator.generate_guardrails(sample_analysis)

        # Verify all layers generated
        assert guardrails.inline_warnings
        assert guardrails.validation_script
        assert guardrails.checklist
        assert guardrails.setup_script

        # Save guardrails
        generator.save_guardrails(guardrails, str(temp_output_dir))

        # Verify all files created
        assert (temp_output_dir / 'inline_warnings.json').exists()
        assert (temp_output_dir / 'scripts' / 'validate_prereqs.sh').exists()
        assert (temp_output_dir / 'checklists' / 'pre-flight.md').exists()
        assert (temp_output_dir / 'scripts' / 'setup.sh').exists()

        # Verify file contents
        validation_script = (temp_output_dir / 'scripts' / 'validate_prereqs.sh').read_text()
        assert '#!/bin/bash' in validation_script

        checklist = (temp_output_dir / 'checklists' / 'pre-flight.md').read_text()
        assert '# Pre-Flight Checklist' in checklist

    def test_guardrails_with_templates(self, sample_analysis, temp_output_dir):
        """Test guardrail generation with template metadata."""
        generator = GuardrailGenerator(verbose=False)

        templates_metadata = {
            'total_templates': 2,
            'templates': [
                {'name': 'cli_basic', 'type': 'basic'}
            ]
        }

        guardrails = generator.generate_guardrails(sample_analysis, templates_metadata)

        # Should still generate all layers
        assert guardrails.inline_warnings
        assert guardrails.validation_script
        assert guardrails.checklist
        assert guardrails.setup_script

    def test_layer_integration(self, sample_analysis, temp_output_dir):
        """Test that all 4 layers work together."""
        generator = GuardrailGenerator(verbose=False)

        guardrails = generator.generate_guardrails(sample_analysis)
        generator.save_guardrails(guardrails, str(temp_output_dir))

        # Layer 1: Inline warnings should be JSON
        warnings_file = temp_output_dir / 'inline_warnings.json'
        with open(warnings_file, 'r') as f:
            warnings = json.load(f)
        assert isinstance(warnings, dict)

        # Layer 2: Validation script should be executable bash
        validation = (temp_output_dir / 'scripts' / 'validate_prereqs.sh').read_text()
        assert validation.startswith('#!/bin/bash')

        # Layer 3: Checklist should be markdown
        checklist = (temp_output_dir / 'checklists' / 'pre-flight.md').read_text()
        assert checklist.startswith('#')

        # Layer 4: Setup script should be executable bash
        setup = (temp_output_dir / 'scripts' / 'setup.sh').read_text()
        assert setup.startswith('#!/bin/bash')
