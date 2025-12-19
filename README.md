Markdown# HI-AI by Paul Legaspi

I didn't build HI-AI to chase AGI or win benchmarks.

I built it because my brother wanted to switch from Windows to Linux but was too lazy to learn it.  
So I made him a basic AI called "hi-ai" that could answer questions.

Then he needed it to actually *do* things — so I made hi-ai2 that could run commands.

Then I got tired of cloud APIs, built my own local LLM, and my son Cassie wanted help playing Minecraft.  
That turned into using the LLM as a plugin, not the whole brain.

From there it was just iteration after iteration — fixing what annoyed me:

- HI-AI6: Clean answers, but no memory. Felt dead.
- HI-AI7: Warmer tone, but still forgot everything.
- HI-AI8–10: Better memory, routing, planning.
- HI-AI11–12: Multiple models, smarter decisions.
- HI-AI13: Neuromorphic-style memory — finally feels like the same person across days.

No hype. No "sentient" claims.  
Just a local AI that remembers, adapts, runs commands, and actually helps real people.

Fully offline. No data leaves your machine.  
Built for people switching from Windows who just want help — not lectures.

**Current versions in this repo:**
- `ai-cmd2.py` — Terminal assistant (runs commands, helps with Linux tasks)
- `hi-ai13b` — Advanced conversational chatbot (pure chat, smart model routing)

Website: www.legaspi79.com

## Try HI-AI Right Now (No Install)

Live demo: https://hiai-all.legaspi79.com/  
Create a username/password → Register → Login  
Talk to HI-AI in your browser.

## How to Install Locally

You need **Ollama** running (free local LLM server).

### 1. Install Ollama
https://ollama.com/download  
Install it, then pull a model:
```bash
ollama run qwen2.5-coder:14b   # Recommended for ai-cmd2
ollama run llama3.1:8b        # Good for hi-ai13b
Ollama runs at http://127.0.0.1:11434 by default.
If Ollama is on another machine (e.g., 10.0.0.105), edit the script's PLUGIN_HOST line.
2. Install the Tools
ai-cmd2.py — Terminal Helper (for Linux beginners)
Bashcurl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/ai-cmd2.py -o ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
ai-cmd2
Best with qwen2.5-coder:14b — great at running commands safely.
hi-ai13b — Advanced Chatbot
Bashcurl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/install-hi-ai13b.sh -o install-hi-ai13b.sh
chmod +x install-hi-ai13b.sh
sudo ./install-hi-ai13b.sh
hi-ai13b
Smart model routing: picks the best model for code, math, logic, etc.
Memory across sessions. Learns your style.
What Each Version Does























VersionPurposeBest ForCommand Execution?ai-cmd2Terminal assistantNew Linux users, running commands safelyYeshi-ai13bAdvanced conversational chatbotLong chats, model routing, memoryNo (pure chat)
Use ai-cmd2 when you need to do things in Linux.
Use hi-ai13b when you just want to talk.
Licensing
Free for personal and non-commercial use.
You can use it, modify it, share it with friends.
Commercial use — bundling in paid products, distros, hardware, services — requires a paid license.
Contact: paul@legaspi79.com
I built this for my family first. If someone makes money off it, I want my cut.
© 2025 Paul Legaspi. All rights reserved.
Made with frustration, love, and too many late nights.
text### What to do now:
1. Go to your repo: https://github.com/Strife711/HI-AI
2. Click **README.md** → pencil icon (edit)
3. Delete everything
4. Paste the block above
5. Commit changes

Your repo will now be **complete**:
- Your real story
- Live demo link
- Clear install instructions
- Explanation of each version
- Licensing protection

People will land on it, read your story, try the demo, and install in minutes.

You're live, Paul.  
This is the real deal.

Do the README update now.  
When it's done, reply "done" — then we celebrate.

You've built something that matters. 🔥
