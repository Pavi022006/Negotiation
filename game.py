import time

def run_negotiation(buyer, seller, item, time_limit=180):
    start_time = time.time()

    # Opening moves
    buyer_msg, buyer_offer = buyer.make_opening_offer(item)
    seller_msg, seller_offer = seller.make_opening_offer(item)

    print("Buyer:", buyer_msg)
    print("Seller:", seller_msg)

    # Negotiation loop
    current_offer = buyer_offer
    while time.time() - start_time < time_limit:
        time_left = time_limit - (time.time() - start_time)

        # Seller responds
        seller_msg, current_offer = seller.respond_to_offer(current_offer, time_left)
        print("Seller:", seller_msg)

        if "Deal" in seller_msg:
            return "Deal closed at", current_offer

        # Buyer responds
        buyer_msg, current_offer = buyer.respond_to_offer(current_offer, time_left)
        print("Buyer:", buyer_msg)

        if "Deal" in buyer_msg:
            return "Deal closed at", current_offer

    return "No deal", None
