from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["products"], list)

def test_create_product():
    product_data = {
        "name": "Test shirt",
        "price": 19.99,
        "quantity": 5
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    json_data = response.json()["data"]["product"]
    assert json_data["name"] == "Test shirt"
    assert json_data["price"] == 19.99
    assert json_data["quantity"] == 5

def test_create_order():
    product_data = {
        "name": "Test Jacket",
        "price": 40.0,
        "quantity": 2
    }
    product_res = client.post("/products", json=product_data)
    assert product_res.status_code == 200
    product_id = product_res.json()["data"]["product"]["id"]

    order_data = {
        "product_id": product_id,
        "quantity": 1
    }

    order_res = client.post("/order", json=order_data)
    assert order_res.status_code == 200
    assert order_res.json()["data"]["order"]["product_id"] == product_id

def test_get_product_by_id():
    product_data = {
        "name": "Test Hat",
        "price": 12.99,
        "quantity": 3
    }
    create_res = client.post("/products", json=product_data)
    assert create_res.status_code == 200
    product_id = create_res.json()["data"]["product"]["id"]

    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == 200
    fetched_product = get_res.json()["data"]["product"]

    assert fetched_product["id"] == product_id
    assert fetched_product["name"] == product_data["name"]
    assert fetched_product["price"] == product_data["price"]
    assert fetched_product["quantity"] == product_data["quantity"]
