import ollama
import random
import time

class NegotiationAgent:
    def __init__(self, role, persona, min_price=None, max_budget=None):
        self.role = role  # "buyer" or "seller"
        self.persona = persona  # diplomat, aggressive, analyst, wildcard
        self.min_price = min_price
        self.max_budget = max_budget
        self.history = []
        self.fallback = None

    def persona_wrap(self, raw_message):
        system_prompts = {
            "aggressive": "You are an aggressive trader. Use ultimatums, short sentences, and urgency.",
            "diplomat": "You are a smooth diplomat. Be polite, persuasive, and collaborative.",
            "analyst": "You are a data-driven negotiator. Use numbers, facts, and logic.",
            "wildcard": "You are unpredictable and creative. Use humor, surprises, and boldness."
        }

        response = ollama.chat(model="llama3", messages=[
            {"role": "system", "content": system_prompts[self.persona]},
            {"role": "user", "content": raw_message}
        ])
        return response['message']['content']

    def make_opening_offer(self, item):
        if self.role == "seller":
            offer = int(self.min_price * 1.2)
        else:
            offer = int(self.max_budget * 0.8)

        message = self.persona_wrap(f"My opening offer is {offer} for {item}.")
        self.history.append(("me", offer))
        return message, offer

    def respond_to_offer(self, opponent_offer, time_left):
        if self.role == "seller":
            target = self.min_price
            next_offer = max(target, int((opponent_offer + target) / 2))
        else:
            target = self.max_budget
            next_offer = min(target, int((opponent_offer + target) / 2))

        # Accept if close or time’s low
        if abs(next_offer - opponent_offer) <= 0.05 * target or time_left < 30:
            return self.persona_wrap(f"Deal! I accept {opponent_offer}."), opponent_offer

        message = self.persona_wrap(f"How about {next_offer}?")
        self.history.append(("me", next_offer))
        return message, next_offer

    def decide_fallback(self):
        if self.role == "seller":
            self.fallback = int((self.min_price + self.min_price * 1.5) / 2)
        else:
            self.fallback = int((self.max_budget + self.max_budget * 0.7) / 2)
