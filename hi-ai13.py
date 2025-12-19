#!/usr/bin/env python3
"""
chat-ai13 — Pure conversational HI-AI13
Advanced chatbot with model routing, memory, and user profiling
No command execution — that's for ai-cmd2
"""

import os, sys, time, json, re, sqlite3
from datetime import datetime, timezone
import urllib.request, urllib.error
from collections import Counter

# ===================== COLORS =====================
class Colors:
    BLUE = '\033[94m'      # User
    GREEN = '\033[92m'     # AI
    YELLOW = '\033[93m'    # System
    RED = '\033[91m'       # Error
    MAGENTA = '\033[95m'   # Model info
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ===================== CONFIG =====================
# CHANGE THIS if your Ollama server is on another machine
# Default: http://127.0.0.1:11434 (local)
# Example remote: http://10.0.0.105:11434
PLUGIN_HOST = "http://127.0.0.1:11434"

APP_DIR = os.path.expanduser("~/.chat_ai13")
DB_PATH = os.path.join(APP_DIR, "memory.db")
PROFILE_PATH = os.path.join(APP_DIR, "profile.json")

MODELS = {
    "general": "llama3.1:8b",
    "code": "qwen2.5-coder:7b",
    "math": "qwen2.5-math:7b",
    "medical": "meditron:7b",
    "logic": "llama3.1:8b"
}

MAX_CONTEXT = 16
os.makedirs(APP_DIR, exist_ok=True)
START_TIME = time.time()

# ===================== USER PROFILE =====================
class UserProfile:
    def __init__(self):
        self.data = self.load()
    
    def load(self):
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH) as f:
                return json.load(f)
        return {"style": [], "topics": {}, "models": {}, "count": 0}
    
    def save(self):
        with open(PROFILE_PATH, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log(self, text: str, model: str):
        self.data["count"] += 1
        self.data["models"][model] = self.data["models"].get(model, 0) + 1
        if any(w in text.lower() for w in ["fuck", "shit", "damn"]):
            self.data["style"].append("casual")
        if len(text) < 40:
            self.data["style"].append("short")
        self.data["style"] = self.data["style"][-20:]
        self.save()
    
    def hint(self) -> str:
        if not self.data["style"]: return ""
        c = Counter(self.data["style"])
        if c["casual"] > 5: return "User is casual — match tone, swearing OK."
        if c["short"] > 10: return "User prefers short answers."
        return ""

profile = UserProfile()

# ===================== DB =====================
def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS convo (
            id INTEGER PRIMARY KEY,
            role TEXT,
            content TEXT,
            model TEXT,
            ts TEXT
        )""")
        c.commit()

def store(role: str, content: str, model: str = ""):
    with db() as c:
        c.execute("INSERT INTO convo(role, content, model, ts) VALUES (?,?,?,?)",
                  (role, content, model, datetime.now(timezone.utc).isoformat()))
        c.commit()

def recent() -> list:
    with db() as c:
        rows = c.execute("SELECT role, content FROM convo ORDER BY id DESC LIMIT ?", (MAX_CONTEXT,)).fetchall()
    return list(reversed([dict(r) for r in rows]))

init_db()

# ===================== ROUTING =====================
ROUTES = {
    "code": re.compile(r"\b(code|script|python|bash|error|debug|fix|api|github)\b", re.I),
    "math": re.compile(r"\b(math|calculate|equation|solve|formula)\b", re.I),
    "medical": re.compile(r"\b(medical|health|symptom|drug|diagnosis)\b", re.I),
    "logic": re.compile(r"\b(logic|reason|why|analyze|prove)\b", re.I),
}

def route(text: str) -> tuple[str, str]:
    for key, rx in ROUTES.items():
        if rx.search(text):
            return MODELS[key], key
    return MODELS["general"], "general"

# ===================== LLM CALL =====================
def call_llm(messages: list, model: str) -> str:
    try:
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.8}
        }).encode()
        req = urllib.request.Request(PLUGIN_HOST + "/api/chat", data=payload,
                                   headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["message"]["content"]
    except Exception as e:
        return f"Connection error: {e}. Is Ollama running at {PLUGIN_HOST}?"

# ===================== UI =====================
def banner():
    print(f"{Colors.BOLD}╔══════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}║        chat-ai13 by Paul         ║{Colors.RESET}")
    print(f"{Colors.BOLD}╚══════════════════════════════════╝{Colors.RESET}")
    print(f"Conversational HI-AI — no commands, just talk")
    print(f"Host: {PLUGIN_HOST}")
    print(f"Sessions: {profile.data['count']}\n")
    print("Type 'exit', 'stats', 'memory', or 'clear'\n")

def stats():
    uptime = int(time.time() - START_TIME)
    with db() as c:
        total = c.execute("SELECT COUNT(*) FROM convo").fetchone()[0]
    print(f"\nUptime: {uptime}s | Messages: {total} | Sessions: {profile.data['count']}\n")

def memory():
    print(f"\n{Colors.YELLOW}What I know about you:{Colors.RESET}")
    print(f"Total interactions: {profile.data['count']}")
    if profile.data["models"]:
        print("Favorite models:")
        for m, c in sorted(profile.data["models"].items(), key=lambda x: -x[1]):
            print(f"  {m}: {c}")
    hint = profile.hint()
    if hint: print(f"Style: {hint}")
    print()

# ===================== MAIN =====================
def main():
    banner()
    while True:
        try:
            u = input(f"{Colors.BLUE}You > {Colors.RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}Bye!{Colors.RESET}")
            break

        if not u: continue
        if u.lower() in ("exit", "quit"): 
            print(f"{Colors.YELLOW}Later!{Colors.RESET}")
            break
        if u.lower() == "clear":
            os.system("clear" if "linux" in sys.platform else "cls")
            banner()
            continue
        if u.lower() == "stats": 
            stats()
            continue
        if u.lower() == "memory":
            memory()
            continue

        store("user", u)
        history = recent()
        model, reason = route(u)
        hint = profile.hint()

        msgs = [{"role": "system", "content": 
                "You are chat-ai13 — a smart, honest conversational AI.\n"
                "Be natural, direct, helpful. No disclaimers.\n"
                "Match the user's style.\n"
                + (hint + "\n" if hint else "") +
                "You're here to talk and help."}]
        msgs.extend(history)
        msgs.append({"role": "user", "content": u})

        reply = call_llm(msgs, model)
        profile.log(u, model)
        store("assistant", reply, model)

        print(f"\n{Colors.GREEN}{reply}{Colors.RESET}")
        print(f"{Colors.MAGENTA}[{model} • {reason}]{Colors.RESET}\n")

if __name__ == "__main__":
    main()
