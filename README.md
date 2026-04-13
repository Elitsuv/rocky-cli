# 🪨 Rocky

> *"Question? I answer. We do science."*

Rocky is a terminal companion inspired by the Eridian character from **Project Hail Mary** by Andy Weir. It runs as an interactive shell with commands themed around the novel — astrophage science, the Hail Mary mission, Eridian lore, and Rocky's iconic personality.

---

## 📁 Project Structure

```
rocky/
├── rocky.py
├── test.py           
├── README.md
├── .gitignore
└── rky/              
    ├── __init__.py
    ├── commands.py     ← All commands and the router
    ├── brain.py        ← NN layer of rocky
    └── personality.py  ← Response formatting + Rocky's voice
```
---

## Running Rocky
**Interactive mode**
```bash
python rocky.py
```

---

## 🔧 Requirements

- Python 3.10+
- No external libraries — standard library only

---

## 🪐 Adding New Commands

1. Add a function `cmd_yourcommand()` in `rky/commands.py`
2. Register it in `COMMAND_MAP` with your trigger phrase as the key
3. That's it — the router handles the rest
 
Rocky is an Eridian scientist. Logic is good. Panic is not.
