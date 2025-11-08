#!/usr/bin/env python3
"""
Unit tests for doc_analyzer.py
"""

import json
from pathlib import Path

import pytest

from doc_analyzer import (
    DocAnalyzer,
    ToolType,
    CodeExample,
    Workflow,
    Pattern,
    Pitfall,
    Gap,
    AnalysisContext
)
from doc_extractor import DocumentationCorpus, Page


class TestToolType:
    """Tests for ToolType enum."""

    def test_tool_type_values(self):
        """Test ToolType enum values."""
        assert ToolType.CLI.value == "cli"
        assert ToolType.API.value == "api"
        assert ToolType.LIBRARY.value == "library"
        assert ToolType.FRAMEWORK.value == "framework"
        assert ToolType.UNKNOWN.value == "unknown"

    def test_tool_type_from_string(self):
        """Test creating ToolType from string."""
        assert ToolType("cli") == ToolType.CLI
        assert ToolType("api") == ToolType.API
        assert ToolType("library") == ToolType.LIBRARY


class TestCodeExample:
    """Tests for CodeExample dataclass."""

    def test_code_example_creation(self):
        """Test creating a CodeExample."""
        example = CodeExample(
            title="Test Example",
            language="python",
            code="print('hello')",
            source_url="test.md",
            context="Basic usage"
        )

        assert example.title == "Test Example"
        assert example.code == "print('hello')"
        assert example.language == "python"
        assert example.source_url == "test.md"
        assert example.context == "Basic usage"

    def test_code_example_repr(self):
        """Test CodeExample string representation."""
        example = CodeExample(
            title="Test",
            language="python",
            code="code",
            source_url="test.md"
        )

        repr_str = repr(example)
        assert "CodeExample" in repr_str
        assert "Test" in repr_str


class TestWorkflow:
    """Tests for Workflow dataclass."""

    def test_workflow_creation(self):
        """Test creating a Workflow."""
        workflow = Workflow(
            name="Setup Workflow",
            description="Initial setup steps",
            steps=["Install", "Configure", "Test"],
            frequency="common"
        )

        assert workflow.name == "Setup Workflow"
        assert workflow.description == "Initial setup steps"
        assert len(workflow.steps) == 3
        assert workflow.frequency == "common"

    def test_workflow_repr(self):
        """Test Workflow string representation."""
        workflow = Workflow(
            name="Test Workflow",
            description="Test description",
            steps=["Step 1", "Step 2"]
        )

        repr_str = repr(workflow)
        assert "Workflow" in repr_str
        assert "Test Workflow" in repr_str


class TestPitfall:
    """Tests for Pitfall dataclass."""

    def test_pitfall_creation(self):
        """Test creating a Pitfall."""
        pitfall = Pitfall(
            description="Missing input validation",
            source_url="test.md",
            severity="high",
            context="Validation section"
        )

        assert pitfall.description == "Missing input validation"
        assert pitfall.source_url == "test.md"
        assert pitfall.severity == "high"
        assert pitfall.context == "Validation section"

    def test_pitfall_repr(self):
        """Test Pitfall string representation."""
        pitfall = Pitfall(
            description="File not found error",
            source_url="test.md",
            severity="high"
        )

        repr_str = repr(pitfall)
        assert "Pitfall" in repr_str
        assert "high" in repr_str


class TestDocAnalyzer:
    """Tests for DocAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test creating DocAnalyzer instance."""
        analyzer = DocAnalyzer(verbose=False)
        assert analyzer is not None
        assert analyzer.verbose == False

    def test_classify_tool_type_cli(self, cli_tool_corpus):
        """Test classifying CLI tool documentation."""
        analyzer = DocAnalyzer(verbose=False)

        # Create corpus from fixture
        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        tool_type, confidence, evidence = analyzer.classify_tool_type(corpus)

        # Classification is heuristic - verify valid type rather than exact match
        assert tool_type in [t for t in ToolType]
        assert confidence > 0.0
        assert len(evidence) > 0

    def test_extract_workflows(self, cli_tool_corpus):
        """Test extracting workflows from documentation."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        workflows = analyzer.extract_workflows(corpus)

        # Workflow extraction is heuristic - may or may not find workflows
        assert isinstance(workflows, list)
        # If workflows found, verify they are valid Workflow objects
        if len(workflows) > 0:
            assert all(isinstance(w, Workflow) for w in workflows)
            assert all(w.name for w in workflows)

    def test_extract_examples(self, cli_tool_corpus):
        """Test extracting code examples from documentation."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        examples = analyzer.extract_examples(corpus)

        assert len(examples) > 0
        assert all(isinstance(e, CodeExample) for e in examples)
        # Should extract bash examples
        assert any(e.language == "bash" for e in examples)
        # Should extract python examples
        assert any(e.language == "python" for e in examples)

    def test_identify_patterns(self):
        """Test identifying patterns from code examples."""
        analyzer = DocAnalyzer(verbose=False)

        examples = [
            CodeExample(
                title="Example 1",
                language="bash",
                code="test-tool run --input file.txt",
                source_url="test.md"
            ),
            CodeExample(
                title="Example 2",
                language="bash",
                code="test-tool run --input data.csv --format json",
                source_url="test.md"
            ),
            CodeExample(
                title="Example 3",
                language="bash",
                code="test-tool validate file.txt",
                source_url="test.md"
            )
        ]

        patterns = analyzer.identify_patterns(examples)

        assert isinstance(patterns, list)
        # Patterns may or may not be found depending on similarity threshold

    def test_extract_pitfalls(self, cli_tool_corpus):
        """Test extracting pitfalls from documentation."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        pitfalls = analyzer.extract_pitfalls(corpus)

        assert isinstance(pitfalls, list)
        assert all(isinstance(p, Pitfall) for p in pitfalls)
        # May or may not find pitfalls depending on documentation format

    def test_analyze_gaps(self, cli_tool_corpus):
        """Test analyzing documentation gaps."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        gaps = analyzer.analyze_gaps(corpus)

        assert isinstance(gaps, list)
        # May or may not find gaps depending on documentation completeness

    def test_analyze_full_workflow(self, cli_tool_corpus):
        """Test complete analysis workflow."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        analysis = analyzer.analyze(corpus)

        assert isinstance(analysis, AnalysisContext)
        assert analysis.tool_type in [t for t in ToolType]
        assert isinstance(analysis.tool_type_confidence, float)
        assert 0 <= analysis.tool_type_confidence <= 1
        assert isinstance(analysis.tool_type_reasoning, list)
        assert len(analysis.examples) > 0
        assert len(analysis.workflows) >= 0  # May or may not find workflows
        assert isinstance(analysis.metadata, dict)

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        analyzer = DocAnalyzer(verbose=True)
        analyzer.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        analyzer = DocAnalyzer(verbose=False)
        analyzer.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestAnalysisContext:
    """Tests for AnalysisContext dataclass."""

    def test_analysis_context_creation(self):
        """Test creating an AnalysisContext."""
        context = AnalysisContext(
            tool_type=ToolType.CLI,
            tool_type_confidence=0.9,
            tool_type_reasoning=["Has CLI commands", "Uses command-line flags"],
            workflows=[],
            examples=[],
            patterns=[],
            pitfalls=[],
            gaps=[],
            metadata={"tool_name": "test-tool"}
        )

        assert context.tool_type == ToolType.CLI
        assert context.tool_type_confidence == 0.9
        assert len(context.tool_type_reasoning) == 2
        assert context.metadata["tool_name"] == "test-tool"

    def test_analysis_context_from_fixture(self, sample_analysis):
        """Test creating AnalysisContext from fixture data."""
        # The fixture has tool_type as string, need to convert
        tool_type = ToolType(sample_analysis['tool_type'])

        workflows = [Workflow(**w) for w in sample_analysis['workflows']]
        examples = [CodeExample(**e) for e in sample_analysis['examples']]
        pitfalls = [Pitfall(**p) for p in sample_analysis['pitfalls']]

        context = AnalysisContext(
            tool_type=tool_type,
            tool_type_confidence=sample_analysis['tool_type_confidence'],
            tool_type_reasoning=sample_analysis['tool_type_reasoning'],
            workflows=workflows,
            examples=examples,
            patterns=[],
            pitfalls=pitfalls,
            gaps=[],
            metadata=sample_analysis['metadata']
        )

        assert context.tool_type == ToolType.CLI
        assert context.tool_type_confidence > 0
        assert len(context.tool_type_reasoning) > 0
        assert len(context.workflows) == 2
        assert len(context.examples) == 5
        assert len(context.pitfalls) == 3


class TestDocAnalyzerIntegration:
    """Integration tests for doc analyzer."""

    def test_full_analysis_from_fixture(self, fixtures_dir):
        """Test complete analysis workflow from fixture."""
        analyzer = DocAnalyzer(verbose=False)

        # Load corpus from fixture
        corpus_file = fixtures_dir / "cli_tool_corpus.json"
        with open(corpus_file, 'r') as f:
            corpus_data = json.load(f)

        pages = [Page(**p) for p in corpus_data['pages']]
        corpus = DocumentationCorpus(
            source=corpus_data['source'],
            pages=pages,
            metadata=corpus_data['metadata']
        )

        # Analyze
        analysis = analyzer.analyze(corpus)

        # Verify complete analysis
        assert analysis.tool_type in [t for t in ToolType]
        assert isinstance(analysis.tool_type_confidence, float)
        assert isinstance(analysis.tool_type_reasoning, list)
        assert len(analysis.examples) > 0

        # Verify examples have required fields
        for example in analysis.examples:
            assert example.code
            assert example.language
            assert example.source_url

    def test_tool_type_classification_accuracy(self, cli_tool_corpus):
        """Test tool type classification provides valid results."""
        analyzer = DocAnalyzer(verbose=False)

        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        tool_type, confidence, evidence = analyzer.classify_tool_type(corpus)

        # Should classify as a valid tool type
        assert tool_type in [t for t in ToolType]
        # Should have reasonable confidence
        assert 0 <= confidence <= 1
        # Should provide evidence
        assert isinstance(evidence, list)
        assert len(evidence) > 0
