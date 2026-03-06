# AI Notes Assistant

A private, local-first notes management system powered by AI. Combines [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for beautiful documentation rendering with an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that lets AI assistants like Claude read, create, and manage your notes through natural conversation.

**Talk to your notes. Ask Claude to create a new topic, update existing content, or organize your knowledge base — all through natural language.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![MCP](https://img.shields.io/badge/MCP-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Why AI Notes Assistant?

- **Private & Local** — Your notes stay on your machine. No cloud sync, no third-party access.
- **AI-Powered** — Create, read, and update notes through natural conversation with Claude.
- **Beautiful UI** — MkDocs Material renders your markdown notes as a searchable, navigable website.
- **Auto-Managed** — The MCP server handles folder creation, navigation updates, and server restarts automatically.
- **Open Format** — Notes are plain markdown files. No vendor lock-in, works with any editor.

## How It Works

```
You (natural language) → Claude (AI) → MCP Server → Markdown Files → MkDocs (rendered site)
                                            ↓
                                      mkdocs.yml (auto-updated navigation)
```

1. You tell Claude what you want: *"Create a note about Kubernetes in the DevOps folder"*
2. Claude calls the MCP server tools to create the file and update navigation
3. MkDocs automatically rebuilds and serves the updated site
4. You browse your notes at `http://localhost:8000`

## Features

| Feature | Description |
|---------|-------------|
| **List folders** | See all topic categories |
| **List notes** | Browse notes within any folder |
| **Read notes** | View full note content |
| **Create notes** | Add new notes to existing or new folders |
| **Create folders** | Add new topic categories |
| **Update notes** | Modify existing note content |
| **Server control** | Start, stop, or restart the MkDocs dev server |
| **Auto-restart** | MkDocs server auto-restarts after every write operation |
| **Nav sync** | `mkdocs.yml` navigation is automatically updated |

## Project Structure

```
ai-notes-assistant/
├── README.md
├── mkdocs.yml                 # MkDocs configuration & navigation
├── mcp_notes_server.py        # MCP server (the AI bridge)
├── .mcp.json                  # Claude Code MCP config
└── docs/                      # Your notes (markdown files)
    ├── index.md               # Homepage
    ├── programming/
    │   ├── index.md
    │   ├── python-basics.md
    │   └── javascript-tips.md
    ├── devops/
    │   ├── index.md
    │   ├── docker-guide.md
    │   └── ci-cd-pipeline.md
    ├── database/
    │   ├── index.md
    │   ├── sql-fundamentals.md
    │   └── nosql-concepts.md
    └── cloud/
        ├── index.md
        ├── aws-services.md
        └── azure-basics.md
```

## Setup from Scratch

### Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip
- **Claude Desktop** or **Claude Code** (for AI integration)

### 1. Clone the Repository

```bash
git clone https://github.com/DevOpsAIguru123/notes-agent.git
cd notes-agent
```

### 2. Create Virtual Environment & Install Dependencies

Using **uv** (recommended):

```bash
uv venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

uv pip install mkdocs mkdocs-material "mcp[cli]"
```

Using **pip**:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

pip install mkdocs mkdocs-material "mcp[cli]"
```

### 3. Verify the Setup

Start the MkDocs dev server:

```bash
mkdocs serve
```

Open http://localhost:8000 in your browser. You should see the notes site with collapsible folder navigation.

### 4. Connect to Claude

Choose **one** of the following based on your setup:

---

#### Option A: Claude Code (CLI)

The `.mcp.json` file in the project root is auto-detected. Just update the paths:

```json
{
  "mcpServers": {
    "notes": {
      "command": "/path/to/ai-notes-assistant/.venv/bin/python",
      "args": ["/path/to/ai-notes-assistant/mcp_notes_server.py"]
    }
  }
}
```

Then start Claude Code from the project directory:

```bash
cd ai-notes-assistant
claude
```

The notes tools will be available immediately.

---

#### Option B: Claude Desktop (GUI)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "notes": {
      "command": "/path/to/ai-notes-assistant/.venv/bin/python",
      "args": ["/path/to/ai-notes-assistant/mcp_notes_server.py"]
    }
  }
}
```

Restart Claude Desktop to load the server.

---

### 5. Test the Connection

Ask Claude:

> "List all my note folders"

You should see the folders listed. Then try:

> "Create a note about Redis caching in the database folder"

The note will be created, navigation updated, and MkDocs restarted automatically.

## MCP Tools Reference

### `list_folders`

List all note folders.

```
No parameters required.
```

### `list_notes`

List all notes in a folder.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `folder` | string | Yes | Folder name (e.g., `programming`) |

### `read_note`

Read the content of a note.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `folder` | string | Yes | Folder name |
| `note` | string | Yes | Note slug without `.md` (e.g., `python-basics`) |

### `update_note`

Update an existing note's content.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `folder` | string | Yes | Folder name |
| `note` | string | Yes | Note slug without `.md` |
| `content` | string | Yes | New markdown content |

### `create_note`

Create a new note. Auto-creates the folder if it doesn't exist.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `folder` | string | Yes | Folder slug (e.g., `machine-learning`) |
| `note` | string | Yes | Note slug (e.g., `neural-networks`) |
| `title` | string | Yes | Display title (e.g., `Neural Networks`) |
| `content` | string | Yes | Markdown content |

### `create_folder`

Create a new empty folder with an index page.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `folder` | string | Yes | Folder slug |
| `title` | string | No | Display title (auto-generated if omitted) |

### `mkdocs_server`

Start, stop, or restart the MkDocs development server.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | Yes | One of `start`, `stop`, or `restart` |

## Usage Examples

### Natural Language (through Claude)

```
"List all my note folders"
"Show me the notes in the programming folder"
"Read my Python basics note"
"Update the Docker guide with a section about volumes"
"Create a new folder called machine-learning"
"Create a note about transformers in the machine-learning folder"
"Restart the docs server"
```

### Manual Editing

You can also edit notes directly with any text editor. The files are plain markdown in the `docs/` directory. After editing, the MkDocs dev server auto-reloads on file changes.

To add a new note manually:

1. Create the `.md` file in the appropriate `docs/` subfolder
2. Add the entry to `mkdocs.yml` under the `nav` section
3. The dev server will pick up the changes

## Customization

### Changing the Theme

Edit `mkdocs.yml` to customize colors:

```yaml
theme:
  name: material
  palette:
    scheme: slate        # dark mode
    primary: teal
    accent: amber
```

See [Material for MkDocs theming docs](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/) for all options.

### Adding Search

Search is enabled by default. The `search.suggest` feature provides search-as-you-type suggestions in the header bar.

### Adding More Markdown Features

Add extensions to `mkdocs.yml`:

```yaml
markdown_extensions:
  - toc:
      permalink: true
  - admonition            # callout boxes (tip, warning, etc.)
  - pymdownx.highlight    # code syntax highlighting
  - pymdownx.superfences  # fenced code blocks
  - pymdownx.tasklist:    # checkbox task lists
      custom_checkbox: true
  - pymdownx.tabbed:      # tabbed content blocks
      alternate_style: true
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Claude (AI)                    │
│         Natural language understanding           │
└─────────────────┬───────────────────────────────┘
                  │ MCP Protocol (stdio)
┌─────────────────▼───────────────────────────────┐
│             mcp_notes_server.py                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ list_*   │ │ create_* │ │ mkdocs_server    │ │
│  │ read_*   │ │ update_* │ │ (start/stop)     │ │
│  └────┬─────┘ └────┬─────┘ └────────┬─────────┘ │
└───────┼─────────────┼────────────────┼───────────┘
        │             │                │
   ┌────▼─────┐  ┌────▼──────┐  ┌─────▼──────┐
   │ docs/    │  │mkdocs.yml │  │ mkdocs     │
   │ *.md     │  │ (nav)     │  │ serve      │
   └──────────┘  └───────────┘  └─────┬──────┘
                                      │
                              ┌───────▼───────┐
                              │ localhost:8000 │
                              │ (your browser) │
                              └───────────────┘
```

## Troubleshooting

### MCP server not showing up in Claude

- **Claude Code**: Make sure `.mcp.json` is in the project root and paths are absolute. Restart Claude Code.
- **Claude Desktop**: Check `claude_desktop_config.json` paths. Restart Claude Desktop.

### MkDocs server not starting

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
kill $(lsof -ti :8000)

# Start manually
source .venv/bin/activate
mkdocs serve
```

### Notes not updating in browser

The MCP server auto-restarts MkDocs after every write. If you edit files manually, either:
- Refresh the browser (MkDocs live-reload should handle it)
- Ask Claude: *"Restart the docs server"*

### Navigation not showing new pages

The MCP server auto-updates `mkdocs.yml` when creating notes/folders. If you add files manually, you need to add them to the `nav` section in `mkdocs.yml`.

## Contributing

Contributions are welcome! Here are some ideas:

- **Search tool** — Add a tool to search across all notes
- **Delete support** — Add tools to delete notes and folders
- **Tags/metadata** — Support frontmatter tags for better organization
- **Export** — Export notes as PDF or static site
- **Windows support** — Adapt process management for Windows

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and [Model Context Protocol](https://modelcontextprotocol.io/).
