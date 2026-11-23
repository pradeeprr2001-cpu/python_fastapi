from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_products(client: TestClient):
    create = client.post(
        "/products/",
        json={"name": "Notebook", "description": "A5 dotted", "price": 4.5},
    )
    assert create.status_code == 201
    body = create.json()
    assert body["name"] == "Notebook"
    assert "id" in body

    listed = client.get("/products/")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_missing_product(client: TestClient):
    response = client.get("/products/999")
    assert response.status_code == 404
