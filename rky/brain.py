import time
import threading
import random
import sys
import os
import json
import numpy as np
from rky.personality import format_response, C

MEMORY = "memory.json"

class Brain:
    def __init__(self):
        self.active = True

        self.state = np.array([0.0, 0.0, 5.0]) 
        
        # ML Feature: Word Embeddings (Simple weight vectors)
        self.vocab_weights = {
            "youtube": np.array([3.0, -2.0, 0.0]),
            "bored": np.array([2.0, -1.0, 0.0]),
            "movie": np.array([2.5, -1.0, 0.0]),
            "jee": np.array([1.0, 3.0, 0.0]),
            "physics": np.array([-1.0, 2.0, 0.0]),
            "math": np.array([-1.0, 2.0, 0.0]),
            "chemistry": np.array([-1.0, 2.0, 0.0]),
            "code": np.array([-0.5, 2.5, 0.0]),
            "matrixmind": np.array([-1.0, 3.0, 0.0]),
            "water": np.array([0.0, 0.0, -5.0]),
            "tired": np.array([1.0, -2.0, 2.0]),
        }
        
        # Fixed the function call to match the defined name
        self.todos = self._load_memory()

    def _load_memory(self): # Added underscore here
        if os.path.exists(MEMORY):
            try:
                with open(MEMORY, "r") as f:
                    return json.load(f).get("todos", [])
            except:
                return []
        return []
    
    def save_memory(self):
        try:
            with open(MEMORY, "w") as f:
                json.dump({"todos": self.todos}, f, indent=4)
            return True
        except:
            return False
        
    def process_input(self, text: str):
        words = text.lower().split()
        for word in words:
            if word in self.vocab_weights: # Fixed "words" to "word"
                self.state += self.vocab_weights[word]

        self.state[2] += 0.5 # Time decay for dehydration
        self.state = np.clip(self.state, 0.0, 10.0) # Prevents Exploding Gradients

    def start_heartbeat(self):
        t = threading.Thread(target=self._pulse, daemon=True)
        t.start()

    def _pulse(self): # Added underscore here
        while self.active:
            time.sleep(90)
            self.state[2] += 1.0 # Hydration alert

            message = ""
            
            if self.state[2] >= 8.0:
                message = self._generate_water_satire()
                self.state[2] = 0.0
            elif self.state[0] > self.state[1] and self.state[0] > 5.0:
                message = "Warning! Astrophage levels rising. Consider H20 or taking a break."
                self.state[0] -= 2.0
            elif self.todos and random.random() > 0.6:
                task = random.choice(self.todos)
                message = f"Task pending: '{task}'. Why is this not complete? Human efficiency is low."
            else:
                message = "Question! Are you applying logic right now, or just staring at the glowing rectangle?"

            self._interrupt_console(message)

    def _generate_water_satire(self):
        satire = [
            "Human biology requires constant fluid. You are drying out like Venus. Drink H2O.",
            "Reminder: Your brain is 73% water. Logic fails when dry. Drink now.",
            "I do not need water. You do. Do not die while we do science."
        ]
        return random.choice(satire)

    def _interrupt_console(self, message):
        """Safely prints over the input line without breaking the terminal."""
        formatted = format_response(message, add_flair=False)
        sys.stdout.write(f"\033[2K\r\n{formatted}{C['ROCKY']}rocky>{C['RESET']} ")
        sys.stdout.flush()

brain = Brain()