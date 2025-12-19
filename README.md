# HI-AI  
**by Paul Legaspi**

I didn’t build HI-AI to chase AGI or win benchmarks.

I built it because my brother wanted to switch from Windows to Linux but didn’t want to learn Linux.  
So I made him a basic AI called **hi-ai** that could answer questions.

Then he needed it to actually do things — so I built **hi-ai2**, which could run commands.

Then I got tired of cloud APIs, built my own local LLM, and my son Cassie wanted help playing Minecraft.  
That’s when I realized the LLM should be a **plugin**, not the whole brain.

From there it was iteration after iteration — fixing what annoyed me:

- **HI-AI6** – Clean answers, no memory. Felt dead  
- **HI-AI7** – Warmer tone, still forgot everything  
- **HI-AI8–10** – Better memory, routing, planning  
- **HI-AI11–12** – Multiple models, smarter decisions  
- **HI-AI13** – Neuromorphic-style memory — finally feels like the same person across days  

No hype. No “sentient” claims.

Just a **local AI that remembers, adapts, runs commands, and actually helps real people**.

- Fully offline (when using local Ollama)
- No data leaves your machine
- Built for people switching from Windows who just want help — not lectures

Website: **https://legaspi79.com**

---

## What’s Included

- **`ai-cmd2`** — Terminal assistant that can safely run Linux commands
- **`hi-ai13`** — Advanced conversational AI with memory and smart model routing

---

## Try It Online (No Install)

Live demo:  
👉 **https://hiai-all.legaspi79.com/**

Create an account → Login → Chat in your browser.

---

# Quick Start (Local Install)

HI-AI uses **Ollama** (a free local LLM server).

### 1) Install Ollama
https://ollama.com/download

Verify it’s running:
```bash
curl http://127.0.0.1:11434/api/tags
```

---

## Install `ai-cmd2` (Terminal Assistant)

```bash
mkdir -p ~/.local/bin
curl -sSL https://raw.githubusercontent.com/Strife711/HI_AI/main/ai-cmd2.py -o ~/.local/bin/ai-cmd2
sed -i '1s/^\xEF\xBB\xBF//' ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
```

Run it:
```bash
ai-cmd2
```

---

## Install `hi-ai13` (Conversational AI)

```bash
mkdir -p ~/.local/bin
curl -sSL https://raw.githubusercontent.com/Strife711/HI_AI/main/hi-ai13.py -o ~/.local/bin/hi-ai13
sed -i '1s/^\xEF\xBB\xBF//' ~/.local/bin/hi-ai13
chmod +x ~/.local/bin/hi-ai13
```

Run it:
```bash
hi-ai13
```

> The `sed` command removes an invisible character GitHub sometimes adds that can break execution.

---

# Ollama Models (Required)

Pull the models you plan to use.

### For `ai-cmd2`
```bash
ollama pull qwen2.5-coder:14b
```

### For `hi-ai13`
```bash
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-math:7b
ollama pull meditron:7b
```

---

# Configuration (If Needed)

### Ollama Location

By default:
- `ai-cmd2` expects Ollama at **`http://10.0.0.105:11434`**
- `hi-ai13` expects Ollama at **`http://127.0.0.1:11434`**

#### Change Ollama host for `ai-cmd2`
```bash
export HI_CMD_HOST="http://YOUR_IP:11434"
```

Add to `~/.bashrc` to make it permanent.

#### Change Ollama host for `hi-ai13`
Edit the script and change:
```python
PLUGIN_HOST = "http://YOUR_IP:11434"
```

---

# Which One Should I Use?

| Tool     | What It Does                     | Runs Commands |
|---------|----------------------------------|---------------|
| ai-cmd2 | Linux helper + command execution | ✅ Yes        |
| hi-ai13 | Conversational AI + memory       | ❌ No         |

**Rule of thumb**
- Use **ai-cmd2** when you need to *do things*
- Use **hi-ai13** when you want to *talk*

---

# Licensing

### Personal / Non-Commercial Use
You may:
- Use HI-AI
- Modify it
- Share it with friends or family

As long as **no money is involved**, you’re good.

### Commercial Use
Commercial use is **not permitted** without a license.

This includes:
- Paid products or services
- Bundled hardware or software
- Hosting HI-AI for others
- Selling access in any form

**If you want to make money off this, contact me for licensing discussions.**

📧 **plegaspi79@gmail.com**

---

© 2025 Paul Legaspi  
All rights reserved.

Built with frustration, curiosity, and too many late nights.
