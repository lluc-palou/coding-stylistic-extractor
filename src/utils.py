"""
Utility functions for the coding stylistic extractor.
"""

import os
import sys
import anthropic
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Loads environment variables from a .env file
load_dotenv()

class StylisticExtractorUtils:
    """
    A utility class for handling file operations and API interactions.
    """
    def __init__(self, code_repository_path: str, output_file_path: str) -> None:
        self.repo_path = Path(code_repository_path)
        self.output_file = output_file_path
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.current_draft: Optional[str] = None

    def scan_repository(self, max_files: int = 20, extensions: List[str] = None) -> List[Path]:
        """
        Scans the indicated code repository and retrieves a list of code files with specified 
        extensions.
        """
        if extensions is None:
            extensions = [".py"]
            
        code_files= []

        for ext in extensions:
            for filepath in self.repo_path.rglob(f'*{ext}'):
                code_files.append(filepath)

                if len(code_files) >= max_files:
                    break
        
        print(f"Found {len(code_files)} code files in the repository.")
        return code_files
    
    def read_files(self, filepaths: List[Path]) -> List[Dict[str, any]]:
        """
        Reads the content of the provided list of file paths.
        """
        samples = []
        total_lines = 0

        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lines = len(content.splitlines())
                    total_lines += lines
                    samples.append({
                        "path": str(filepath.relative_to(self.repo_path)),
                        "content": content,
                        "lines": lines
                    })

                    print(f"Read {lines} lines from {filepath}")

            except Exception as e:
                print(f"Error reading {filepath.name}: {e}")
        
        print(f"Total: {total_lines} lines of code read from {len(samples)} files.")
        return samples
    
    def extraction(self, code_samples: List[Dict[str, any]]) -> str:
        """
        Performs the initial stylistic extraction from the code samples.
        """
        # Prepares code for LLM processing
        combined_code = "\n\n".join(
            [
                f"### File: {sample['path']}\n```python\n{sample['content']}\n```"
                for sample in code_samples
            ]
        )

        # Coding stylistic extraction prompt declaration
        prompt = f"""I want you to analyze these Python files from my repository and create a comprehensive coding style guide.

These files represent my personal coding style developed over time. Your task is to:

1. **Identify patterns and conventions** across all files
2. **Create a detailed markdown style guide** that captures my distinctive coding style
3. **Include specific examples** from my actual code
4. **Make it prescriptive** so another AI could replicate my style exactly

Analyze these aspects:

**Documentation:**
- Docstring format (Google/NumPy/Sphinx style?)
- What sections do I include? (Args, Returns, Examples, etc.)
- Level of detail in docstrings
- Module-level documentation patterns

**Type Hints:**
- Where and when do I use type annotations?
- Full typing or selective?
- Complex types (Union, Optional, List, Dict patterns)

**Naming Conventions:**
- Variable naming (length, descriptiveness, patterns)
- Function naming (verbs, patterns)
- Class naming
- Constants (if any)
- Private/protected members (underscore usage)

**Code Organization:**
- Import ordering and grouping
- Class structure (method ordering, organization)
- File structure patterns
- Use of __init__.py, __main__.py

**Comments:**
- When do I add comments?
- Inline vs block comments
- Comment style and detail level

**Code Style:**
- Line length preferences
- Indentation patterns
- Blank line usage
- String quotes (single vs double)

**Python Idioms:**
- List/dict comprehensions usage
- Use of decorators
- Context managers
- Generators and iterators
- Exception handling patterns

**Distinctive Patterns:**
- Any unique or characteristic patterns you notice
- Preferred libraries or approaches
- Code complexity preferences

Here are my Python files:

{combined_code}

Create a markdown document with clear sections, examples, and actionable rules.
Format it as a professional style guide that could be given to a coding agent."""

        # Calls LLM API to generate a coding stylistic draft
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Stores the draft and updates the conversation history
        self.current_draft = message.content[0].text
        self.conversation_history.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": self.current_draft
            }
        )

        # Displays statistics
        print(f"\nCoding stylistic draft generated")
        print(f"  Input tokens: {message.usage.input_tokens:,}")
        print(f"  Output tokens: {message.usage.output_tokens:,}")
        print(f"  Total tokens: {message.usage.total_tokens:,}\n")
        
        return self.current_draft
    
    def save_draft(self, content: str = None) -> None:
        """
        Saves the current draft to a file.
        """
        if content is None:
            content = self.current_draft
            
        if content is None:
            print("No content to save!")
            return
            
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved draft to: {self.output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")

def main() -> None:
    """
    Main execution function.
    """
    # Configuration
    MAX_FILES = 20
    OUTPUT_FILE = "coding_stylistic_guide_DRAFT.md"

    print("="*70)
    print("Coding Style Extractor")
    print("="*70)

    # Gets the repository path
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]

    else:
        repo_path = input("\nPath to your code repository: ").strip()
    
    # Validates the repository path
    if not Path(repo_path).exists():
        print(f"\nError: Path does not exist. Check path: {repo_path}")
        return
    
    if not Path(repo_path).is_dir():
        print(f"\nError: Not a directory. Check path: {repo_path}")
        return

    # Initializes the utility class
    extractor_utils = StylisticExtractorUtils(
        code_repository_path=repo_path,
        output_file_path=OUTPUT_FILE
    )

    # Step 1: Scans repository for code files
    code_files = extractor_utils.scan_repository(
        max_files=MAX_FILES,
        extensions=[".py"]
    )

    if not code_files:
        print("\nNo code files of the specified format found in the repository.")
        return
    
    # Step 2: Reads code files
    code_samples = extractor_utils.read_files(code_files)

    if not code_samples:
        print("\nNo code samples could be read from the files.")
        return
    
    # Step 3: Performs the coding stylistic extraction
    draft = extractor_utils.extraction(code_samples)

    # Step 4: Saves the draft
    extractor_utils.save_draft()

    print(f"\nCoding stylistic extraction complete")
    print(f"\nNext steps:")
    print(f"  1. Review the draft: {OUTPUT_FILE}")
    print(f"  2. Upload it to Claude.ai chat")
    print(f"  3. Refine through conversation")
    print(f"  4. Save final version\n")

if __name__ == "__main__":
    main()