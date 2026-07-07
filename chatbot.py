# Name: Khushi Rani Shaw
# Simple NLP Chatbot using Python + Tkinter

import tkinter as tk
from tkinter import scrolledtext
import re
import random
from datetime import datetime

class SimpleChatbot:

    def __init__(self):

        self.stop_words = ["how", "are", "you", "is", "the", "a", "an", "what"]

        self.knowledge_base = {
            "greeting": {
                "patterns": [r"\b(hi|hello|hey)\b"],
                "responses": [
                    "Hello! How can I help you?",
                    "Hi there!",
                    "Hey! Nice to meet you."
                ]
            },

            "time": {
                "patterns": [r"\b(time)\b"],
                "responses": []
            },

            "joke": {
                "patterns": [r"\b(joke)\b"],
                "responses": [
                    "Why did the programmer quit his job? He didn't get arrays 😄",
                    "Why do Java developers wear glasses? Because they don't C 😄"
                ]
            },

            "thanks": {
                "patterns": [r"\b(thanks|thank you)\b"],
                "responses": ["You're welcome!", "Happy to help!"]
            },

            "bye": {
                "patterns": [r"\b(bye|goodbye)\b"],
                "responses": ["Bye! Take care!", "See you later!"]
            }
        }

    def tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text.split()

    def extract_keywords(self, tokens):
        return [word for word in tokens if word not in self.stop_words]

    def match_pattern(self, user_input):
        for category in self.knowledge_base:
            for pattern in self.knowledge_base[category]["patterns"]:
                if re.search(pattern, user_input.lower()):
                    return category
        return None

    def generate_response(self, user_input):

        tokens = self.tokenize(user_input)
        keywords = self.extract_keywords(tokens)

        category = self.match_pattern(user_input)

        if category == "time":
            return "Current time is: " + datetime.now().strftime("%I:%M %p")

        if category:
            return random.choice(self.knowledge_base[category]["responses"])

        return "Sorry, I didn't understand that."


class ChatbotGUI:

    def __init__(self):

        self.bot = SimpleChatbot()

        self.window = tk.Tk()
        self.window.title("Simple Chatbot")

        self.chat_area = scrolledtext.ScrolledText(self.window, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state="disabled")

        self.entry = tk.Entry(self.window, width=40)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        self.clear_btn = tk.Button(self.window, text="Clear", command=self.clear_chat)
        self.clear_btn.pack(side=tk.LEFT)

        self.window.mainloop()

    def display_message(self, sender, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, sender + ": " + message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        user_text = self.entry.get()
        if user_text.strip() == "":
            return

        self.display_message("You", user_text)

        response = self.bot.generate_response(user_text)
        self.display_message("Bot", response)

        self.entry.delete(0, tk.END)

    def clear_chat(self):
        self.chat_area.config(state="normal")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state="disabled")


if __name__ == "__main__":
    ChatbotGUI()
