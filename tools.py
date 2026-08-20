import os

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "workspace")


def _resolve(path):
    full = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
    if not full.startswith(os.path.abspath(WORKSPACE_DIR)):
        raise ValueError("path escapes workspace directory")
    return full


def list_files(path="."):
    target = _resolve(path)
    return "\n".join(sorted(os.listdir(target))) or "(empty directory)"


def read_file(path):
    with open(_resolve(path)) as f:
        return f.read()


def write_file(path, content):
    target = _resolve(path)
    with open(target, "w") as f:
        f.write(content)
    return f"wrote {len(content)} bytes to {path}"


# Every tool needs two things: a JSON schema the model reads to decide when/how
# to call it, and a plain Python function that actually runs. The schema and
# the function are linked only by the "name" string, so keep them in sync by hand.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a path inside the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path relative to the workspace root. Defaults to '.'.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full contents of a text file inside the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to the workspace root.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file inside the workspace, creating or overwriting it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to the workspace root.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content to write to the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}
