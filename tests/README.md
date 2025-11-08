# Tests

Test suite for skill-creator-from-docs.

## Structure

```
tests/
├── test_doc_extractor.py      # Test documentation extraction
├── test_doc_analyzer.py        # Test analysis functions
├── test_template_synthesizer.py # Test template generation
├── test_guardrail_generator.py # Test guardrail creation
├── test_integration.py         # End-to-end tests
└── fixtures/                   # Test data
    ├── sample_cli_docs.md
    ├── sample_api_docs.md
    └── sample_library_docs.md
```

## Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_doc_extractor.py

# With coverage
pytest --cov=scripts tests/

# Verbose
pytest -v tests/
```

## Test Categories

### Unit Tests
Test individual components in isolation.

### Integration Tests
Test complete workflows from docs to generated skill.

### Fixtures
Sample documentation for testing various tool types.

## Adding Tests

1. Create test file in `tests/`
2. Use fixtures from `fixtures/` directory
3. Follow naming convention: `test_<component>.py`
4. Include docstrings describing what's tested

## Requirements

```bash
pip install pytest pytest-cov
```
