# Skill Stylistic Extraction

A reproducible and automated framework for extracting personal coding and writing styles from sample repositories, enabling AI-powered content generation that mimics individual stylistic patterns through LLM API integration.

## Overview

This project represents a first-approach solution to personal style replication using Large Language Models combined with a simplified Retrieval-Augmented Generation workflow. The system analyzes code and writing samples to generate comprehensive style guides that enable AI assistants to produce content matching individual stylistic patterns, reducing manual work while maintaining consistency across generated outputs.

The framework addresses a fundamental challenge in AI-assisted content creation: LLMs lack the ability to inherently replicate personal stylistic nuances without explicit guidance. By extracting and codifying these patterns into machine-readable style guides, the system enables rapid deployment of AI agents that produce outputs aligned with individual preferences for code development, technical writing, or documentation tasks.

## Core Concept

The extraction process leverages Claude's analytical capabilities to identify consistent stylistic patterns independent of subject matter or application context from curated personal samples. These patterns are distilled into prescriptive markdown guides that serve as reference documentation for subsequent AI interactions, either through manual chat-based workflows or automated API-driven processes.

This approach provides immediate practical value for rapid prototyping and experimentation with style-aware AI systems. While output quality may not match human-level refinement or sophisticated RAG implementations, the framework offers substantial time savings and establishes a foundation for iterative improvement. The key advantage lies in reproducibility and automation: users can programmatically generate and deploy style guides that ensure consistent AI behavior across multiple sessions, eliminating the need to repeatedly describe stylistic preferences in each interaction.

## Workflow

### Initial Setup

The extraction process begins with sample curation, where users populate the `code_samples/` or `writing_samples/` directories with representative examples of their work. Samples should reflect authentic personal output with minimal AI assistance to ensure extracted patterns genuinely represent individual style. For code, 10-20 well-written Python files covering diverse functionality provide sufficient material. For writing, academic papers, technical documentation, or professional reports converted to plain text formats serve as appropriate input.

### Automated Extraction

Executing `coding_stylistic_extractor.py` or `writing_stylistic_extractor.py` initiates the extraction pipeline: scans the sample directory, reads file contents, constructs an analysis prompt emphasizing style-over-content focus, submits combined samples to Claude's API, and generates a draft style guide saved to `skill_set/`. The process requires only an Anthropic API key in a `.env` file and executes without manual intervention, producing reproducible results across multiple runs.

### Refinement and Deployment

The generated draft serves as a starting point for iterative refinement through conversational interaction with Claude. Users upload the draft, provide feedback on missing or inaccurate patterns, and improve the guide until it accurately captures their stylistic preferences. The finalized guide can be deployed through Claude Projects (added to project knowledge for automatic application) or programmatic integration (included in system prompts for API-based agents).

## Future Directions

The current framework establishes a foundation for more sophisticated implementations through architectural enhancements and expanded capabilities.

### True RAG Integration

Implementing proper Retrieval-Augmented Generation would enable dynamic pattern retrieval based on current generation context, maintaining a searchable repository of approved samples, retrieving contextually relevant examples in real-time, and continuously updating the knowledge base with validated outputs.

### Agentic Systems

Extending the framework to support autonomous AI agents would enable multi-step generation workflows with iterative refinement, automated testing and validation against style compliance criteria, coordination between specialized agents with different stylistic constraints, and integration with development tools for real-time stylistic feedback.

## Project Structure

```
skill-stylistic-extractor/
├── code_samples/                        # Python files for coding style analysis
├── writing_samples/                     # Text/markdown files for writing style analysis
├── skill_set/                           # Generated style guides
│   ├── coding_stylistic_guide.md
│   └── writing_stylistic_guide.md
├── src/                                 # Source code
│   ├── coding_stylistic_extractor.py    # Code style extraction script
│   └── writing_stylistic_extractor.py   # Writing style extraction script
├── .env                                 # API key configuration (not tracked)
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```
