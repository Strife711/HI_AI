# HI-AI  
**by Paul Legaspi**

I didn’t build HI-AI to chase AGI or win benchmarks.

I built it because my brother wanted to switch from Windows to Linux but didn’t want to learn Linux.  
So I made him a basic AI called **hi-ai** that could answer questions.

Then he needed it to actually do things — so I built **hi-ai2**, which could run commands.

Then I got tired of cloud APIs, built my own local LLM, and my son Cassie wanted help playing Minecraft.  
That’s when I realized the LLM should be a **plugin**, not the whole brain.

From there it was iteration after iteration — fixing what annoyed me:

- **HI-AI6** – Clean answers, no memory. Felt dead.  
- **HI-AI7** – Warmer tone, still forgot everything.  
- **HI-AI8–10** – Better memory, routing, planning.  
- **HI-AI11–12** – Multiple models, smarter decisions.  
- **HI-AI13** – Neuromorphic-style memory. Finally feels like the same person across days.

No hype. No “sentient” claims.  
Just a **local AI that remembers, adapts, and actually helps real people**.

- Fully offline (when running locally)
- No data leaves your machine (unless you point it to a LAN host)
- Built for Windows → Linux switchers who want help — not lectures

---

## What’s in This Repo

- **`ai-cmd2.py`** — Terminal assistant (runs commands, Linux help)
- **`hi-ai13` / `chat-ai13`** — Advanced conversational chatbot (pure chat, smart routing)

Website: **https://www.legaspi79.com**

---

## Try HI-AI Right Now (No Install)

Live demo:  
👉 **https://hiai-all.legaspi79.com/**

1. Create a username & password  
2. Register → Login  
3. Start chatting in your browser  

---

# Build an LLM Server (Ollama) + Install Models

HI-AI uses **Ollama** as the local/LAN LLM server.

### 1) Install Ollama (server machine)

Install: https://ollama.com/download

Verify it’s running:

```bash
curl http://127.0.0.1:11434/api/tags
```

If you see JSON back, Ollama is up.

### 2) Make Ollama accessible on your LAN (optional)

If you want other machines to use the Ollama server (example: `10.0.0.105`), you need Ollama listening on your LAN IP.

**Quick method (systemd override):**

```bash
sudo systemctl edit ollama
```

Paste:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Now test from another machine:

```bash
curl http://10.0.0.105:11434/api/tags
```

> If this fails, it’s usually firewall rules. Allow TCP 11434 on the server machine.

---

## Pull the Models (what HI-AI expects)

### Models for `ai-cmd2` (command-running helper)
`ai-cmd2` defaults to a coder model (recommended):

```bash
ollama pull qwen2.5-coder:14b
```

### Models for `chat-ai13` (multi-model routing chatbot)
`chat-ai13` routes by topic and expects these names by default: :contentReference[oaicite:3]{index=3}

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-math:7b
ollama pull meditron:7b
```

> If you don’t have one of these models installed, either `ollama pull` it, or change the model name in the `MODELS` dictionary (see below).

---

# Install + Run

## Install `ai-cmd2` (Terminal Helper)

```bash
curl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/ai-cmd2.py -o ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Run:

```bash
ai-cmd2
```

## Install `chat-ai13` / `hi-ai13` (Chatbot)

(Use whatever filename you ship in the repo; example below assumes `hi-ai13.py`.)

```bash
curl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/hi-ai13.py -o ~/.local/bin/hi-ai13
chmod +x ~/.local/bin/hi-ai13
hi-ai13
```

---

# Customization (IMPORTANT)

This is the part people always ask for: **how do I point it at my server + change models?**

## A) Customize `ai-cmd2` (no code editing)

`ai-cmd2` is designed to be configured with environment variables: :contentReference[oaicite:4]{index=4}

### Set Ollama host (local vs LAN)
Default is `http://10.0.0.105:11434` unless you override it. :contentReference[oaicite:5]{index=5}

Example: use local Ollama:

```bash
export HI_CMD_HOST="http://127.0.0.1:11434"
```

Example: use LAN server:

```bash
export HI_CMD_HOST="http://10.0.0.105:11434"
```

### Set the model used by ai-cmd2

Default is `qwen2.5-coder:14b`. :contentReference[oaicite:6]{index=6}

```bash
export HI_CMD_MODEL="qwen2.5-coder:14b"
```

Want a smaller model?

```bash
export HI_CMD_MODEL="qwen2.5-coder:7b"
```

### Auto-run low-risk commands (optional)

By default, ai-cmd2 asks before running commands.  
You can allow *auto-run* for “low risk” actions:

```bash
export AUTO_RUN_LOW_RISK=true
```

The script still blocks obviously dangerous commands and forces an override. :contentReference[oaicite:7]{index=7} :contentReference[oaicite:8]{index=8}

### Make these settings permanent

Add to `~/.bashrc`:

```bash
echo 'export HI_CMD_HOST="http://10.0.0.105:11434"' >> ~/.bashrc
echo 'export HI_CMD_MODEL="qwen2.5-coder:14b"' >> ~/.bashrc
echo 'export AUTO_RUN_LOW_RISK=false' >> ~/.bashrc
source ~/.bashrc
```

---

## B) Customize `chat-ai13` / `hi-ai13` (edit 1 block of config)

`chat-ai13` uses a config block at the top:

### 1) Change the Ollama host

Edit `PLUGIN_HOST` here: :contentReference[oaicite:9]{index=9}

- Local: `http://127.0.0.1:11434`
- LAN: `http://10.0.0.105:11434`

### 2) Change which models it routes to

Edit the `MODELS` dictionary here: :contentReference[oaicite:10]{index=10}

Example: make everything use a single model (simple mode)

```python
MODELS = {
  "general": "llama3.1:8b",
  "code": "llama3.1:8b",
  "math": "llama3.1:8b",
  "medical": "llama3.1:8b",
  "logic": "llama3.1:8b"
}
```

### 3) Change routing keywords (how it decides “code vs math vs medical”)

Routing rules are regex patterns here: :contentReference[oaicite:11]{index=11}

If you want “docker” or “systemd” to go to the coder model, add words to the `code` route.

---

# Which One Should I Use?

| Version   | Purpose               | Best For                          | Runs Commands |
|----------|------------------------|-----------------------------------|--------------|
| ai-cmd2  | Terminal assistant     | Linux tasks + safe command running| ✅ Yes       |
| chat-ai13| Conversational AI      | Long chats + memory + routing     | ❌ No        |

Rule of thumb:
- Use **ai-cmd2** when you need to *do things* on Linux
- Use **chat-ai13** when you want to *talk* (and let it route models)

---

# Licensing

### Personal / Non-Commercial Use
You are free to:
- Use HI-AI for personal purposes
- Modify it
- Share it with friends or family

As long as **no money is involved**, you’re good.

### Commercial Use
Commercial use is **NOT** permitted without a paid license.

This includes (but is not limited to):
- Bundling HI-AI with paid software, hardware, or services
- Selling access to HI-AI or hosting it for others
- Including HI-AI in commercial distributions or products

If you want to use HI-AI commercially, you must obtain a license.

📧 Contact: **plegaspi79.com**    *legaspi79.com webpage*** 

I built this for my family first.  
If someone makes money off it, I want my cut.

---

© 2025 Paul Legaspi. All rights reserved.

Made with frustration, love, and far too many late nights.
