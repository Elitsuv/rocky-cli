import pyttsx3
import threading
import queue
import re

class VoiceAssistant:
    def __init__(self):
        self.enabled = False
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        try:
            engine = pyttsx3.init()
            # Optional: configure voice properties
            engine.setProperty('rate', 170)
        except Exception:
            return
            
        while True:
            text = self.q.get()
            if text is None: break
            try:
                # Strip ANSI codes just in case
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                clean_text = ansi_escape.sub('', text)
                engine.say(clean_text)
                engine.runAndWait()
            except Exception:
                pass
            self.q.task_done()

    def speak(self, text):
        if self.enabled:
            self.q.put(text)

voice_assistant = VoiceAssistant()
