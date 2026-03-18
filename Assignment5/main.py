from fastapi import FastAPI

app = FastAPI()

# Sample Data
products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 499},
    {"id": 2, "name": "Keyboard", "category": "Electronics", "price": 799},
    {"id": 3, "name": "Notebook", "category": "Stationery", "price": 99},
    {"id": 4, "name": "Pen", "category": "Stationery", "price": 20},
]

orders = [
    {"id": 1, "customer": "Ram", "total": 1000},
    {"id": 2, "customer": "Sita", "total": 500},
    {"id": 3, "customer": "Ravi", "total": 700},
]

# ---------------- Q1, Q2, Q3 ---------------- #

@app.get("/products")
def get_products(sort_by: str = "price", order: str = "asc", page: int = 1, limit: int = 10):
    if sort_by not in ["price", "name"]:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit

    return sorted_products[start:end]


@app.get("/products/search")
def search_products(search: str):
    result = [p for p in products if search.lower() in p["name"].lower()]

    if not result:
        return {"message": "No products found"}

    return result


# ---------------- Q4 ---------------- #

@app.get("/orders/search")
def search_orders(customer: str):
    result = [o for o in orders if customer.lower() in o["customer"].lower()]

    if not result:
        return {"message": "No orders found"}

    return result


# ---------------- Q5 ---------------- #

@app.get("/products/sort-by-category")
def sort_by_category():
    category_order = {"Electronics": 0, "Stationery": 1}

    return sorted(products, key=lambda x: (category_order[x["category"]], x["price"]))


# ---------------- Q6 ---------------- #

@app.get("/products/browse")
def browse_products(
    search: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 10
):
    result = products

    if search:
        result = [p for p in result if search.lower() in p["name"].lower()]

    if sort_by not in ["price", "name"]:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit

    total_pages = (len(result) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": result[start:end]
    }


# ---------------- BONUS ---------------- #

@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit

    total_pages = (len(orders) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": orders[start:end]
    }