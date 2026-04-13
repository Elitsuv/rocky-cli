# 🪨 Rocky

> *"Question? I answer. We do science."*

Rocky is a terminal companion inspired by the Eridian scientist from **Project Hail Mary** by Andy Weir.  
It lives in your terminal, talks back in Rocky's voice, and helps you stay productive — todo lists, focus timers, streaks, notes, quick tools, and more.

---

## First time?

When Rocky starts, he'll ask your name and your focus area (coding, physics, exams — whatever you're working on). This personalizes his responses. You can reset this anytime with `know me`.

---

## Single command mode

You can also call Rocky without entering interactive mode:

```bash
rocky status
rocky "focus 50"
rocky "todo add finish the report"
rocky motivate
```

---

## Project Structure

```
rocky-cli/
├── setup.py           ← pip install config
├── rocky.py           ← entry point
└── rky/
    ├── commands.py    ← all commands live here
    ├── brain.py       ← memory and state
    └── personality.py ← Rocky's voice and formatting
```

---

## Adding a new command (takes 2 minutes)

1. Write a function in `rky/commands.py`:

```python
def cmd_mycommand():
    return format_response("Rocky says something here.")
```

2. Add it to `COMMAND_MAP` inside `execute()`:

```python
"mycommand": cmd_mycommand,
```

Done. Rocky will now respond to `mycommand`.

---

## Requirements

- Python 3.10+
- Numpy

---

## Local dev setup

```bash
git clone https://github.com/Elitsuv/rocky-cli.git
cd rocky-cli
pip install -e .
rocky
```

---

## License

Apache 2.0 — see [LICENSE](LICENSE)

---

*Rocky is an Eridian scientist. Logic is good. Panic is not.*