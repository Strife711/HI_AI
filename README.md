# HI-AI by Paul Legaspi

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

**Current versions:**
- `ai-cmd2` — Terminal assistant (stable)
- `hi-ai13b` — Advanced chatbot (in development)

Website: www.legaspi79.com

## Try HI-AI Right Now (No Install Needed)

Go to the live demo:  
**https://hiai-all.legaspi79.com/**

1. Create a username and password
2. Click **Register**
3. Then click **Login**

Talk to HI-AI in your browser — see how it feels.

## Local Install (For Full Power)

Want it running on your machine?

```bash
curl -sSL https://raw.githubusercontent.com/Strife711/HI-AI/main/ai-cmd2 -o ~/.local/bin/ai-cmd2
chmod +x ~/.local/bin/ai-cmd2
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
ai-cmd2



## Licensing

Free for personal and non-commercial use.  
You can use it, modify it, share it with friends — no restrictions.

Commercial use — including bundling in paid Linux distributions, selling hardware with HI-AI pre-installed, or offering it as a service — requires a paid license.

Contact: plegaspi79@gmail.com or www.legaspi79.com

I built this for my family first. If someone makes money off it, I want my cut.

© 2025 Paul Legaspi. All rights reserved.
