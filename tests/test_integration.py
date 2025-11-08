#!/usr/bin/env python3
"""
Integration tests for complete skill-creator-from-docs pipeline.
Tests the full workflow from documentation extraction to SKILL.md generation.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts directory to Python path
REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from doc_extractor import DocExtractor, DocumentationCorpus, Page
from doc_analyzer import DocAnalyzer, ToolType, AnalysisContext
from template_synthesizer import TemplateSynthesizer, Template
from guardrail_generator import GuardrailGenerator, GuardrailSet
from asset_generator import AssetGenerator, SupportAssets
from skill_md_generator import SkillMDGenerator, SkillMD


class TestCompletePipeline:
    """Integration tests for complete pipeline workflow."""

    def test_full_pipeline_from_markdown(self, fixtures_dir, temp_output_dir):
        """
        Test complete pipeline from sample markdown documentation to final SKILL.md.

        This is the end-to-end test that verifies all components work together.
        """
        # Phase 1: Extract documentation
        extractor = DocExtractor(verbose=False)
        sample_docs = fixtures_dir / "sample_docs.md"

        corpus = extractor.extract_from_markdown(str(sample_docs))

        # Verify extraction
        assert isinstance(corpus, DocumentationCorpus)
        assert len(corpus.pages) > 0
        assert corpus.metadata

        # Phase 2: Analyze documentation
        analyzer = DocAnalyzer(verbose=False)

        analysis = analyzer.analyze(corpus)

        # Verify analysis
        assert isinstance(analysis, AnalysisContext)
        assert analysis.tool_type in [t for t in ToolType]
        assert len(analysis.examples) > 0
        assert isinstance(analysis.metadata, dict)

        # Phase 3: Synthesize templates
        synthesizer = TemplateSynthesizer(verbose=False)

        # Convert analysis to dict for template synthesis
        examples = [
            {
                'title': ex.title,
                'language': ex.language,
                'code': ex.code,
                'context': ex.context
            }
            for ex in analysis.examples
        ]

        patterns = []  # Patterns are optional
        tool_type = analysis.tool_type.value

        templates = synthesizer.synthesize_templates(examples, patterns, tool_type)

        # Verify templates
        assert len(templates) >= 1
        assert all(isinstance(t, Template) for t in templates)

        # Save templates
        templates_dir = temp_output_dir / "templates"
        templates_dir.mkdir()
        synthesizer.save_templates(templates, str(templates_dir))

        # Load templates metadata
        templates_meta_file = templates_dir / "_templates_metadata.json"
        assert templates_meta_file.exists()

        with open(templates_meta_file, 'r') as f:
            templates_meta = json.load(f)

        # Phase 4: Generate guardrails
        guardrail_gen = GuardrailGenerator(verbose=False)

        # Convert analysis to dict for guardrail generation
        analysis_dict = {
            'tool_type': analysis.tool_type.value,
            'metadata': analysis.metadata,
            'workflows': [
                {
                    'name': wf.name,
                    'description': wf.description,
                    'steps': wf.steps,
                    'frequency': wf.frequency
                }
                for wf in analysis.workflows
            ],
            'pitfalls': [
                {
                    'description': pf.description,
                    'severity': pf.severity,
                    'context': pf.context,
                    'source_url': pf.source_url
                }
                for pf in analysis.pitfalls
            ],
            'examples': examples
        }

        guardrails = guardrail_gen.generate_guardrails(analysis_dict, templates_meta)

        # Verify guardrails
        assert isinstance(guardrails, GuardrailSet)
        assert guardrails.inline_warnings
        assert guardrails.validation_script
        assert guardrails.checklist
        assert guardrails.setup_script

        # Save guardrails
        guardrails_dir = temp_output_dir / "guardrails"
        guardrails_dir.mkdir()
        guardrail_gen.save_guardrails(guardrails, str(guardrails_dir))

        # Load guardrails metadata
        guardrails_meta_file = guardrails_dir / "guardrails_metadata.json"
        assert guardrails_meta_file.exists()

        with open(guardrails_meta_file, 'r') as f:
            guardrails_meta = json.load(f)

        # Phase 5: Generate support assets
        asset_gen = AssetGenerator(verbose=False)

        assets = asset_gen.generate_assets(analysis_dict, templates_meta)

        # Verify assets
        assert isinstance(assets, SupportAssets)
        assert assets.troubleshooting_tree
        assert assets.quick_reference
        assert assets.config_template
        assert assets.examples_doc

        # Save assets
        assets_dir = temp_output_dir / "assets"
        assets_dir.mkdir()
        asset_gen.save_assets(assets, str(assets_dir))

        # Load assets metadata
        assets_meta_file = assets_dir / "assets_metadata.json"
        assert assets_meta_file.exists()

        with open(assets_meta_file, 'r') as f:
            assets_meta = json.load(f)

        # Phase 6: Generate SKILL.md
        skill_gen = SkillMDGenerator(verbose=False)

        skill_md = skill_gen.generate_skill_md(
            analysis_dict,
            templates_meta,
            guardrails_meta,
            assets_meta
        )

        # Verify SKILL.md
        assert isinstance(skill_md, SkillMD)
        assert skill_md.frontmatter
        assert skill_md.overview
        assert skill_md.quick_start

        # Save SKILL.md
        skill_file = temp_output_dir / "SKILL.md"
        skill_gen.save_skill_md(skill_md, str(skill_file))

        # Final verification
        assert skill_file.exists()

        content = skill_file.read_text()
        assert '---' in content  # Has frontmatter
        assert '##' in content  # Has sections
        assert len(content) > 100  # Has substantial content

        # Verify directory structure
        assert (temp_output_dir / "templates").exists()
        assert (temp_output_dir / "guardrails" / "scripts").exists()
        assert (temp_output_dir / "guardrails" / "checklists").exists()
        assert (temp_output_dir / "assets" / "docs").exists()
        assert (temp_output_dir / "SKILL.md").exists()

        # Verify key files
        assert (guardrails_dir / "scripts" / "validate_prereqs.sh").exists()
        assert (guardrails_dir / "checklists" / "pre-flight.md").exists()
        assert (assets_dir / "docs" / "troubleshooting.md").exists()
        assert (assets_dir / "docs" / "quick-reference.md").exists()

    def test_pipeline_with_real_corpus(self, cli_tool_corpus, temp_output_dir):
        """
        Test pipeline using the CLI tool corpus fixture.

        Tests the pipeline with pre-extracted documentation corpus.
        """
        # Start from Phase 2 with pre-extracted corpus
        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        # Analyze
        analyzer = DocAnalyzer(verbose=False)
        analysis = analyzer.analyze(corpus)

        assert isinstance(analysis, AnalysisContext)
        assert len(analysis.examples) > 0

        # Convert to dict for subsequent phases
        analysis_dict = {
            'tool_type': analysis.tool_type.value,
            'metadata': analysis.metadata,
            'workflows': [
                {
                    'name': wf.name,
                    'description': wf.description,
                    'steps': wf.steps,
                    'frequency': wf.frequency
                }
                for wf in analysis.workflows
            ],
            'pitfalls': [
                {
                    'description': pf.description,
                    'severity': pf.severity,
                    'context': pf.context,
                    'source_url': pf.source_url
                }
                for pf in analysis.pitfalls
            ],
            'examples': [
                {
                    'title': ex.title,
                    'language': ex.language,
                    'code': ex.code,
                    'context': ex.context
                }
                for ex in analysis.examples
            ]
        }

        # Generate SKILL.md without templates/guardrails/assets for simpler test
        skill_gen = SkillMDGenerator(verbose=False)

        skill_md = skill_gen.generate_skill_md(
            analysis_dict,
            None,  # No templates
            None,  # No guardrails
            None   # No assets
        )

        # Verify and save
        assert isinstance(skill_md, SkillMD)

        skill_file = temp_output_dir / "SKILL.md"
        skill_gen.save_skill_md(skill_md, str(skill_file))

        assert skill_file.exists()
        content = skill_file.read_text()
        assert '---' in content
        assert '##' in content

    def test_pipeline_error_handling(self, temp_output_dir):
        """
        Test pipeline handles edge cases gracefully.

        Tests with minimal/empty inputs to verify error handling.
        """
        # Create minimal corpus with empty pages
        corpus = DocumentationCorpus(
            source="test://minimal",
            pages=[],
            metadata={'tool_name': 'test-tool'}
        )

        # Analysis should still work
        analyzer = DocAnalyzer(verbose=False)
        analysis = analyzer.analyze(corpus)

        # Should classify as unknown with low confidence
        assert analysis.tool_type in [t for t in ToolType]
        assert isinstance(analysis.metadata, dict)

        # SKILL.md generation should handle empty analysis
        analysis_dict = {
            'tool_type': analysis.tool_type.value,
            'metadata': analysis.metadata,
            'workflows': [],
            'pitfalls': [],
            'examples': []
        }

        skill_gen = SkillMDGenerator(verbose=False)
        skill_md = skill_gen.generate_skill_md(analysis_dict, None, None, None)

        # Should still generate valid SKILL.md
        assert isinstance(skill_md, SkillMD)
        assert skill_md.frontmatter

        # Save and verify
        skill_file = temp_output_dir / "SKILL.md"
        skill_gen.save_skill_md(skill_md, str(skill_file))

        assert skill_file.exists()
        content = skill_file.read_text()
        assert '---' in content


class TestPipelineComponents:
    """Test component interactions and data flow."""

    def test_analysis_to_templates_conversion(self, sample_analysis):
        """Test converting analysis results to template synthesis input."""
        synthesizer = TemplateSynthesizer(verbose=False)

        examples = sample_analysis['examples']
        patterns = sample_analysis.get('patterns', [])
        tool_type = sample_analysis['tool_type']

        templates = synthesizer.synthesize_templates(examples, patterns, tool_type)

        assert len(templates) >= 1
        assert all(t.language for t in templates)
        assert all(t.content for t in templates)

    def test_metadata_flow_through_pipeline(self, sample_analysis, temp_output_dir):
        """Test that metadata flows correctly through all pipeline stages."""
        # Generate all components
        templates_dir = temp_output_dir / "templates"
        templates_dir.mkdir()

        synthesizer = TemplateSynthesizer(verbose=False)
        templates = synthesizer.synthesize_templates(
            sample_analysis['examples'],
            [],
            sample_analysis['tool_type']
        )
        synthesizer.save_templates(templates, str(templates_dir))

        # Load templates metadata
        with open(templates_dir / "_templates_metadata.json", 'r') as f:
            templates_meta = json.load(f)

        # Generate guardrails
        guardrails_dir = temp_output_dir / "guardrails"
        guardrails_dir.mkdir()

        guardrail_gen = GuardrailGenerator(verbose=False)
        guardrails = guardrail_gen.generate_guardrails(sample_analysis, templates_meta)
        guardrail_gen.save_guardrails(guardrails, str(guardrails_dir))

        # Load guardrails metadata
        with open(guardrails_dir / "guardrails_metadata.json", 'r') as f:
            guardrails_meta = json.load(f)

        # Generate assets
        assets_dir = temp_output_dir / "assets"
        assets_dir.mkdir()

        asset_gen = AssetGenerator(verbose=False)
        assets = asset_gen.generate_assets(sample_analysis, templates_meta)
        asset_gen.save_assets(assets, str(assets_dir))

        # Load assets metadata
        with open(assets_dir / "assets_metadata.json", 'r') as f:
            assets_meta = json.load(f)

        # Verify metadata consistency
        tool_name = sample_analysis['metadata']['tool_name']

        assert guardrails_meta['tool_name'] == tool_name
        assert assets_meta['tool_name'] == tool_name

        # All metadata files should have timestamps
        assert 'created_at' in templates_meta or 'generated_at' in templates_meta
        assert 'generated_at' in guardrails_meta['metadata']
        assert 'generated_at' in assets_meta['metadata']
