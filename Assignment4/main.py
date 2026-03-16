from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Product Database
products = {
    1: {"name": "Wireless Mouse", "price": 499},
    2: {"name": "Notebook", "price": 99},
    3: {"name": "USB Hub", "price": 299}
}

cart = {}
orders = []
order_id = 1


class CartItem(BaseModel):
    product_id: int
    qty: int = 1


@app.get("/")
def home():
    return {"message": "Shopping Cart API running"}


# Add item to cart
@app.post("/cart/add")
def add_to_cart(item: CartItem):
    pid = item.product_id

    if pid not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    if pid == 3:
        raise HTTPException(status_code=400, detail="USB Hub cannot be added")

    if pid in cart:
        cart[pid] += item.qty
    else:
        cart[pid] = item.qty

    return {"message": "Cart updated", "cart": cart}


# View cart
@app.get("/cart")
def view_cart():

    items = []
    total = 0

    for pid, qty in cart.items():
        product = products[pid]
        subtotal = product["price"] * qty

        items.append({
            "product": product["name"],
            "qty": qty,
            "subtotal": subtotal
        })

        total += subtotal

    return {
        "items": items,
        "item_count": len(cart),
        "grand_total": total
    }


# Remove item
@app.delete("/cart/remove/{product_id}")
def remove_item(product_id: int):

    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Item not in cart")

    del cart[product_id]

    return {"message": "Item removed", "cart": cart}


# Checkout
@app.post("/cart/checkout")
def checkout():

    global order_id

    if not cart:
        raise HTTPException(status_code=400, detail="Cart empty")

    total = 0
    items = []

    for pid, qty in cart.items():
        product = products[pid]
        subtotal = product["price"] * qty
        total += subtotal

        items.append({
            "product": product["name"],
            "qty": qty,
            "subtotal": subtotal
        })

    order = {
        "order_id": order_id,
        "items": items,
        "total": total
    }

    orders.append(order)
    order_id += 1
    cart.clear()

    return {"message": "Checkout successful", "order": order}


# View all orders
@app.get("/orders")
def get_orders():
    return {"orders": orders}