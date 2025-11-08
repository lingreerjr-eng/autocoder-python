#!/usr/bin/env python3
"""
autocoder.py — Autonomous multi-file coding agent (Ollama) with:
- Preflight pip installs + auto-install missing imports
- Visual Studio Code handoff (open/focus + live edits)
- Scriptable CLI Agents (single agent, fleets, delegation, IDE<->CLI handoff)
- Minimal MCP-style integration (databases/APIs/docs via YAML connectors)
- Exec runner with colored streaming output and basic Python error surfacing

Quick examples
--------------
Create + open in VS Code + auto-fix:
  python autocoder.py new "FastAPI app with /health and /sum" \
    --dir projects/api --model codellama --entry main.py --max-iters 8 --vscode

Extend later (edits files, reinstalls requirements if changed), keep VS Code open:
  python autocoder.py edit --dir projects/api "Add /multiply and unit tests" --vscode

Run once (no LLM), stream output:
  python autocoder.py run --dir projects/api

Agent run (scriptable):
  python autocoder.py agent run --dir projects/api --name builder \
    --goal "Add pagination to /items and write tests"

Fleet run (parallel agents):
  python autocoder.py fleet run --dir projects/api plan.json

Delegate sub-task between agents:
  python autocoder.py delegate --dir projects/api --from builder --to fixer \
    --context "Tests failing on Windows paths"

MCP call (connectors in mcp_config.yaml):
  python autocoder.py mcp call --dir projects/api --tool db.users.count
  python autocoder.py mcp call --dir projects/api --tool http.get.github /repos/owner/repo

Execute shell in project (stream output; stderr is red):
  python autocoder.py exec --dir projects/api "pytest -q"

Build an .exe (Windows):
  pip install pyinstaller
  pyinstaller --onefile autocoder.py
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import textwrap
import threading
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ----------------------------
# Config
# ----------------------------
DEFAULT_MODEL = "qwen3-coder:480b-cloud"
DEFAULT_ENTRY = "main.py"
MANIFEST_NAME = ".autocoder_manifest.json"
MAX_SNAPSHOT_BYTES = 200_000
AUTO_PIP_DEFAULT = True
MCP_CONFIG_FILE = "mcp_config.yaml"  # optional; per-project

# ANSI Colors
ANSI_RESET = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_BLUE = "\033[34m"
ANSI_YELLOW = "\033[33m"
ANSI_DIM = "\033[2m"

# ----------------------------
# Ollama helpers
# ----------------------------
def ollama_run(model: str, prompt: str) -> str:
    proc = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Ollama error: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout

# ----------------------------
# Pip helpers
# ----------------------------
def pip_install_packages(pkgs: List[str]) -> bool:
    pkgs = [p.strip() for p in pkgs if p and p.strip()]
    if not pkgs:
        return True
    print(f"{ANSI_BLUE}[+] pip install {' '.join(pkgs)}{ANSI_RESET}")
    proc = subprocess.run([sys.executable, "-m", "pip", "install", *pkgs])
    return proc.returncode == 0

def pip_install_requirements(requirements_path: Path) -> bool:
    if not requirements_path.exists():
        return True
    print(f"{ANSI_BLUE}[+] pip install -r {requirements_path}{ANSI_RESET}")
    proc = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
    return proc.returncode == 0

_MISSING_IMPORT_RE = re.compile(r"ModuleNotFoundError:\s+No module named '([^']+)'")
_IMPORT_ERROR_RE = re.compile(r"ImportError:\s+No module named '([^']+)'")

def maybe_install_missing_from_error(stderr_or_stdout: str, auto_pip: bool) -> Optional[str]:
    if not auto_pip:
        return None
    for rx in (_MISSING_IMPORT_RE, _IMPORT_ERROR_RE):
        m = rx.search(stderr_or_stdout)
        if m:
            mod = m.group(1)
            candidate = mod.replace("_", "-")
            print(f"{ANSI_BLUE}[+] Missing module '{mod}' → trying pip install {candidate}{ANSI_RESET}")
            ok = pip_install_packages([candidate])
            return candidate if ok else None
    return None

# ----------------------------
# Project helpers
# ----------------------------
def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_file(root: Path, relpath: str, content: str):
    rel = Path(relpath).as_posix().lstrip("/")
    outpath = (root / rel).resolve()
    root_abs = root.resolve()
    if not str(outpath).startswith(str(root_abs)):
        raise ValueError(f"Refusing to write outside project: {outpath}")
    ensure_dir(outpath.parent)
    outpath.write_text(content, encoding="utf-8")

def read_file(root: Path, relpath: str) -> str:
    p = (root / relpath).resolve()
    return p.read_text(encoding="utf-8")

def discover_files(root: Path) -> List[str]:
    files = []
    for p in root.rglob("*"):
        if p.is_file() and p.name != MANIFEST_NAME:
            files.append(str(p.relative_to(root).as_posix()))
    return sorted(files)

def load_manifest(root: Path) -> Dict:
    p = root / MANIFEST_NAME
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_manifest(root: Path, manifest: Dict):
    (root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")

def snapshot_project(root: Path, truncate_bytes: int = MAX_SNAPSHOT_BYTES) -> str:
    files = discover_files(root)
    parts = []
    parts.append("PROJECT TREE:\n" + "\n".join(files) + "\n")
    parts.append("FILES:\n")
    total = 0
    for f in files:
        try:
            content = read_file(root, f)
        except Exception as e:
            content = f"<<unable to read: {e}>>"
        block = f"\n===== {f} =====\n{content}\n"
        total += len(block.encode("utf-8"))
        if total > truncate_bytes:
            parts.append("\n<<SNAPSHOT TRUNCATED>>\n")
            break
        parts.append(block)
    return "".join(parts)

# ----------------------------
# LLM output parsing
# ----------------------------
def try_parse_json_manifest(text: str) -> Tuple[str, List[Dict], List[str]]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.split("\n", 1)[1] if "\n" in text else text
    data = json.loads(text)
    entry = data.get("entrypoint", "")
    files = data.get("files", [])
    delete = data.get("delete", [])
    if not isinstance(files, list):
        raise ValueError("files must be a list")
    return entry, files, delete

FENCE_RE = re.compile(
    r"```(?:(?:\w+)\s*)?(?:filename\s*=\s*)?([^\n`]+?)\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE
)

def parse_code_fences(text: str) -> List[Dict]:
    results = []
    for m in FENCE_RE.finditer(text):
        filename = m.group(1).strip()
        content = m.group(2).strip()
        results.append({"path": filename, "content": content})
    return results

def parse_llm_files(text: str) -> Tuple[str, List[Dict], List[str]]:
    try:
        entry, files, delete = try_parse_json_manifest(text)
        return entry, files, delete
    except Exception:
        pass
    files = parse_code_fences(text)
    entry = ""
    candidates = [f["path"] for f in files if f["path"].endswith((".py", ".sh", ".bat"))]
    if candidates:
        entry = "main.py" if "main.py" in {Path(c).name for c in candidates} else candidates[0]
    return entry, files, []

# ----------------------------
# Prompts
# ----------------------------
DEP_PLAN_PROMPT = """You are a build planner.
From the TASK below, output ONLY a compact JSON object with a single key "packages"
listing the minimal pip packages (names as they would be installed via pip) required to implement it.
Do not include stdlib modules. Do not include dev tools.

TASK:
{task}
"""

CREATE_PROMPT = """You are a senior software engineer generating a COMPLETE multi-file project.

TASK:
{task}

OUTPUT FORMAT (STRICT):
Return a single JSON object with keys:
- "entrypoint": string (e.g., "main.py" or "src/app.py")
- "files": a list of objects with fields:
    - "path": string (relative path)
    - "content": string (entire file content)
Do NOT include any commentary. Do NOT use backticks. Do NOT abbreviate code.

QUALITY RULES:
- Provide all files required to run immediately (requirements.txt if needed).
- Keep paths POSIX-like (use forward slashes).
- Ensure imports match the provided file paths.
"""

FIX_PROMPT = """You are a repair agent. The current project fails to run.

RUNTIME ERROR (stderr/stdout):
{error}

CURRENT PROJECT SNAPSHOT (trimmed):
{snapshot}

REQUIREMENT:
Return ONLY a JSON object with:
- "files": a list of modified or new files (path+content) that will fix the error.
- "delete": optional list of file paths to remove (if necessary).
Do NOT include backticks or commentary.
Ensure the project then runs with the same entrypoint: {entry}.
"""

EDIT_PROMPT = """You are an editor improving an existing multi-file project.

USER REQUEST:
{instruction}

CURRENT PROJECT SNAPSHOT (trimmed):
{snapshot}

REQUIREMENT:
Return ONLY a JSON object with:
- "files": list of modified and/or new files (path+content).
- "delete": optional list of file paths to remove.
Do NOT include backticks or commentary.
Preserve existing structure unless change is needed.
"""

AGENT_PROMPT = """You are an autonomous coding agent working inside an existing project.

GOAL:
{goal}

CONTEXT (trimmed project snapshot):
{snapshot}

REQUIREMENTS:
- Modify or add only the necessary files.
- Respect current layout and imports.
- Return ONLY a JSON object with "files" and optional "delete".
"""

# ----------------------------
# VS Code integration (IDE handoff)
# ----------------------------
def vscode_available() -> bool:
    try:
        subprocess.run(["code", "-v"], capture_output=True, text=True)
        return True
    except Exception:
        return False

def open_in_vscode(root: Path):
    if vscode_available():
        # -r reuse window; open folder
        subprocess.Popen(["code", "-r", str(root)])
        print(f"{ANSI_GREEN}[+] Opened in VS Code: {root}{ANSI_RESET}")
    else:
        print(f"{ANSI_YELLOW}[!] VS Code 'code' CLI not found in PATH. Skipping IDE handoff.{ANSI_RESET}")

def write_handoff_note(root: Path, title: str, body: str):
    note = root / ".autocoder_handoff.md"
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    content = f"# {title}\n\nTime: {ts}\n\n{body}\n"
    try:
        with open(note, "a", encoding="utf-8") as f:
            f.write(content + "\n")
    except Exception:
        pass

# ----------------------------
# Materialization / Run / Fix
# ----------------------------
def materialize_files(root: Path, files: List[Dict], delete: List[str]):
    # Deletes first
    for d in delete or []:
        p = (root / d).resolve()
        if p.exists():
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                for sub in sorted(p.rglob("*"), reverse=True):
                    if sub.is_file(): sub.unlink()
                    else: sub.rmdir()
                p.rmdir()
    # Write/overwrite
    for f in files:
        path = f["path"]
        content = f.get("content", "")
        write_file(root, path, content)

def run_project(root: Path, entry: str) -> Tuple[int, str, str]:
    entry_path = (root / entry).resolve()
    if not entry_path.exists():
        return 127, "", f"Entrypoint not found: {entry}"
    proc = subprocess.run(
        [sys.executable, str(entry_path)],
        text=True,
        capture_output=True,
        cwd=str(root)
    )
    return proc.returncode, proc.stdout, proc.stderr

def fix_loop(model: str, root: Path, entry: str, max_iters: int, auto_pip: bool) -> bool:
    for i in range(1, max_iters + 1):
        code, out, err = run_project(root, entry)
        if code == 0:
            print(f"{ANSI_GREEN}[+] Run OK (iteration {i}){ANSI_RESET}")
            if out.strip():
                print(out)
            return True

        combined = (err or "") + "\n" + (out or "")
        installed = maybe_install_missing_from_error(combined, auto_pip)
        if installed:
            print(f"{ANSI_BLUE}[+] Installed '{installed}', retrying...{ANSI_RESET}")
            continue

        print(f"{ANSI_YELLOW}[!] Failure (iteration {i}) — attempting LLM fix{ANSI_RESET}")
        snapshot = snapshot_project(root)
        resp = ollama_run(model, FIX_PROMPT.format(error=combined, snapshot=snapshot, entry=entry))
        _, files, delete = parse_llm_files(resp)
        if not files and not delete:
            print(f"{ANSI_RED}[!] LLM provided no changes; stopping.{ANSI_RESET}")
            return False
        materialize_files(root, files, delete)
    print(f"{ANSI_RED}[!] Reached max fix iterations; still failing.{ANSI_RESET}")
    return False

# ----------------------------
# Dependency preflight
# ----------------------------
def dependency_preflight(model: str, task: str, auto_pip: bool):
    if not auto_pip:
        return
    try:
        resp = ollama_run(model, DEP_PLAN_PROMPT.format(task=task))
        text = resp.strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.split("\n", 1)[1] if "\n" in text else text
        data = json.loads(text)
        pkgs = data.get("packages", [])
        if isinstance(pkgs, list) and pkgs:
            print(f"{ANSI_BLUE}[+] Preflight dependency plan: {', '.join(pkgs)}{ANSI_RESET}")
            pip_install_packages(pkgs)
    except Exception as e:
        print(f"{ANSI_YELLOW}[!] Preflight dependency planning failed: {e}{ANSI_RESET}")

# ----------------------------
# High-level ops
# ----------------------------
def create_project(model: str, root: Path, task: str, entry_hint: str, auto_pip: bool, open_vscode_flag: bool) -> str:
    ensure_dir(root)
    dependency_preflight(model, task, auto_pip)
    resp = ollama_run(model, CREATE_PROMPT.format(task=task))
    entry, files, delete = parse_llm_files(resp)
    if not entry:
        entry = entry_hint or DEFAULT_ENTRY
    materialize_files(root, files, delete)
    if auto_pip:
        pip_install_requirements(root / "requirements.txt")
    manifest = {"model": model, "entrypoint": entry, "task": task}
    save_manifest(root, manifest)
    write_handoff_note(root, "Project Created",
                    f"Entry: `{entry}`\n\nUse the CLI (run/fix/edit/agent/fleet) as needed.")
    if open_vscode_flag:
        open_in_vscode(root)
    return entry

def edit_project(model: str, root: Path, instruction: str, auto_pip: bool, open_vscode_flag: bool):
    manifest = load_manifest(root)
    entry = manifest.get("entrypoint", DEFAULT_ENTRY)
    snapshot = snapshot_project(root)
    resp = ollama_run(model, EDIT_PROMPT.format(instruction=instruction, snapshot=snapshot))
    _, files, delete = parse_llm_files(resp)
    if not files and not delete:
        raise RuntimeError("Edit produced no changes.")
    materialize_files(root, files, delete)
    if auto_pip and (root / "requirements.txt").exists():
        pip_install_requirements(root / "requirements.txt")
    write_handoff_note(root, "Edit Applied", f"Instruction:\n\n{instruction}\n")
    if open_vscode_flag:
        open_in_vscode(root)
    code, out, err = run_project(root, entry)
    if code == 0:
        print(f"{ANSI_GREEN}[+] Project runs successfully after edit.{ANSI_RESET}")
        if out.strip(): print(out)
    else:
        print(f"{ANSI_YELLOW}[!] Project failed after edit. Use 'fix' to attempt automatic repairs.{ANSI_RESET}")
        if err.strip(): print(err)

# ----------------------------
# Agents / Fleets / Delegation
# ----------------------------
def agent_run(model: str, root: Path, name: str, goal: str):
    snapshot = snapshot_project(root)
    resp = ollama_run(model, AGENT_PROMPT.format(goal=goal, snapshot=snapshot))
    _, files, delete = parse_llm_files(resp)
    if not files and not delete:
        print(f"{ANSI_YELLOW}[!] Agent '{name}' produced no changes.{ANSI_RESET}")
        return
    materialize_files(root, files, delete)
    write_handoff_note(root, f"Agent {name} Change", f"Goal:\n\n{goal}\n")
    print(f"{ANSI_GREEN}[+] Agent '{name}' applied changes.{ANSI_RESET}")

def fleet_run(model: str, root: Path, plan_path: Path):
    """
    plan.json schema:
    {
      "entrypoint": "main.py",
      "agents": [
        {"name": "planner", "goal": "draft design"},
        {"name": "builder", "goal": "implement endpoints"},
        {"name": "tester", "goal": "add tests"}
      ]
    }
    """
    data = json.loads(plan_path.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    if not isinstance(agents, list) or not agents:
        print(f"{ANSI_YELLOW}[!] Fleet plan has no agents.{ANSI_RESET}")
        return
    for a in agents:
        name = a.get("name", "agent")
        goal = a.get("goal", "")
        print(f"{ANSI_BLUE}[*] Fleet running agent: {name} — {goal}{ANSI_RESET}")
        agent_run(model, root, name, goal)
    print(f"{ANSI_GREEN}[+] Fleet completed.{ANSI_RESET}")

def delegate_task(model: str, root: Path, src: str, dst: str, context: str):
    goal = f"Delegated by {src} to {dst}: {context}"
    agent_run(model, root, dst, goal)

# ----------------------------
# MCP-style connectors (minimal)
# mcp_config.yaml example:
# tools:
#   db.users.count:
#     kind: sqlite
#     path: data/app.db
#     query: "SELECT COUNT(*) FROM users;"
#   http.get.github:
#     kind: http_get
#     base: "https://api.github.com"
# ----------------------------
def load_yaml_safe(p: Path) -> dict:
    try:
        import yaml  # PyYAML
    except ImportError:
        pip_install_packages(["pyyaml"])
        import yaml
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def mcp_call(root: Path, tool: str, arg: Optional[str]):
    cfg_path = root / MCP_CONFIG_FILE
    if not cfg_path.exists():
        print(f"{ANSI_YELLOW}[!] No {MCP_CONFIG_FILE} found in project.{ANSI_RESET}")
        return
    cfg = load_yaml_safe(cfg_path) or {}
    tools = (cfg.get("tools") or {})
    spec = tools.get(tool)
    if not spec:
        print(f"{ANSI_YELLOW}[!] Tool '{tool}' not found in {MCP_CONFIG_FILE}.{ANSI_RESET}")
        return
    kind = spec.get("kind")
    if kind == "sqlite":
        import sqlite3
        dbp = spec.get("path")
        q = spec.get("query")
        if arg:
            # Allow substituting {arg} in query
            q = (q or "").replace("{arg}", arg)
        con = sqlite3.connect(str((root / dbp) if dbp and not os.path.isabs(dbp) else dbp))
        cur = con.cursor()
        cur.execute(q)
        rows = cur.fetchall()
        con.close()
        print(json.dumps(rows, indent=2))
    elif kind == "http_get":
        base = spec.get("base", "").rstrip("/")
        path = (arg or "").lstrip("/")
        url = f"{base}/{path}" if path else base
        proc = subprocess.run(["curl", "-sS", url], text=True, capture_output=True)
        sys.stdout.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)
    elif kind == "http_post":
        url = spec.get("url")
        data = spec.get("json", {})
        if arg:
            # Allow passing raw JSON as arg to override
            try:
                data = json.loads(arg)
            except Exception:
                pass
        proc = subprocess.run(["curl", "-sS", "-X", "POST", "-H", "Content-Type: application/json",
                               "-d", json.dumps(data), url], text=True, capture_output=True)
        sys.stdout.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)
    elif kind == "doc_read":
        doc = spec.get("path")
        p = (root / doc).resolve() if doc and not os.path.isabs(doc) else Path(doc)
        if p.exists():
            print(p.read_text(encoding="utf-8"))
        else:
            print(f"{ANSI_YELLOW}[!] Doc path not found: {p}{ANSI_RESET}")
    else:
        print(f"{ANSI_YELLOW}[!] Unsupported MCP tool kind: {kind}{ANSI_RESET}")

# ----------------------------
# Exec runner (streaming + red stderr)
# ----------------------------
def stream_exec(cmd: str, cwd: Path) -> int:
    print(f"{ANSI_BLUE}[$] {cmd}{ANSI_RESET}")
    proc = subprocess.Popen(cmd, cwd=str(cwd), shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    def pump(stream, color=None):
        for line in iter(stream.readline, ''):
            if color:
                sys.stderr.write(color + line + ANSI_RESET)
            else:
                sys.stdout.write(line)
    t1 = threading.Thread(target=pump, args=(proc.stdout, None), daemon=True)
    t2 = threading.Thread(target=pump, args=(proc.stderr, ANSI_RED), daemon=True)
    t1.start(); t2.start()
    proc.wait()
    t1.join(); t2.join()
    return proc.returncode

# ----------------------------
# CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Autonomous multi-file coding agent (Ollama) with VS Code, Agents, MCP, and Exec.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # new
    p_new = sub.add_parser("new", help="Create a new project and auto-fix until it runs.")
    p_new.add_argument("task", help="Natural language task for the project.")
    p_new.add_argument("--dir", required=True, help="Project directory.")
    p_new.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")
    p_new.add_argument("--entry", default=DEFAULT_ENTRY, help="Entrypoint hint (if not provided by model).")
    p_new.add_argument("--max-iters", type=int, default=6, help="Max fix iterations.")
    p_new.add_argument("--no-auto-pip", action="store_true", help="Disable automatic pip installs.")
    p_new.add_argument("--vscode", action="store_true", help="Open/focus the project in VS Code.")

    # fix
    p_fix = sub.add_parser("fix", help="Run fix loop on an existing project.")
    p_fix.add_argument("--dir", required=True, help="Project directory.")
    p_fix.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")
    p_fix.add_argument("--entry", default=None, help="Entrypoint override (otherwise read from manifest).")
    p_fix.add_argument("--max-iters", type=int, default=6, help="Max fix iterations.")
    p_fix.add_argument("--no-auto-pip", action="store_true", help="Disable automatic pip installs.")
    p_fix.add_argument("--vscode", action="store_true", help="Open/focus the project in VS Code.")

    # edit
    p_edit = sub.add_parser("edit", help="Edit/extend an existing project with new instructions.")
    p_edit.add_argument("--dir", required=True, help="Project directory.")
    p_edit.add_argument("instruction", help="Describe what to add/change.")
    p_edit.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")
    p_edit.add_argument("--no-auto-pip", action="store_true", help="Disable automatic pip installs.")
    p_edit.add_argument("--vscode", action="store_true", help="Open/focus the project in VS Code.")

    # run
    p_run = sub.add_parser("run", help="Just run the project once (no LLM).")
    p_run.add_argument("--dir", required=True, help="Project directory.")
    p_run.add_argument("--entry", default=None, help="Entrypoint override (otherwise read from manifest).")
    p_run.add_argument("--vscode", action="store_true", help="Open/focus the project in VS Code.")

    # open (just open VS Code on the project)
    p_open = sub.add_parser("open", help="Open the project in VS Code.")
    p_open.add_argument("--dir", required=True, help="Project directory.")

    # exec
    p_exec = sub.add_parser("exec", help="Execute a shell command in the project (stream output).")
    p_exec.add_argument("--dir", required=True, help="Project directory.")
    p_exec.add_argument("command", help="Command string to execute (quoted).")

    # agent
    p_agent = sub.add_parser("agent", help="Run a single scriptable agent against the project.")
    sp_agent = p_agent.add_subparsers(dest="agent_cmd", required=True)
    p_agent_run = sp_agent.add_parser("run", help="Run one agent with a goal.")
    p_agent_run.add_argument("--dir", required=True, help="Project directory.")
    p_agent_run.add_argument("--name", default="agent", help="Agent name.")
    p_agent_run.add_argument("--goal", required=True, help="What the agent should do.")
    p_agent_run.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")

    # fleet
    p_fleet = sub.add_parser("fleet", help="Run multiple agents defined in a plan.json.")
    sp_fleet = p_fleet.add_subparsers(dest="fleet_cmd", required=True)
    p_fleet_run = sp_fleet.add_parser("run", help="Run the fleet plan.")
    p_fleet_run.add_argument("--dir", required=True, help="Project directory.")
    p_fleet_run.add_argument("plan", help="Path to plan.json")
    p_fleet_run.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")

    # delegate
    p_delegate = sub.add_parser("delegate", help="Delegate a sub-task from one agent to another.")
    p_delegate.add_argument("--dir", required=True, help="Project directory.")
    p_delegate.add_argument("--from", dest="src", required=True, help="Source agent name.")
    p_delegate.add_argument("--to", dest="dst", required=True, help="Destination agent name.")
    p_delegate.add_argument("--context", required=True, help="Delegation context.")
    p_delegate.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")

    # MCP
    p_mcp = sub.add_parser("mcp", help="Minimal MCP-style integration calls.")
    sp_mcp = p_mcp.add_subparsers(dest="mcp_cmd", required=True)
    p_mcp_call = sp_mcp.add_parser("call", help="Call a configured connector/tool.")
    p_mcp_call.add_argument("--dir", required=True, help="Project directory.")
    p_mcp_call.add_argument("--tool", required=True, help="Tool id, e.g., db.users.count")
    p_mcp_call.add_argument("--arg", default=None, help="Optional argument (e.g., path or JSON)")

    args = parser.parse_args()
    proj = Path(args.dir) if hasattr(args, "dir") else None

    if args.cmd == "new":
        entry = create_project(args.model, proj, args.task, args.entry, auto_pip=(not args.no_auto_pip), open_vscode_flag=args.vscode)
        print(f"{ANSI_GREEN}[+] Project created at {proj} (entry: {entry}){ANSI_RESET}")
        ok = fix_loop(args.model, proj, entry, args.max_iters, auto_pip=(not args.no_auto_pip))
        sys.exit(0 if ok else 1)

    elif args.cmd == "fix":
        manifest = load_manifest(proj)
        entry = args.entry or manifest.get("entrypoint") or DEFAULT_ENTRY
        if args.vscode:
            open_in_vscode(proj)
        ok = fix_loop(args.model, proj, entry, args.max_iters, auto_pip=(not args.no_auto_pip))
        sys.exit(0 if ok else 1)

    elif args.cmd == "edit":
        edit_project(args.model, proj, args.instruction, auto_pip=(not args.no_auto_pip), open_vscode_flag=args.vscode)

    elif args.cmd == "run":
        if args.vscode:
            open_in_vscode(proj)
        manifest = load_manifest(proj)
        entry = args.entry or manifest.get("entrypoint") or DEFAULT_ENTRY
        code, out, err = run_project(proj, entry)
        print(out, end="")
        if err.strip():
            print(ANSI_RED + err + ANSI_RESET, file=sys.stderr, end="")
        sys.exit(code)

    elif args.cmd == "open":
        open_in_vscode(proj)

    elif args.cmd == "exec":
        rc = stream_exec(args.command, proj)
        sys.exit(rc)

    elif args.cmd == "agent":
        if args.agent_cmd == "run":
            agent_run(args.model, proj, args.name, args.goal)

    elif args.cmd == "fleet":
        if args.fleet_cmd == "run":
            fleet_run(args.model, proj, Path(args.plan))

    elif args.cmd == "delegate":
        delegate_task(args.model, proj, args.src, args.dst, args.context)

    elif args.cmd == "mcp":
        if args.mcp_cmd == "call":
            mcp_call(proj, args.tool, args.arg)

if __name__ == "__main__":
    main()
