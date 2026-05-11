import nbformat
import pytest
import os
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from pathlib import Path


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent

NOTEBOOK_ROOTS = [
    PROJECT_ROOT / "climate-dt",
    # PROJECT_ROOT / "extremes-dt",
    # PROJECT_ROOT / "on-demand-extremes-dt",
    # PROJECT_ROOT / "nextgems",
]

SKIP_NOTEBOOKS = {
    PROJECT_ROOT / "climate-dt/full-field-post-processing/climate-dt-train-ai-timeseries-polytope.ipynb",
}

SKIP_DIRS = {
    PROJECT_ROOT / "climate-dt/explorer",
}

DEBUG_NOTEBOOK_COLLECTION = os.environ.get("DEBUG_NOTEBOOK_COLLECTION", "").lower() in {
    "1",
    "true",
    "yes",
}


def is_in_dir(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def should_skip_notebook(notebook_path: Path) -> bool:
    if notebook_path in SKIP_NOTEBOOKS:
        return True
    return any(is_in_dir(notebook_path, skip_dir) for skip_dir in SKIP_DIRS)


def collect_notebooks():
    notebooks = []
    skipped = []

    for root in NOTEBOOK_ROOTS:
        for notebook_path in root.rglob("*.ipynb"):
            # Only parameterize notebook files that we actually want to execute.
            if notebook_path.suffix != ".ipynb":
                skipped.append((notebook_path, "not-a-notebook"))
                continue
            if notebook_path in SKIP_NOTEBOOKS:
                skipped.append((notebook_path, "skip-notebook"))
                continue
            if any(is_in_dir(notebook_path, skip_dir) for skip_dir in SKIP_DIRS):
                skipped.append((notebook_path, "skip-directory"))
                continue
            notebooks.append(notebook_path)

    if DEBUG_NOTEBOOK_COLLECTION:
        print("\n[notebook-collection] Included notebooks:", len(notebooks))
        print("[notebook-collection] Excluded notebooks:", len(skipped))
        for path, reason in sorted(skipped):
            rel_path = path.relative_to(PROJECT_ROOT)
            print(f"[notebook-collection] EXCLUDE ({reason}): {rel_path}")

    return sorted(notebooks)


def execute_notebook(notebook_path: Path):
    nb = nbformat.read(notebook_path, as_version=4)

    client = NotebookClient(
        nb,
        timeout=600,
        kernel_name="python3",
    )

    try:
        client.execute(cwd=notebook_path.parent)
    except CellExecutionError as e:
        pytest.fail(
            f"""
NOTEBOOK EXECUTION FAILED
Notebook: {notebook_path}

----- Original Traceback -----
{e.traceback}
""",
            pytrace=False,
        )



ALL_NOTEBOOKS = collect_notebooks()


@pytest.mark.parametrize(
    "notebook_path",
    ALL_NOTEBOOKS,
    ids=lambda p: str(p.relative_to(PROJECT_ROOT)),
)
@pytest.mark.timeout(600)
def test_notebook_execution(notebook_path, monkeypatch):
    monkeypatch.setenv("LIVE_REQUEST", "false")
    execute_notebook(notebook_path)
