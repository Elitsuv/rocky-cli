# 🪨 Rocky

> *"Question? I answer. We do science."*

Rocky is a terminal companion inspired by the Eridian character from **Project Hail Mary** by Andy Weir. It runs as an interactive shell with commands themed around the novel — astrophage science, the Hail Mary mission, Eridian lore, and Rocky's iconic personality.

---

## 📁 Project Structure

```
rocky/
├── rocky.py          
├── README.md
├── .gitignore
└── rky/              
    ├── __init__.py
    ├── commands.py     ← All commands and the router
    └── personality.py  ← Response formatting + Rocky's voice
```
---

## Running Rocky
**Interactive mode** (recommended):
```bash
python rocky.py
```

**Single command via CLI:**
```bash
python rocky.py status
python rocky.py "encourage me"
python rocky.py "tau ceti"
```

---

## 🛰️ Available Commands

| Category | Commands |
|---|---|
| **System** | `status`, `diagnostics`, `memory` |
| **Astrophage Science** | `astrophage`, `astrophage fuel`, `tau ceti`, `adrian`, `petrovascope`, `scan radiation`, `analyze atmosphere`, `xenonite` |
| **Lore** | `eridian`, `rocky lore`, `grace`, `hail mary`, `stratt` |
| **Interaction** | `hello`, `encourage me`, `help` |
| **Utility** | `time`, `date`, `open youtube`, `focus mode`, `clear`, `exit` |

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