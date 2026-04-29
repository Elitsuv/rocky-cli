# 🪨 Rocky CLI

<div align="center">
  <p><strong>Your Eridian terminal companion from Project Hail Mary.</strong></p>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/version-v1.1.0-orange.svg" alt="Version" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
</div>

<br/>

Rocky CLI is an interactive, intelligent command-line companion designed to help you focus, manage tasks, and stay hydrated while writing code or doing "science." Inspired by the character Rocky from *Project Hail Mary*, this assistant is built with a sophisticated state-driven "brain" and even speaks to you!

---

##  Features

-  **Voice Engine:** Asynchronous text-to-speech functionality. Rocky talks back!
-  **Focus Mode:** Built-in Pomodoro timer (`focus 25`) with a distraction-blocking terminal UI.
-  **Task Management:** Add, remove, and list pending missions straight from your terminal.
-  **Hydration Tracker:** Rocky tracks your fluid intake over time and warns you if you're getting dehydrated.
-  **Dynamic Memory:** Your profile and state are persistently saved in your home directory (`~/.rocky/`), ensuring a seamless experience across sessions.

---

## 📦 Installation

Installing Rocky is incredibly simple. We've included a script to do the heavy lifting for you!

### Windows (Quick Install)
1. Download or clone this repository to your machine.
2. Double-click the `install.bat` file in the project folder.
3. Once the installation completes, you can delete the downloaded folder.

---

##  Usage

Rocky can be used interactively or directly via command-line arguments!

### Interactive Mode
Launch Rocky's interactive shell by typing:
```bash
rocky
```
*(Type `exit` or `quit` to leave).*

### Single Command Mode
Execute commands directly from your standard terminal without entering the interactive shell:
```bash
rocky focus 50
rocky todo list
rocky status
```

---

##  Command Reference

| Command | Description |
|---|---|
| `help` | View all available ship systems and commands. |
| `status` | View ship overview, your Focus, and Hydration metrics. |
| `focus [mins]` | Start a deep work timer (e.g., `focus 25`). |
| `voice [on/off]`| Toggle Rocky's voice output on or off. |
| `todo add [task]`| Log a new mission to memory. |
| `todo rm [id]` | Complete and remove a mission. |
| `todo list` | View all pending missions. |
| `water` | Log hydration to restore internal fluids. |
| `time` | View current Earth time metrics. |
| `know me` | Reset or update your user profile. |

---

##  Architecture

Rocky CLI is built using a modern Python architecture:
- **`commands.py`**: The central nervous system mapping human input to operations.
- **`brain.py`**: The state engine tracking hydration decay, task completion momentum, and focus.
- **`personality.py`**: The interaction layer responsible for Rocky's unique syntax, text formatting, and flair.
- **`voice.py`**: A threaded text-to-speech queue utilizing `pyttsx3` to prevent UI blocking.

*Note: All persistent user data is safely stored in `~/.rocky/` to avoid polluting your system files.*

---

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
  <i>"Amaze! Amaze! Amaze!"</i>
</div>
