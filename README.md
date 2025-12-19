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

No hype.  
No “sentient” claims.

Just a **local AI that remembers, adapts, runs commands, and actually helps real people**.

- Fully offline  
- No data leaves your machine  
- Built for people switching from Windows who just want help — not lectures  

---

## What’s in This Repo

- **`ai-cmd2.py`** — Terminal assistant (runs commands, Linux help)
- **`hi-ai13b`** — Advanced conversational chatbot (pure chat, smart routing)

Website: **https://www.legaspi79.com**

---

## Try HI-AI Right Now (No Install)

Live demo:  
👉 **https://hiai-all.legaspi79.com/**

1. Create a username & password  
2. Register → Login  
3. Start chatting with HI-AI in your browser  

---

## Install Locally (Linux)

You need **Ollama** running (free local LLM server).

### 1. Install Ollama

Download and install:  
https://ollama.com/download

Pull recommended models:

```bash
ollama run qwen2.5-coder:14b   # Recommended for ai-cmd2
ollama run llama3.1:8b        # Good for hi-ai13b
```

Ollama runs at:  
`http://127.0.0.1:11434`

If Ollama is on another machine (for example `10.0.0.105`), edit the script’s `PLUGIN_HOST` value.

---

### 2. Install `ai-cmd2` (Terminal Helper)

Best for Linux beginners who want the AI to **actually run commands safely**.

```bash
curl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/ai-cmd2.py -o ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Run it:

```bash
ai-cmd2
```

**Recommended model:** `qwen2.5-coder:14b`

---

### 3. Install `hi-ai13b` (Advanced Chatbot)

Pure conversational AI with memory and smart model routing.

```bash
curl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/install-hi-ai13b.sh -o install-hi-ai13b.sh
chmod +x install-hi-ai13b.sh
sudo ./install-hi-ai13b.sh
```

Run it:

```bash
hi-ai13b
```

- Routes between models for code, math, logic, etc.
- Persistent memory across sessions
- Learns your style over time

---

## Which One Should I Use?

| Version   | Purpose               | Best For                          | Runs Commands |
|----------|-----------------------|-----------------------------------|---------------|
| ai-cmd2  | Terminal assistant    | New Linux users, system tasks     | ✅ Yes        |
| hi-ai13b | Conversational AI     | Long chats, memory, reasoning     | ❌ No         |

**Rule of thumb:**  
- Use **ai-cmd2** when you need to *do things*  
- Use **hi-ai13b** when you want to *talk*

---

## Licensing

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

📧 Contact: **paul@legaspi79.com**

I built this for my family first.  
If someone makes money off it, I want my cut.

---

© 2025 Paul Legaspi. All rights reserved.

Made with frustration, love, and far too many late nights.
