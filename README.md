# HI-AI  
**by Paul Legaspi**

I didn’t build HI-AI to chase AGI or win benchmarks.

I built it because my brother wanted to switch from Windows to Linux but didn’t want to fight the terminal every time he needed to do something. So I made a small AI called **hi-ai** that could answer questions.

Then he needed it to actually *do* things — so I built **hi-ai2**, which could safely run commands.

Then I got tired of cloud APIs. Around the same time, my kid Cassie wanted help with Minecraft. That’s when it clicked:

**The LLM shouldn’t be the brain.  
It should be a plugin.**

So I rebuilt the system around a **local LLM server** and moved the real logic — memory, routing, tools, and behavior — *outside* the model.

From there it was iteration after iteration, fixing what annoyed me instead of chasing hype:

- **HI-AI6** – Clean answers, no memory. Felt dead  
- **HI-AI7** – Warmer tone, still forgot everything  
- **HI-AI8–10** – Better memory, routing, planning  
- **HI-AI11–12** – Multiple models, smarter decisions  
- **HI-AI13** – Persistent, personality-consistent memory across days  

No hype.  
No “sentient” claims.

Just a **modular, local AI system** that remembers, adapts, runs commands when appropriate, and actually helps real people.

---

## What HI-AI Is (and Is Not)

HI-AI **does NOT** run an LLM on every device.

You are expected to run **your own LLM server**.

HI-AI connects to that server over HTTP and treats the model as a **replaceable backend**.

- The **system** is the point  
- The **model** is a plugin  
- Swap models, move hardware, scale up or down — the tools don’t change  

This keeps power usage realistic and avoids cloud lock-in.  
I don’t have Microsoft money to open a nuclear reactor — and I don’t want to.

Website: **https://legaspi79.com**

---

## What’s Included

- **ai-cmd2**  
  Terminal assistant that explains Linux and can safely run commands

- **hi-ai13**  
  Conversational AI with memory and smart model routing  
  (No command execution — talk only)

Both tools connect to the **same LLM server**.

---

## Try It Online (No Install)

Live demo:  
👉 **https://hiai-all.legaspi79.com/**

(Create an account → Login → Chat)

---

## Architecture Overview (Important)

```
[ Your Device(s) ]
   |        |
ai-cmd2  hi-ai13
   |        |
   +---- HTTP ----+
                  |
            [ LLM SERVER ]
             (Ollama)
          http://IP:11434
                  |
            [ Local Models ]
```

- One LLM server can serve many tools
- Tools can run on different machines
- The server can be a desktop, VM, NAS, or small box

---

# Build Your Own LLM Server (Required)

HI-AI requires **Ollama** running as an LLM server.

You can run it:
- on the same machine
- on a dedicated server box
- on a VM or homelab system

### 1) Install Ollama (Server Machine)

https://ollama.com/download

After install, verify it’s running:

```bash
curl http://127.0.0.1:11434/api/tags
```

If you see JSON, the server is up.

---

## Expose Ollama on Your Network (LAN / Server Use)

By default, Ollama listens only on localhost.

If HI-AI runs on another machine, you must expose Ollama.

### 2) Set Ollama to listen on all interfaces

```bash
sudo systemctl edit ollama
```

Add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Test from another machine:

```bash
curl http://SERVER_IP:11434/api/tags
```

---

## Static IP (Strongly Recommended)

Your LLM server should **not change IPs**.

Options:
- Set a static IP on the server
- OR create a DHCP reservation in your router

Example:
```
LLM Server IP: 10.0.0.105
Port: 11434
```

HI-AI tools assume this address stays stable.

---

## Firewall / Port Notes

- Ollama uses **TCP port 11434**
- Ensure it’s allowed on the server firewall
- No inbound internet exposure is required

This is **LAN-only** unless you intentionally expose it.

---

## Install HI-AI Tools (Client Machines)

### Install ai-cmd2 (Terminal Assistant)

```bash
mkdir -p ~/.local/bin
curl -sSL https://raw.githubusercontent.com/Strife711/HI_AI/main/ai-cmd2.py -o ~/.local/bin/ai-cmd2
sed -i '1s/^\xEF\xBB\xBF//' ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
```

Run:
```bash
ai-cmd2
```

---

### Install hi-ai13 (Conversational AI)

```bash
mkdir -p ~/.local/bin
curl -sSL https://raw.githubusercontent.com/Strife711/HI_AI/main/hi-ai13.py -o ~/.local/bin/hi-ai13
sed -i '1s/^\xEF\xBB\xBF//' ~/.local/bin/hi-ai13
chmod +x ~/.local/bin/hi-ai13
```

Run:
```bash
hi-ai13
```

---

## Configure HI-AI to Use Your LLM Server

### ai-cmd2
```bash
export HI_CMD_HOST="http://SERVER_IP:11434"
```

Add to `~/.bashrc` to make permanent.

---

### hi-ai13
Edit the script and change:

```python
PLUGIN_HOST = "http://SERVER_IP:11434"
```

---

## Install Required Models (On the LLM Server)

### For ai-cmd2
```bash
ollama pull qwen2.5-coder:14b
```

### For hi-ai13
```bash
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-math:7b
ollama pull meditron:7b
```

Models can be swapped later — the system does not depend on one model.

---

## Which Tool Should I Use?

| Tool     | Purpose                         | Runs Commands |
|---------|----------------------------------|---------------|
| ai-cmd2 | Linux helper + execution         | ✅ Yes        |
| hi-ai13 | Conversational AI + memory       | ❌ No         |

**Rule of thumb**
- Use **ai-cmd2** to *do things*
- Use **hi-ai13** to *talk*

---

## Licensing

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
