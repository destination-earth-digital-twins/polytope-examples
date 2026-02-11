import nbformat
import pytest
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
    PROJECT_ROOT / "extremes-dt",
    PROJECT_ROOT / "on-demand-extremes-dt",
    PROJECT_ROOT / "nextgems",
]

SKIP_NOTEBOOKS = {
    PROJECT_ROOT / "climate-dt/climate-dt-train-ai-timeseries-polytope.ipynb",
}


def collect_notebooks():
    notebooks = []
    for root in NOTEBOOK_ROOTS:
        notebooks.extend(root.rglob("*.ipynb"))
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
    if notebook_path in SKIP_NOTEBOOKS:
        pytest.skip("Notebook skipped by configuration")

    monkeypatch.setenv("LIVE_REQUEST", "false")
    execute_notebook(notebook_path)
