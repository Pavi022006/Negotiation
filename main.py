from agent import NegotiationAgent
from game import run_negotiation

if __name__ == "__main__":
    buyer = NegotiationAgent(role="buyer", persona="analyst", max_budget=220000)
    seller = NegotiationAgent(role="seller", persona="aggressive", min_price=150000)

    item = "100 boxes of Grade-A Alphonso Mangoes"
    result = run_negotiation(buyer, seller, item)
    print("Result:", result)
