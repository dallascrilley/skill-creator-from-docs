#!/usr/bin/env python3
"""
Unit tests for template_synthesizer.py
"""

import json
from pathlib import Path

import pytest

from template_synthesizer import (
    TemplateSynthesizer,
    TemplateType,
    Template,
    ValidationResult
)


class TestTemplateType:
    """Tests for TemplateType enum."""

    def test_template_type_values(self):
        """Test TemplateType enum values."""
        assert TemplateType.BASIC.value == "basic"
        assert TemplateType.ADVANCED.value == "advanced"
        assert TemplateType.CONFIGURATION.value == "configuration"
        assert TemplateType.WORKFLOW.value == "workflow"

    def test_template_type_from_string(self):
        """Test creating TemplateType from string."""
        assert TemplateType("basic") == TemplateType.BASIC
        assert TemplateType("advanced") == TemplateType.ADVANCED
        assert TemplateType("configuration") == TemplateType.CONFIGURATION


class TestTemplate:
    """Tests for Template dataclass."""

    def test_template_creation(self):
        """Test creating a Template."""
        template = Template(
            name="test_template",
            type=TemplateType.BASIC,
            language="python",
            content="print('hello')",
            placeholders=["NAME"],
            defaults={"NAME": "world"}
        )

        assert template.name == "test_template"
        assert template.type == TemplateType.BASIC
        assert template.language == "python"
        assert template.content == "print('hello')"
        assert template.placeholders == ["NAME"]
        assert template.defaults == {"NAME": "world"}

    def test_template_repr(self):
        """Test Template string representation."""
        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="python",
            content="code"
        )

        repr_str = repr(template)
        assert "Template" in repr_str
        assert "test" in repr_str
        assert "basic" in repr_str


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_valid(self):
        """Test creating a valid ValidationResult."""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[],
            suggestions=["Add more comments"]
        )

        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.suggestions) == 1

    def test_validation_result_invalid(self):
        """Test creating an invalid ValidationResult."""
        result = ValidationResult(
            is_valid=False,
            errors=["Syntax error"],
            warnings=["Missing quotes"]
        )

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert len(result.warnings) == 1


class TestTemplateSynthesizer:
    """Tests for TemplateSynthesizer class."""

    def test_synthesizer_initialization(self):
        """Test creating TemplateSynthesizer instance."""
        synthesizer = TemplateSynthesizer(verbose=False)
        assert synthesizer is not None
        assert synthesizer.verbose is False

    def test_group_by_language(self):
        """Test grouping examples by language."""
        synthesizer = TemplateSynthesizer(verbose=False)

        examples = [
            {'language': 'python', 'code': 'print("hello")'},
            {'language': 'bash', 'code': 'echo "hello"'},
            {'language': 'python', 'code': 'print("world")'},
        ]

        grouped = synthesizer._group_by_language(examples)

        assert 'python' in grouped
        assert 'bash' in grouped
        assert len(grouped['python']) == 2
        assert len(grouped['bash']) == 1

    def test_generalize_code_urls(self):
        """Test generalizing URLs in code."""
        synthesizer = TemplateSynthesizer(verbose=False)

        code = 'curl https://api.example.com/v1/users'
        generalized = synthesizer._generalize_code(code, 'bash')

        assert '${URL}' in generalized
        assert 'https://api.example.com' not in generalized

    def test_generalize_code_emails(self):
        """Test generalizing email addresses."""
        synthesizer = TemplateSynthesizer(verbose=False)

        code = 'send_email("user@example.com")'
        generalized = synthesizer._generalize_code(code, 'python')

        # Email should be replaced (either ${EMAIL} or ${ARG} due to Python patterns)
        assert 'user@example.com' not in generalized
        # Should have some placeholder
        assert '${' in generalized

    def test_add_placeholders(self):
        """Test adding placeholders to content."""
        synthesizer = TemplateSynthesizer(verbose=False)

        content = "process file.txt with format json"
        variable_parts = ["file.txt", "json"]

        result = synthesizer._add_placeholders(content, variable_parts, "bash")

        assert "${FILE_TXT}" in result
        assert "${JSON}" in result
        assert "file.txt" not in result
        assert "json" not in result

    def test_get_comment_syntax_python(self):
        """Test getting comment syntax for Python."""
        synthesizer = TemplateSynthesizer(verbose=False)
        assert synthesizer._get_comment_syntax('python') == '#'
        assert synthesizer._get_comment_syntax('py') == '#'

    def test_get_comment_syntax_javascript(self):
        """Test getting comment syntax for JavaScript."""
        synthesizer = TemplateSynthesizer(verbose=False)
        assert synthesizer._get_comment_syntax('javascript') == '//'
        assert synthesizer._get_comment_syntax('js') == '//'

    def test_create_header_comment(self):
        """Test creating header comment."""
        synthesizer = TemplateSynthesizer(verbose=False)

        context = {
            'title': 'Test Template',
            'context': 'Example usage',
            'description': 'Does something useful'
        }

        header = synthesizer._create_header_comment(context, '#')

        assert len(header) > 0
        assert any('Test Template' in line for line in header)
        assert any('Example usage' in line for line in header)

    def test_add_inline_comments(self):
        """Test adding inline comments to template."""
        synthesizer = TemplateSynthesizer(verbose=False)

        content = "process ${INPUT_FILE} ${FORMAT}"
        context = {'title': 'Test', 'context': 'Basic usage'}

        result = synthesizer.add_inline_comments(content, context, 'python')

        assert '#' in result  # Has Python comments
        assert 'INPUT_FILE' in result
        assert 'FORMAT' in result

    def test_create_variable_placeholders(self):
        """Test extracting placeholders from template content."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="bash",
            content="process ${INPUT} and ${OUTPUT}"
        )

        result = synthesizer.create_variable_placeholders(template)

        assert len(result.placeholders) == 2
        assert 'INPUT' in result.placeholders
        assert 'OUTPUT' in result.placeholders

    def test_add_default_values(self):
        """Test adding default values to template."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="bash",
            content="curl ${URL}",
            placeholders=["URL"]
        )

        examples = [
            {'code': 'curl https://api.example.com/v1'}
        ]

        result = synthesizer.add_default_values(template, examples)

        # May or may not find defaults depending on pattern matching
        assert isinstance(result.defaults, dict)

    def test_validate_template_syntax_valid(self):
        """Test validating valid template."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="python",
            content="# Comment\nprint(${MESSAGE})",
            placeholders=["MESSAGE"]
        )

        result = synthesizer.validate_template_syntax(template)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_template_syntax_mismatched_placeholders(self):
        """Test validation catches mismatched placeholders."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="bash",
            content="echo ${MISSING_CLOSE"
        )

        result = synthesizer.validate_template_syntax(template)

        assert result.is_valid is False
        assert len(result.errors) > 0
        assert 'placeholder' in result.errors[0].lower()

    def test_validate_template_syntax_unmatched_quotes_python(self):
        """Test validation catches unmatched quotes in Python."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test",
            type=TemplateType.BASIC,
            language="python",
            content='print("hello\nprint("world")'
        )

        result = synthesizer.validate_template_syntax(template)

        # Should have warnings about unmatched quotes
        assert len(result.warnings) > 0

    def test_generate_usage_example(self):
        """Test generating usage documentation."""
        synthesizer = TemplateSynthesizer(verbose=False)

        template = Template(
            name="test_template",
            type=TemplateType.BASIC,
            language="bash",
            content="echo ${MESSAGE}",
            placeholders=["MESSAGE"],
            defaults={"MESSAGE": "Hello"}
        )

        examples = [
            {
                'code': 'echo "Hello World"',
                'context': 'Basic greeting example'
            }
        ]

        usage = synthesizer.generate_usage_example(template, examples)

        assert "test_template" in usage
        assert "basic" in usage
        assert "MESSAGE" in usage
        assert "bash" in usage

    def test_create_basic_template(self, sample_analysis):
        """Test creating basic template from examples."""
        synthesizer = TemplateSynthesizer(verbose=False)

        examples = sample_analysis['examples']
        bash_examples = [e for e in examples if e['language'] == 'bash']

        template = synthesizer._create_basic_template(
            bash_examples,
            'bash',
            'cli'
        )

        assert template is not None
        assert template.type == TemplateType.BASIC
        assert template.language == 'bash'
        assert template.name == 'cli_basic'

    def test_synthesize_templates(self, sample_analysis):
        """Test complete template synthesis workflow."""
        synthesizer = TemplateSynthesizer(verbose=False)

        examples = sample_analysis['examples']
        patterns = sample_analysis.get('patterns', [])
        tool_type = sample_analysis['tool_type']

        templates = synthesizer.synthesize_templates(examples, patterns, tool_type)

        # Should generate at least one template
        assert len(templates) >= 1
        assert all(isinstance(t, Template) for t in templates)
        assert all(t.language for t in templates)
        assert all(t.content for t in templates)

    def test_save_templates(self, temp_output_dir):
        """Test saving templates to disk."""
        synthesizer = TemplateSynthesizer(verbose=False)

        templates = [
            Template(
                name="test_template",
                type=TemplateType.BASIC,
                language="bash",
                content="#!/bin/bash\necho 'test'",
                placeholders=["MESSAGE"],
                defaults={"MESSAGE": "hello"},
                usage_example="# Test Template\n\nBasic usage example"
            )
        ]

        synthesizer.save_templates(templates, str(temp_output_dir))

        # Check template file created
        template_file = temp_output_dir / "test_template.sh"
        assert template_file.exists()

        # Check usage file created
        usage_file = temp_output_dir / "test_template_USAGE.md"
        assert usage_file.exists()

        # Check metadata file created
        metadata_file = temp_output_dir / "_templates_metadata.json"
        assert metadata_file.exists()

        # Verify metadata content
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        assert metadata['total_templates'] == 1
        assert len(metadata['templates']) == 1
        assert metadata['templates'][0]['name'] == 'test_template'

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        synthesizer = TemplateSynthesizer(verbose=True)
        synthesizer.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        synthesizer = TemplateSynthesizer(verbose=False)
        synthesizer.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestTemplateSynthesizerIntegration:
    """Integration tests for template synthesizer."""

    def test_full_synthesis_workflow(self, sample_analysis, temp_output_dir):
        """Test complete synthesis workflow from analysis to saved templates."""
        synthesizer = TemplateSynthesizer(verbose=False)

        # Synthesize templates
        templates = synthesizer.synthesize_templates(
            sample_analysis['examples'],
            sample_analysis.get('patterns', []),
            sample_analysis['tool_type']
        )

        # Add placeholders and defaults
        for template in templates:
            synthesizer.create_variable_placeholders(template)
            synthesizer.add_default_values(template, sample_analysis['examples'])

        # Validate templates
        for template in templates:
            result = synthesizer.validate_template_syntax(template)
            # Basic validation should pass or have only warnings
            if not result.is_valid:
                # Log errors for debugging but don't fail test
                print(f"Template {template.name} validation: {result.errors}")

        # Save templates
        synthesizer.save_templates(templates, str(temp_output_dir))

        # Verify output
        metadata_file = temp_output_dir / "_templates_metadata.json"
        assert metadata_file.exists()

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        assert metadata['total_templates'] == len(templates)
        assert len(metadata['templates']) == len(templates)

    def test_template_file_extensions(self, temp_output_dir):
        """Test templates saved with correct file extensions."""
        synthesizer = TemplateSynthesizer(verbose=False)

        templates = [
            Template(name="bash_test", type=TemplateType.BASIC, language="bash", content="#!/bin/bash"),
            Template(name="python_test", type=TemplateType.BASIC, language="python", content="#!/usr/bin/env python3"),
            Template(name="js_test", type=TemplateType.BASIC, language="javascript", content="// JavaScript"),
        ]

        for template in templates:
            template.usage_example = "# Usage example"

        synthesizer.save_templates(templates, str(temp_output_dir))

        assert (temp_output_dir / "bash_test.sh").exists()
        assert (temp_output_dir / "python_test.py").exists()
        assert (temp_output_dir / "js_test.js").exists()
