def get_order_total_price(products):
    return round(sum(item.item.price * item.quantity for item in products), 2)
