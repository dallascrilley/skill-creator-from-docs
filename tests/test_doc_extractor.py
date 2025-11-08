#!/usr/bin/env python3
"""
Unit tests for doc_extractor.py
"""

import json
from pathlib import Path

import pytest

from doc_extractor import (
    DocExtractor,
    DocumentationCorpus,
    Page
)


class TestPage:
    """Tests for Page dataclass."""

    def test_page_creation(self):
        """Test creating a Page with required fields."""
        page = Page(
            url="https://example.com/doc",
            title="Test Doc",
            content="# Test\n\nContent here",
            metadata={"type": "documentation"}
        )

        assert page.content == "# Test\n\nContent here"
        assert page.url == "https://example.com/doc"
        assert page.title == "Test Doc"
        assert page.metadata["type"] == "documentation"

    def test_page_repr(self):
        """Test Page string representation."""
        page = Page(
            url="https://example.com",
            title="Test Page",
            content="Test content"
        )

        repr_str = repr(page)
        assert "Page" in repr_str
        assert "Test Page" in repr_str
        assert "https://example.com" in repr_str


class TestDocumentationCorpus:
    """Tests for DocumentationCorpus dataclass."""

    def test_corpus_creation(self):
        """Test creating a DocumentationCorpus."""
        pages = [
            Page(url="url1", title="Page 1", content="Content 1"),
            Page(url="url2", title="Page 2", content="Content 2")
        ]

        corpus = DocumentationCorpus(
            source="test_source",
            pages=pages,
            metadata={"count": 2}
        )

        assert corpus.source == "test_source"
        assert len(corpus.pages) == 2
        assert corpus.metadata["count"] == 2

    def test_total_content_length(self):
        """Test calculating total content length."""
        pages = [
            Page(url="url1", title="P1", content="12345"),
            Page(url="url2", title="P2", content="1234567890")
        ]

        corpus = DocumentationCorpus(
            source="test",
            pages=pages
        )

        assert corpus.total_content_length() == 15

    def test_get_page_by_url(self):
        """Test retrieving page by URL."""
        pages = [
            Page(url="url1", title="Page 1", content="Content 1"),
            Page(url="url2", title="Page 2", content="Content 2")
        ]

        corpus = DocumentationCorpus(source="test", pages=pages)

        page = corpus.get_page_by_url("url2")
        assert page is not None
        assert page.content == "Content 2"

        # Test non-existent URL
        assert corpus.get_page_by_url("url3") is None


class TestDocExtractor:
    """Tests for DocExtractor class."""

    def test_extractor_initialization(self):
        """Test creating DocExtractor instance."""
        extractor = DocExtractor(verbose=False)
        assert extractor is not None
        assert extractor.verbose == False

        extractor_verbose = DocExtractor(verbose=True)
        assert extractor_verbose.verbose == True

    def test_extract_from_markdown(self, sample_markdown_doc, fixtures_dir):
        """Test extracting from markdown file."""
        extractor = DocExtractor(verbose=False)

        # Use fixture file
        markdown_file = fixtures_dir / "sample_docs.md"

        corpus = extractor.extract_from_markdown(str(markdown_file))

        assert corpus is not None
        assert isinstance(corpus, DocumentationCorpus)
        assert len(corpus.pages) == 1
        assert "Test Tool" in corpus.pages[0].content
        assert corpus.source == str(markdown_file)

    def test_extract_markdown_file(self, fixtures_dir):
        """Test extracting single markdown file."""
        extractor = DocExtractor(verbose=False)
        markdown_file = fixtures_dir / "sample_docs.md"

        page = extractor._extract_markdown_file(markdown_file)

        assert page is not None
        assert isinstance(page, Page)
        assert "Test Tool" in page.content
        # URL is formatted as file:// URL
        assert str(markdown_file) in page.url or page.url.endswith("sample_docs.md")
        assert page.title  # Has a title

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test normal name (dots are replaced)
        assert DocExtractor._sanitize_filename("normal_file") == "normal_file"

        # Test with special characters
        assert DocExtractor._sanitize_filename("file/with\\special:chars") == "file_with_special_chars"

        # Test with spaces (collapsed to single underscore)
        assert DocExtractor._sanitize_filename("file with spaces") == "file_with_spaces"

        # Test with multiple special chars
        assert DocExtractor._sanitize_filename("file<>|?*") == "file_____"

        # Test with dots (dots are replaced with underscores)
        assert DocExtractor._sanitize_filename("file.name.txt") == "file_name_txt"

    def test_save_raw_docs_json(self, temp_output_dir, cli_tool_corpus):
        """Test saving corpus to JSON format."""
        extractor = DocExtractor(verbose=False)

        # Create corpus from fixture
        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        # Save to JSON
        extractor.save_raw_docs(corpus, str(temp_output_dir), format='json')

        # Verify files created
        corpus_file = temp_output_dir / "corpus.json"
        assert corpus_file.exists()

        # Verify content
        with open(corpus_file, 'r') as f:
            saved_data = json.load(f)

        assert saved_data['source'] == corpus.source
        assert len(saved_data['pages']) == len(corpus.pages)

    def test_save_raw_docs_markdown(self, temp_output_dir, cli_tool_corpus):
        """Test saving corpus to markdown files."""
        extractor = DocExtractor(verbose=False)

        # Create corpus from fixture
        pages = [Page(**p) for p in cli_tool_corpus['pages']]
        corpus = DocumentationCorpus(
            source=cli_tool_corpus['source'],
            pages=pages,
            metadata=cli_tool_corpus['metadata']
        )

        # Save to markdown
        extractor.save_raw_docs(corpus, str(temp_output_dir), format='markdown')

        # Verify files created
        page_files = list(temp_output_dir.glob("page_*.md"))
        assert len(page_files) == len(corpus.pages)

        # Verify metadata file
        metadata_file = temp_output_dir / "_metadata.json"
        assert metadata_file.exists()

    def test_extract_nonexistent_file(self):
        """Test extracting from nonexistent file."""
        extractor = DocExtractor(verbose=False)

        with pytest.raises(Exception):
            extractor.extract_from_markdown("/nonexistent/file.md")

    def test_log_verbose(self, capsys):
        """Test logging with verbose mode."""
        extractor = DocExtractor(verbose=True)
        extractor.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err

    def test_log_quiet(self, capsys):
        """Test logging with quiet mode."""
        extractor = DocExtractor(verbose=False)
        extractor.log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err


class TestDocExtractorIntegration:
    """Integration tests for doc extractor workflow."""

    def test_full_extraction_workflow(self, fixtures_dir, temp_output_dir):
        """Test complete extraction workflow from file to saved output."""
        extractor = DocExtractor(verbose=False)

        # Extract
        markdown_file = fixtures_dir / "sample_docs.md"
        corpus = extractor.extract_from_markdown(str(markdown_file))

        # Verify extraction
        assert len(corpus.pages) > 0
        assert corpus.total_content_length() > 0

        # Save
        extractor.save_raw_docs(corpus, str(temp_output_dir), format='json')

        # Verify saved file can be loaded
        corpus_file = temp_output_dir / "corpus.json"
        with open(corpus_file, 'r') as f:
            saved_data = json.load(f)

        assert saved_data['source'] == str(markdown_file)
        assert len(saved_data['pages']) == len(corpus.pages)
