import subprocess
import re


def run_benchmarks():
    # Run benchmarks.py and capture its output
    result = subprocess.run(
        ["python", "tests/benchmarks.py"], capture_output=True, text=True
    )
    return result.stdout


def update_readme(benchmarks_markdown):
    # Read the current README.md content
    with open("README.md", "r", encoding="utf-8") as file:
        readme_contents = file.read()

    # Define a pattern to find the Benchmarks section
    # Adjust the pattern as necessary to match your README's structure
    pattern = r"(## Benchmarks\n)(.*?)(\n## )"
    replacement = r"\1" + benchmarks_markdown + r"\3"

    # Replace the Benchmarks section with the new benchmarks
    updated_readme = re.sub(pattern, replacement, readme_contents, flags=re.DOTALL)

    # Write the updated README back to disk
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)


if __name__ == "__main__":
    benchmarks_markdown = run_benchmarks()
    update_readme(benchmarks_markdown)
