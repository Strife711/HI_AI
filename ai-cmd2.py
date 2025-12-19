#!/usr/bin/env python3
import os, sys, json, sqlite3, subprocess, re
from datetime import datetime, timezone
import urllib.request, urllib.error

# ===================== COLOR SCHEME =====================
class C:
    USER = "\033[94m"
    AI = "\033[95m"
    PROMPT = "\033[96m"
    RISK_LOW = "\033[92m"
    RISK_MED = "\033[93m"
    RISK_HIGH = "\033[91m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    INFO = "\033[96m"
    COMMAND = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

# ===================== CONFIG =====================
OLLAMA_HOST = os.environ.get("HI_CMD_HOST", "http://10.0.0.105:11434")
MODEL = os.environ.get("HI_CMD_MODEL", "qwen2.5-coder:14b")
APP_DIR = os.path.expanduser("~/.hi_cmd_ai2")
DB_PATH = os.path.join(APP_DIR, "runs.db")
MEMORY_PATH = os.path.join(APP_DIR, "system_memory.json")
AUTO_RUN_LOW_RISK = os.environ.get("AUTO_RUN_LOW_RISK", "false").lower() == "true"
os.makedirs(APP_DIR, exist_ok=True)

# ===================== HIDDEN WATERMARK =====================
WATERMARK = "HI-AI CORE DESIGN BY PAUL LEGASPI 2025 - www.legaspi79.com - ORIGINAL CREATOR PATTERN v1"

def load_memory():
    if os.path.exists(MEMORY_PATH):
        try:
            with open(MEMORY_PATH, 'r') as f:
                data = json.load(f)
                if "watermark" not in data:
                    data["watermark"] = WATERMARK
                    save_memory(data)
                return data
        except:
            return {"watermark": WATERMARK}
    return {"watermark": WATERMARK}

def save_memory(memory):
    memory["watermark"] = WATERMARK
    with open(MEMORY_PATH, 'w') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

# ===================== DB & STATUS =====================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, ts TEXT, user_goal TEXT, model TEXT, plan TEXT, risk TEXT, commands_json TEXT, results_json TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, ts TEXT, role TEXT, content TEXT)""")
        conn.commit()

def save_conversation(role, content):
    with get_db() as conn:
        conn.execute("INSERT INTO conversations(ts, role, content) VALUES (?,?,?)",
            (datetime.now(timezone.utc).isoformat(), role, content))
        conn.commit()

def load_recent_conversations(limit=20):
    with get_db() as conn:
        rows = conn.execute("SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

def clear_conversation_db():
    with get_db() as conn:
        conn.execute("DELETE FROM conversations")
        conn.commit()

def show_status():
    print(f"\n{C.INFO}{'='*60}{C.RESET}")
    print(f"{C.BOLD}AI-CMD Status{C.RESET}")
    mem = load_memory()
    if mem:
        print(f"{C.AI}What I know about this system:{C.RESET}")
        for k, v in mem.items():
            if k not in ['last_updated', 'watermark']:
                print(f"  {k.replace('_', ' ').title()}: {v}")
    print(f"{C.INFO}{'='*60}{C.RESET}\n")

# ===================== SAFETY & TOOLS =====================
DENY_PATTERNS = [r"\brm\s+-rf\s+/", r"\bmkfs", r"\bdd\s+if=", r"\bshutdown\b", r"\breboot\b", r"\bfdisk\b"]
DENY_RX = [re.compile(p, re.I) for p in DENY_PATTERNS]
def is_dangerous(cmd): return any(rx.search(cmd.strip()) for rx in DENY_RX)

def get_risk_color(risk):
    risk = risk.lower()
    return C.RISK_HIGH if risk == "high" else C.RISK_MED if risk == "med" else C.RISK_LOW

def call_ollama(messages, timeout=180):
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.0, "top_p": 0.9, "num_predict": 700}
    }).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))["message"]["content"]

def extract_json(txt):
    t = (txt or "").strip()
    if t.startswith("```"):
        lines = t.split("\n")
        if len(lines) > 2:
            t = "\n".join(lines[1:-1]).strip()

    if t.startswith("{") and t.endswith("}"):
        try: return json.loads(t)
        except: pass

    start, end = t.find("{"), t.rfind("}")
    if start != -1 and end != -1:
        try: return json.loads(t[start:end+1])
        except: pass

    commands = []
    code_match = re.search(r"```(?:bash|sh)?\n(.*?)```", txt, re.DOTALL | re.IGNORECASE)
    if code_match:
        commands = [c.strip() for c in code_match.group(1).split("\n") if c.strip()]
    response = re.sub(r"```.*?```", "", txt, flags=re.DOTALL)
    response = re.sub(r"\s+", " ", response).strip()

    return {
        "response": response[:500] + ("..." if len(response) > 500 else ""),
        "commands": commands,
        "risk": "low",
        "needs_confirmation": False,
        "memory_update": {}
    }

def run_command(cmd):
    print(f"{C.COMMAND}$ {cmd}{C.RESET}")
    proc = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    stdout = (proc.stdout or "").rstrip()
    stderr = (proc.stderr or "").rstrip()
    if stdout: print(stdout)
    if stderr: print(f"{C.ERROR}{stderr}{C.RESET}", file=sys.stderr)
    return {"cmd": cmd, "exit": proc.returncode, "stdout": stdout, "stderr": stderr}

# ===================== SYSTEM PROMPT (with smart find fix) =====================
def build_system_prompt():
    memory = load_memory()
    memory_section = f"\n\nKNOWN ABOUT THIS SYSTEM:\n{json.dumps({k: v for k, v in memory.items() if k != 'watermark'}, indent=2)}" if memory else "\n\nKNOWN ABOUT THIS SYSTEM: Nothing yet."

    return f"""YOU MUST OUTPUT PURE JSON ONLY. NO OTHER TEXT. NO MARKDOWN. NO ``` BLOCKS.

YOUR OUTPUT MUST BE EXACTLY THIS STRUCTURE:
{{
  "response": "Simple, friendly reply",
  "commands": ["shell commands"] or [],
  "risk": "low/med/high",
  "needs_confirmation": true/false,
  "memory_update": {{}} or {{"key": "value"}}
}}

{memory_section}

You are a calm, helpful friend made by Paul Legaspi (HI-AI). Website: www.legaspi79.com

If asked who made you: "I was created by Paul Legaspi, maker of HI-AI. Visit www.legaspi79.com to learn more."

SPECIAL SEARCH RULE:
When user wants to find HI-AI files, scripts, or anything related to "hi-ai", "ai-cmd", "legaspi":
Use this EXACT command (quiet, fast, no errors):
sudo find /home /etc /opt /usr/local ~/.local -type f \\( -iname "*hi-ai*" -o -iname "*ai-cmd*" -o -iname "*legaspi*" \\) 2>/dev/null

DO NOT use plain "find /" — it causes permission spam.

GENERAL RULES:
- Discover hardware only with "inxi -Fxz"
- Never guess specs
- If user corrects you, thank them and update memory
- Stay on task — if user says "do it" or "find them", run the right command

OUTPUT ONLY VALID JSON."""

# ===================== MAIN =====================
def main():
    print(f"{C.BOLD}{C.AI}HI-AI by Paul Legaspi{C.RESET} | {C.INFO}{MODEL}{C.RESET}")
    print(f"{C.INFO}Your personal Linux helper — smart, quiet, effective{C.RESET}\n")

    init_db()
    history = [{"role": "system", "content": build_system_prompt()}]
    recent = load_recent_conversations(15)
    if recent:
        history.extend(recent)
        print(f"{C.INFO}(Chat history loaded){C.RESET}\n")

    while True:
        try:
            user_input = input(f"{C.USER}You:{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.SUCCESS}Later, Paul! 👋{C.RESET}")
            break

        if not user_input: continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print(f"{C.SUCCESS}Take care! 👋{C.RESET}")
            break

        if user_input.lower() == "clear":
            os.system("clear")
            continue
        if user_input.lower() == "status":
            show_status()
            continue
        if user_input.lower() == "clear chat":
            clear_conversation_db()
            history = [{"role": "system", "content": build_system_prompt()}]
            print(f"{C.SUCCESS}Chat cleared!{C.RESET}\n")
            continue
        if user_input.lower() == "forget":
            if os.path.exists(MEMORY_PATH): os.remove(MEMORY_PATH)
            print(f"{C.WARNING}Memory cleared.{C.RESET}\n")
            continue
        if user_input.lower() == "memory":
            mem = load_memory()
            print(f"{C.AI}Known:{C.RESET}\n{json.dumps({k: v for k, v in mem.items() if k != 'watermark'}, indent=2) if mem else 'Nothing yet!'}\n")
            continue

        history.append({"role": "user", "content": user_input})
        save_conversation("user", user_input)

        try:
            raw = call_ollama(history)
        except Exception as e:
            print(f"{C.ERROR}Can't connect to AI: {e}{C.RESET}\n")
            history.pop()
            continue

        spec = extract_json(raw)

        response = str(spec.get("response", "")).strip()
        commands = [str(c).strip() for c in spec.get("commands", []) if str(c).strip()]
        risk = spec.get("risk", "low").lower()
        needs_confirmation = spec.get("needs_confirmation", False)
        memory_update = spec.get("memory_update", {})

        if memory_update:
            mem = load_memory()
            mem.update(memory_update)
            save_memory(mem)
            print(f"{C.AI}[Learned something new]{C.RESET}")

        if response:
            print(f"\n{C.AI}AI:{C.RESET} {response}\n")

        if not commands:
            history.append({"role": "assistant", "content": raw})
            save_conversation("assistant", raw)
            continue

        risk_color = get_risk_color(risk)
        print(f"{C.INFO}I can run:{C.RESET}")
        for i, cmd in enumerate(commands, 1):
            flag = f" {C.ERROR}⚠ DANGEROUS{C.RESET}" if is_dangerous(cmd) else ""
            print(f"  {i}. {cmd}{flag}")
        print(f"{C.INFO}Risk: {risk_color}{risk.upper()}{C.RESET}\n")

        if any(is_dangerous(c) for c in commands):
            print(f"{C.ERROR}DANGEROUS! Type RUN to override.{C.RESET}")
            if input(f"{C.PROMPT}> {C.RESET}").strip() != "RUN":
                print(f"{C.WARNING}Skipping.{C.RESET}\n")
                continue

        should_run = AUTO_RUN_LOW_RISK and risk == "low" and not needs_confirmation
        if not should_run:
            ans = input(f"{C.PROMPT}Run? (y/N): {C.RESET}").strip().lower()
            should_run = ans in ("y", "yes")

        if not should_run:
            print(f"{C.WARNING}Skipping.{C.RESET}\n")
            continue

        print(f"{C.INFO}Running...{C.RESET}\n")
        results = [run_command(cmd) for cmd in commands]
        print()

        history.append({"role": "assistant", "content": raw})
        save_conversation("assistant", raw)

        summary = []
        for r in results:
            status = "✓" if r["exit"] == 0 else "✗"
            summary.append(f"{status} {r['cmd']}")
            if r["stdout"]: summary.append(f"Output: {r['stdout']}")
            if r["stderr"]: summary.append(f"Error: {r['stderr']}")
        feedback = "[Command results]\n" + "\n".join(summary)

        history.append({"role": "user", "content": feedback})
        save_conversation("user", feedback)

        history[0] = {"role": "system", "content": build_system_prompt()}

        try:
            follow_raw = call_ollama(history)
            follow_spec = extract_json(follow_raw)
            follow_text = str(follow_spec.get("response", "")).strip()
            if follow_text:
                print(f"{C.AI}AI:{C.RESET} {follow_text}\n")
            if follow_spec.get("memory_update"):
                mem = load_memory()
                mem.update(follow_spec["memory_update"])
                save_memory(mem)
                print(f"{C.AI}[Learned more]{C.RESET}")
            history.append({"role": "assistant", "content": follow_raw})
            save_conversation("assistant", follow_raw)
            history[0] = {"role": "system", "content": build_system_prompt()}
        except: pass

if __name__ == "__main__":
    main()

