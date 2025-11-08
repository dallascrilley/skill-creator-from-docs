# Test Tool Documentation

Test Tool is a command-line utility for testing purposes.

## Installation

```bash
pip install test-tool
```

## Quick Start

Basic usage example:

```bash
test-tool run --input data.txt --output results.txt
```

## Commands

### run

Execute the main processing:

```bash
test-tool run [OPTIONS]
```

**Options:**
- `--input FILE` - Input file path (required)
- `--output FILE` - Output file path (default: stdout)
- `--verbose` - Enable verbose logging
- `--format FORMAT` - Output format: json, csv, text (default: text)

**Example:**

```bash
# Process with JSON output
test-tool run --input data.txt --output results.json --format json
```

### validate

Validate input file:

```bash
test-tool validate FILE
```

**Example:**

```bash
test-tool validate data.txt
```

## Common Workflows

### 1. Basic Processing

1. Prepare your input file
2. Run the tool: `test-tool run --input data.txt`
3. Check output in results

### 2. Batch Processing

For multiple files:

```bash
for file in *.txt; do
  test-tool run --input "$file" --output "${file%.txt}.json" --format json
done
```

## Common Pitfalls

### Missing Input File

**Problem:** File not found error

**Solution:** Ensure the input file path is correct and the file exists.

```bash
# Bad
test-tool run --input nonexistent.txt

# Good
test-tool run --input $(pwd)/data.txt
```

### Invalid Format

**Problem:** Output format not supported

**Solution:** Use one of: json, csv, text

### Permission Issues

**Problem:** Cannot write to output file

**Solution:** Check file permissions or use a different output location

## Configuration

Create a config file at `~/.test-tool/config.yaml`:

```yaml
default_format: json
verbose: false
output_dir: ./results
```

## API

For programmatic usage:

```python
from test_tool import TestTool

tool = TestTool()
result = tool.run(input_file="data.txt", format="json")
print(result)
```

## Troubleshooting

**Q: Tool runs slow**
A: Use `--format text` for faster processing

**Q: Output is empty**
A: Check input file encoding (must be UTF-8)

**Q: Command not found**
A: Ensure test-tool is in your PATH after installation
