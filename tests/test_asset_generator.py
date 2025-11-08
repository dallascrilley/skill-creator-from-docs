#!/usr/bin/env python3
"""
Unit tests for asset_generator.py
"""

import json
from pathlib import Path

import pytest

from asset_generator import (
    AssetGenerator,
    SupportAssets
)


class TestSupportAssets:
    """Tests for SupportAssets dataclass."""

    def test_support_assets_creation(self):
        """Test creating SupportAssets."""
        assets = SupportAssets(
            tool_name="test-tool",
            tool_type="cli",
            troubleshooting_tree="# Troubleshooting\n",
            quick_reference="# Quick Ref\n",
            config_template="# Config\n",
            examples_doc="# Examples\n"
        )

        assert assets.tool_name == "test-tool"
        assert assets.tool_type == "cli"
        assert "Troubleshooting" in assets.troubleshooting_tree
        assert "Quick Ref" in assets.quick_reference
        assert "Config" in assets.config_template
        assert "Examples" in assets.examples_doc

    def test_support_assets_defaults(self):
        """Test SupportAssets with default values."""
        assets = SupportAssets(
            tool_name="test-tool",
            tool_type="api"
        )

        assert assets.troubleshooting_tree == ""
        assert assets.quick_reference == ""
        assert assets.config_template == ""
        assert assets.examples_doc == ""
        assert assets.metadata == {}


class TestAssetGenerator:
    """Tests for AssetGenerator class."""

    def test_generator_initialization(self):
        """Test creating AssetGenerator instance."""
        generator = AssetGenerator(verbose=False)
        assert generator is not None
        assert generator.verbose is False

    def test_generate_troubleshooting_tree(self):
        """Test generating troubleshooting decision tree."""
        generator = AssetGenerator(verbose=False)

        pitfalls = [
            {
                'description': 'File not found',
                'severity': 'high',
                'context': 'Input validation'
            }
        ]

        tree = generator.generate_troubleshooting_tree('test-tool', pitfalls)

        assert '# Troubleshooting Guide' in tree
        assert 'test-tool' in tree
        assert 'File not found' in tree

    def test_generate_troubleshooting_tree_with_validation(self):
        """Test troubleshooting tree includes validation script reference."""
        generator = AssetGenerator(verbose=False)

        tree = generator.generate_troubleshooting_tree('test-tool', [])

        assert 'validate_prereqs.sh' in tree
        assert 'Quick Diagnosis' in tree

    def test_generate_quick_reference(self):
        """Test generating quick reference cheatsheet."""
        generator = AssetGenerator(verbose=False)

        workflows = [
            {
                'name': 'Basic Processing',
                'description': 'Process a file',
                'steps': ['Step 1', 'Step 2']
            }
        ]

        examples = [
            {
                'title': 'Basic Example',
                'language': 'bash',
                'code': 'test-tool run --input file.txt',
                'context': 'Basic usage'
            }
        ]

        ref = generator.generate_quick_reference(
            'test-tool',
            'cli',
            workflows,
            examples
        )

        assert '# Quick Reference' in ref
        assert 'test-tool' in ref
        assert 'Common Workflows' in ref

    def test_generate_quick_reference_extracts_commands(self):
        """Test quick reference extracts commands from examples."""
        generator = AssetGenerator(verbose=False)

        examples = [
            {
                'title': 'Run command',
                'language': 'bash',
                'code': 'test-tool run --input file.txt',
                'context': 'Run tool'
            },
            {
                'title': 'Validate command',
                'language': 'bash',
                'code': 'test-tool validate file.txt',
                'context': 'Validate input'
            }
        ]

        ref = generator.generate_quick_reference(
            'test-tool',
            'cli',
            [],
            examples
        )

        assert 'Key Commands' in ref
        # Should extract commands from bash examples
        assert 'test-tool' in ref

    def test_generate_config_template(self):
        """Test generating configuration file template."""
        generator = AssetGenerator(verbose=False)

        config = generator.generate_config_template(
            'test-tool',
            'cli',
            []
        )

        assert '# Configuration Template' in config
        assert 'test-tool' in config

    def test_generate_config_template_tool_specific(self):
        """Test config template includes tool-specific sections."""
        generator = AssetGenerator(verbose=False)

        # API tool should have API-specific config
        api_config = generator.generate_config_template('test-api', 'api', [])
        assert 'API' in api_config or 'api' in api_config.lower()

        # CLI tool should have CLI-specific config
        cli_config = generator.generate_config_template('test-cli', 'cli', [])
        assert isinstance(cli_config, str)
        assert 'Configuration Template' in cli_config

    def test_generate_examples_doc(self):
        """Test generating examples documentation."""
        generator = AssetGenerator(verbose=False)

        workflows = [
            {
                'name': 'Basic Workflow',
                'description': 'Basic processing',
                'steps': ['Step 1', 'Step 2']
            }
        ]

        examples = [
            {
                'title': 'Basic Example',
                'language': 'bash',
                'code': 'test-tool run',
                'context': 'Basic usage',
                'example_type': 'basic'
            },
            {
                'title': 'Advanced Example',
                'language': 'python',
                'code': 'from test_tool import run',
                'context': 'Python usage',
                'example_type': 'advanced'
            }
        ]

        doc = generator.generate_examples_doc(
            'test-tool',
            examples,
            workflows
        )

        assert '# Examples' in doc
        assert 'test-tool' in doc
        assert 'Basic Usage' in doc
        assert 'Advanced Usage' in doc

    def test_generate_examples_doc_groups_by_type(self):
        """Test examples documentation groups examples by type."""
        generator = AssetGenerator(verbose=False)

        examples = [
            {
                'title': 'Example 1',
                'language': 'bash',
                'code': 'code1',
                'context': 'context1',
                'example_type': 'basic'
            },
            {
                'title': 'Example 2',
                'language': 'bash',
                'code': 'code2',
                'context': 'context2',
                'example_type': 'advanced'
            }
        ]

        doc = generator.generate_examples_doc('test-tool', examples, [])

        # Should have separate sections
        assert '## Basic Usage' in doc
        assert '## Advanced Usage' in doc

    def test_generate_assets(self, sample_analysis):
        """Test complete asset generation workflow."""
        generator = AssetGenerator(verbose=False)

        assets = generator.generate_assets(sample_analysis)

        assert isinstance(assets, SupportAssets)
        assert assets.tool_name
        assert assets.tool_type
        assert assets.troubleshooting_tree
        assert assets.quick_reference
        assert assets.config_template
        assert assets.examples_doc

    def test_generate_assets_metadata(self, sample_analysis):
        """Test assets include metadata."""
        generator = AssetGenerator(verbose=False)

        assets = generator.generate_assets(sample_analysis)

        assert 'generated_at' in assets.metadata
        assert 'pitfalls_count' in assets.metadata
        assert 'workflows_count' in assets.metadata
        assert 'examples_count' in assets.metadata

    def test_save_assets(self, temp_output_dir, sample_analysis):
        """Test saving assets to disk."""
        generator = AssetGenerator(verbose=False)

        assets = generator.generate_assets(sample_analysis)
        generator.save_assets(assets, str(temp_output_dir))

        # Check directory structure
        assert (temp_output_dir / 'docs').exists()

        # Check files created
        assert (temp_output_dir / 'docs' / 'troubleshooting.md').exists()
        assert (temp_output_dir / 'docs' / 'quick-reference.md').exists()
        assert (temp_output_dir / 'docs' / 'examples.md').exists()
        assert (temp_output_dir / 'templates' / 'config-template.yaml').exists()
        assert (temp_output_dir / 'assets_metadata.json').exists()

    def test_save_assets_metadata_content(self, temp_output_dir, sample_analysis):
        """Test assets metadata content."""
        generator = AssetGenerator(verbose=False)

        assets = generator.generate_assets(sample_analysis)
        generator.save_assets(assets, str(temp_output_dir))

        metadata_file = temp_output_dir / 'assets_metadata.json'
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        assert metadata['tool_name'] == assets.tool_name
        assert metadata['tool_type'] == assets.tool_type
        assert 'assets' in metadata
        assert 'troubleshooting' in metadata['assets']
        assert 'quick_reference' in metadata['assets']
        assert 'config_template' in metadata['assets']
        assert 'examples' in metadata['assets']

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        generator = AssetGenerator(verbose=True)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        generator = AssetGenerator(verbose=False)
        generator.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestAssetGeneratorIntegration:
    """Integration tests for asset generator."""

    def test_full_generation_workflow(self, sample_analysis, temp_output_dir):
        """Test complete generation workflow from analysis to saved assets."""
        generator = AssetGenerator(verbose=False)

        # Generate assets
        assets = generator.generate_assets(sample_analysis)

        # Verify all asset types generated
        assert assets.troubleshooting_tree
        assert assets.quick_reference
        assert assets.config_template
        assert assets.examples_doc

        # Save assets
        generator.save_assets(assets, str(temp_output_dir))

        # Verify all files created
        assert (temp_output_dir / 'docs' / 'troubleshooting.md').exists()
        assert (temp_output_dir / 'docs' / 'quick-reference.md').exists()
        assert (temp_output_dir / 'docs' / 'examples.md').exists()
        assert (temp_output_dir / 'templates' / 'config-template.yaml').exists()

        # Verify file contents
        troubleshooting = (temp_output_dir / 'docs' / 'troubleshooting.md').read_text()
        assert '# Troubleshooting Guide' in troubleshooting

        quick_ref = (temp_output_dir / 'docs' / 'quick-reference.md').read_text()
        assert '# Quick Reference' in quick_ref

        examples = (temp_output_dir / 'docs' / 'examples.md').read_text()
        assert '# Examples' in examples

    def test_assets_with_templates(self, sample_analysis, temp_output_dir):
        """Test asset generation with template metadata."""
        generator = AssetGenerator(verbose=False)

        templates_metadata = {
            'total_templates': 2,
            'templates': [
                {'name': 'cli_basic', 'type': 'basic'}
            ]
        }

        assets = generator.generate_assets(sample_analysis, templates_metadata)

        # Should still generate all assets
        assert assets.troubleshooting_tree
        assert assets.quick_reference
        assert assets.config_template
        assert assets.examples_doc

    def test_asset_integration(self, sample_analysis, temp_output_dir):
        """Test that all assets work together."""
        generator = AssetGenerator(verbose=False)

        assets = generator.generate_assets(sample_analysis)
        generator.save_assets(assets, str(temp_output_dir))

        # All assets should reference the validation script
        troubleshooting = (temp_output_dir / 'docs' / 'troubleshooting.md').read_text()
        assert 'validate_prereqs.sh' in troubleshooting

        # Quick reference should link to other assets
        quick_ref = (temp_output_dir / 'docs' / 'quick-reference.md').read_text()
        assert 'troubleshooting.md' in quick_ref or 'examples.md' in quick_ref

    def test_helper_methods(self):
        """Test helper methods for generating content."""
        generator = AssetGenerator(verbose=False)

        # Test symptom generation
        symptoms = generator._generate_symptoms(
            "File not found error",
            "Input validation"
        )
        assert isinstance(symptoms, str)
        assert len(symptoms) > 0

        # Test diagnosis step generation
        diagnosis = generator._generate_diagnosis_steps(
            "File not found error",
            "high"
        )
        assert isinstance(diagnosis, str)
        assert len(diagnosis) > 0

        # Test solution generation
        solutions = generator._generate_solutions(
            "File not found error",
            "high"
        )
        assert isinstance(solutions, str)
        assert len(solutions) > 0

        # Test prevention generation
        prevention = generator._generate_prevention(
            "File not found error"
        )
        assert isinstance(prevention, str)
        assert len(prevention) > 0
