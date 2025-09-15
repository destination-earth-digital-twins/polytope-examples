import argparse
import base64
import functools
from pathlib import Path

import nbformat
import nbformat.v4

LOGO_NAME = "./docs/images/Logo_Destination_Earth_Colours.png"
MANDATORY_TAGS: dict[str, set[str]] = {"code": {"hide-input"}}
README_PATH = Path("./README.md")


@functools.cache
def get_disclaimer(readme: Path) -> str:
    lines = readme.open()
    disclaimer = ['<div class="alert alert-block alert-warning">']
    for line in lines:
        if line.startswith("> [!WARNING]"):
            for line in lines:
                if line.startswith(">"):
                    disclaimer.append(line.removeprefix(">").strip())
                else:
                    break
    disclaimer.append("</div>")
    return "\n".join(disclaimer)


def add_header(notebook: nbformat.NotebookNode, path: Path) -> None:
    path = path.resolve().relative_to(Path(".").resolve())
    logo_path = "../" * len(path.parent.parts) + LOGO_NAME
    notebook.cells.insert(0, nbformat.v4.new_markdown_cell(f"![logo]({logo_path})"))


def add_tags(cell: nbformat.NotebookNode) -> None:
    tags = set(cell["metadata"].get("tags", []))
    mandatory_tags = MANDATORY_TAGS.get(cell["cell_type"], set())
    cell["metadata"]["tags"] = list(tags | mandatory_tags)


def decode_attachmets(cell: nbformat.NotebookNode, path: Path) -> None:
    attachments = cell.pop("attachments", {})
    for name, data in attachments.items():
        cell["source"] = cell["source"].replace(f"attachment:{name}", f"{name}")
        for encoded in data.values():
            (path.parent / name).write_bytes(base64.b64decode(encoded))


def add_disclaimer(notebook: nbformat.NotebookNode) -> None:
    disclaimer = get_disclaimer(README_PATH)
    cell = nbformat.v4.new_markdown_cell(disclaimer, metadata={"tags": ["disclaimer"]})
    notebook.cells.insert(0, cell)


def edit_section_references(notebook: nbformat.NotebookNode, path: Path) -> None:
    references = {}
    for cell in notebook.cells:
        if "source" not in cell:
            continue

        lines: list[str] = []
        for line in cell["source"].splitlines():
            if line.strip().startswith("(") and line.strip().endswith(")="):
                old_reference = line.strip()[1:-2]
                new_reference = f"{path.stem}:{old_reference}"
                references[old_reference] = new_reference
                line = line.replace(f"({old_reference})=", f"({new_reference})=")
            lines.append(line)
        cell["source"] = "\n".join(lines)

    for cell in notebook.cells:
        if "source" not in cell:
            continue

        for old_reference, new_reference in references.items():
            cell["source"] = cell["source"].replace(
                f"]({old_reference})", f"]({new_reference})"
            )


def convert_notebook(path: Path, disclaimer: bool) -> None:
    notebook = nbformat.read(path, nbformat.NO_CONVERT)

    if disclaimer:
        add_disclaimer(notebook)
    add_header(notebook, path)

    for cell in notebook.cells:
        add_tags(cell)
        decode_attachmets(cell, path)

    edit_section_references(notebook, path)

    nbformat.write(notebook, path)


def main(path: Path, disclaimer: bool) -> None:
    for notebook_path in path.glob("**/*.ipynb"):
        convert_notebook(path=notebook_path, disclaimer=disclaimer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--disclaimer", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    main(path=args.path, disclaimer=args.disclaimer)