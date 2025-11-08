#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures for skill-creator-from-docs tests.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

import pytest

# Add scripts directory to Python path
REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def cli_tool_corpus(fixtures_dir: Path) -> Dict[str, Any]:
    """Load CLI tool documentation corpus fixture."""
    corpus_file = fixtures_dir / "cli_tool_corpus.json"
    with open(corpus_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def api_docs_corpus(fixtures_dir: Path) -> Dict[str, Any]:
    """Load API documentation corpus fixture."""
    corpus_file = fixtures_dir / "api_docs_corpus.json"
    with open(corpus_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def library_docs_corpus(fixtures_dir: Path) -> Dict[str, Any]:
    """Load library documentation corpus fixture."""
    corpus_file = fixtures_dir / "library_docs_corpus.json"
    with open(corpus_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def framework_docs_corpus(fixtures_dir: Path) -> Dict[str, Any]:
    """Load framework documentation corpus fixture."""
    corpus_file = fixtures_dir / "framework_docs_corpus.json"
    with open(corpus_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def sample_analysis(fixtures_dir: Path) -> Dict[str, Any]:
    """Load sample analysis result fixture."""
    analysis_file = fixtures_dir / "sample_analysis.json"
    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def sample_templates(fixtures_dir: Path) -> Dict[str, Any]:
    """Load sample templates metadata fixture."""
    templates_file = fixtures_dir / "sample_templates.json"
    with open(templates_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def sample_guardrails(fixtures_dir: Path) -> Dict[str, Any]:
    """Load sample guardrails metadata fixture."""
    guardrails_file = fixtures_dir / "sample_guardrails.json"
    with open(guardrails_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Create temporary output directory for tests."""
    output_dir = tmp_path / "test_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def sample_markdown_doc(fixtures_dir: Path) -> str:
    """Load sample markdown documentation."""
    doc_file = fixtures_dir / "sample_docs.md"
    return doc_file.read_text(encoding='utf-8')
