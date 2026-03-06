"""MCP server for managing MkDocs notes."""

import subprocess
from pathlib import Path

import yaml
from mcp.server.fastmcp import FastMCP

PROJECT_DIR = Path(__file__).parent
DOCS_DIR = PROJECT_DIR / "docs"
MKDOCS_YML = PROJECT_DIR / "mkdocs.yml"
VENV_PYTHON = PROJECT_DIR / ".venv" / "bin" / "python"

mcp = FastMCP("notes-server", instructions="Manage MkDocs notes: list, read, create, and update notes and folders.")

def _kill_existing_mkdocs() -> None:
    """Find and kill any running mkdocs serve process."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "mkdocs serve"],
            capture_output=True, text=True
        )
        for pid in result.stdout.strip().split("\n"):
            if pid:
                subprocess.run(["kill", pid], capture_output=True)
    except Exception:
        pass


def _start_mkdocs_server() -> str:
    _kill_existing_mkdocs()
    proc = subprocess.Popen(
        [str(VENV_PYTHON), "-m", "mkdocs", "serve"],
        cwd=str(PROJECT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return f"MkDocs server started (PID: {proc.pid}) at http://127.0.0.1:8000/"


def _restart_mkdocs_server() -> str:
    return _start_mkdocs_server()


def _load_mkdocs_config() -> dict:
    with open(MKDOCS_YML, "r") as f:
        return yaml.safe_load(f)


def _save_mkdocs_config(config: dict) -> None:
    with open(MKDOCS_YML, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _get_folders() -> list[str]:
    return sorted(
        d.name for d in DOCS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def _folder_exists_in_nav(nav: list, folder_title: str) -> bool:
    for item in nav:
        if isinstance(item, dict) and folder_title in item:
            return True
    return False


def _title_from_folder(folder: str) -> str:
    return folder.replace("-", " ").replace("_", " ").title()


def _add_folder_to_nav(config: dict, folder: str, title: str) -> None:
    nav = config.get("nav", [])
    if not _folder_exists_in_nav(nav, title):
        nav.append({title: [f"{folder}/index.md"]})
        config["nav"] = nav


def _add_note_to_nav(config: dict, folder: str, note: str, title: str) -> None:
    nav = config.get("nav", [])
    folder_title = None
    # Find the folder section by matching the folder path prefix
    for item in nav:
        if isinstance(item, dict):
            for key, entries in item.items():
                if isinstance(entries, list):
                    for entry in entries:
                        path = entry if isinstance(entry, str) else list(entry.values())[0] if isinstance(entry, dict) else None
                        if path and path.startswith(f"{folder}/"):
                            folder_title = key
                            break
                if folder_title:
                    break
        if folder_title:
            break

    if folder_title is None:
        return

    note_path = f"{folder}/{note}.md"
    for item in nav:
        if isinstance(item, dict) and folder_title in item:
            entries = item[folder_title]
            # Check if note already in nav
            for entry in entries:
                if isinstance(entry, str) and entry == note_path:
                    return
                if isinstance(entry, dict) and note_path in entry.values():
                    return
            entries.append({title: note_path})
            break


@mcp.tool()
def list_folders() -> str:
    """List all note folders."""
    folders = _get_folders()
    if not folders:
        return "No folders found."
    return "\n".join(f"- {f}" for f in folders)


@mcp.tool()
def list_notes(folder: str) -> str:
    """List all notes in a folder.

    Args:
        folder: Folder name (e.g., 'programming', 'devops')
    """
    folder_path = DOCS_DIR / folder
    if not folder_path.is_dir():
        return f"Error: Folder '{folder}' not found."

    notes = sorted(
        f.stem for f in folder_path.glob("*.md")
        if f.name != "index.md"
    )
    if not notes:
        return f"No notes found in '{folder}'."
    return "\n".join(f"- {n}" for n in notes)


@mcp.tool()
def read_note(folder: str, note: str) -> str:
    """Read the content of a note.

    Args:
        folder: Folder name (e.g., 'programming')
        note: Note name without .md extension (e.g., 'python-basics')
    """
    note_path = DOCS_DIR / folder / f"{note}.md"
    if not note_path.is_file():
        return f"Error: Note '{note}' not found in folder '{folder}'."
    return note_path.read_text()


@mcp.tool()
def update_note(folder: str, note: str, content: str) -> str:
    """Update an existing note's content.

    Args:
        folder: Folder name (e.g., 'programming')
        note: Note name without .md extension (e.g., 'python-basics')
        content: New markdown content for the note
    """
    note_path = DOCS_DIR / folder / f"{note}.md"
    if not note_path.is_file():
        return f"Error: Note '{note}' not found in folder '{folder}'."
    note_path.write_text(content)
    _restart_mkdocs_server()
    return f"Updated note '{note}' in folder '{folder}'."


@mcp.tool()
def create_folder(folder: str, title: str = "") -> str:
    """Create a new empty folder with an index page.

    Args:
        folder: Folder slug (e.g., 'machine-learning')
        title: Display title for the folder (e.g., 'Machine Learning'). Auto-generated from folder name if not provided.
    """
    folder_path = DOCS_DIR / folder
    if folder_path.exists():
        return f"Error: Folder '{folder}' already exists."

    display_title = title or _title_from_folder(folder)

    folder_path.mkdir(parents=True)
    index_path = folder_path / "index.md"
    index_path.write_text(f"# {display_title}\n\nOverview of {display_title} notes.\n")

    config = _load_mkdocs_config()
    _add_folder_to_nav(config, folder, display_title)
    _save_mkdocs_config(config)
    _restart_mkdocs_server()

    return f"Created folder '{folder}' with title '{display_title}'."


@mcp.tool()
def create_note(folder: str, note: str, title: str, content: str) -> str:
    """Create a new note. Auto-creates the folder if it doesn't exist.

    Args:
        folder: Folder slug (e.g., 'programming' or 'machine-learning' for a new folder)
        note: Note slug without .md extension (e.g., 'neural-networks')
        title: Display title for the note (e.g., 'Neural Networks')
        content: Markdown content for the note
    """
    folder_path = DOCS_DIR / folder
    note_path = folder_path / f"{note}.md"

    if note_path.is_file():
        return f"Error: Note '{note}' already exists in folder '{folder}'. Use update_note instead."

    config = _load_mkdocs_config()

    # Create folder if it doesn't exist
    if not folder_path.exists():
        folder_title = _title_from_folder(folder)
        folder_path.mkdir(parents=True)
        index_path = folder_path / "index.md"
        index_path.write_text(f"# {folder_title}\n\nOverview of {folder_title} notes.\n")
        _add_folder_to_nav(config, folder, folder_title)

    note_path.write_text(content)
    _add_note_to_nav(config, folder, note, title)
    _save_mkdocs_config(config)
    _restart_mkdocs_server()

    return f"Created note '{title}' at {folder}/{note}.md"


@mcp.tool()
def mkdocs_server(action: str) -> str:
    """Start, stop, or restart the MkDocs development server.

    Args:
        action: One of 'start', 'stop', or 'restart'
    """
    if action == "start":
        return _start_mkdocs_server()
    elif action == "stop":
        _kill_existing_mkdocs()
        return "MkDocs server stopped."
    elif action == "restart":
        return _restart_mkdocs_server()
    else:
        return f"Error: Unknown action '{action}'. Use 'start', 'stop', or 'restart'."


if __name__ == "__main__":
    mcp.run(transport="stdio")
