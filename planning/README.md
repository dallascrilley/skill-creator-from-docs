# Planning

Planning and research documentation for skill creation.

## Structure

```
planning/
├── research-logs/              # Documentation research logs
│   ├── [tool-name]/
│   │   ├── RESEARCH_LOG.md    # Using RESEARCH_LOG_TEMPLATE.md
│   │   └── raw/               # Raw extracted documentation
│   └── README.md
└── README.md                   # This file
```

## Research Logs

Each tool/library/API being analyzed gets its own research log following the template at `templates/RESEARCH_LOG_TEMPLATE.md`.

### Creating a Research Log

```bash
# 1. Create directory for the tool
mkdir -p planning/research-logs/[tool-name]/raw

# 2. Copy template
cp templates/RESEARCH_LOG_TEMPLATE.md planning/research-logs/[tool-name]/RESEARCH_LOG.md

# 3. Fill in as you progress through phases
# Edit planning/research-logs/[tool-name]/RESEARCH_LOG.md
```

### Research Log Purpose

The research log documents:
- Documentation sources and extraction process
- Analysis findings (patterns, examples, gaps)
- Research queries and findings (Perplexity MCP)
- Template synthesis decisions
- Guardrail strategies
- Unresolved items requiring human review

This provides transparency and allows future updates/improvements.
