from fastapi.testclient import TestClient


def _get_admin_token(client: TestClient) -> str:
    create_response = client.post(
        "/admins/",
        json={"username": "admin_upload", "password": "supersecure123"},
    )
    assert create_response.status_code == 200

    login_response = client.post(
        "/admins/login",
        json={"username": "admin_upload", "password": "supersecure123"},
    )
    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_presigned_url_requires_auth(client: TestClient):
    response = client.post(
        "/upload/presigned-url",
        json={"fileName": "soap.jpg", "contentType": "image/jpeg"},
    )

    assert response.status_code == 401


def test_presigned_url_rejects_invalid_content_type(client: TestClient):
    token = _get_admin_token(client)

    response = client.post(
        "/upload/presigned-url",
        json={"fileName": "soap.svg", "contentType": "image/svg+xml"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "Invalid contentType" in response.json()["detail"]


def test_presigned_url_returns_upload_url_and_key(client: TestClient, monkeypatch):
    token = _get_admin_token(client)

    def mock_generate_presigned_put_url(key: str, content_type: str, expires_in: int = 300) -> str:
        assert content_type == "image/jpeg"
        assert expires_in == 300
        assert key.startswith("products/")
        assert "../" not in key
        return f"https://example-bucket.s3.amazonaws.com/{key}?signature=test"

    monkeypatch.setattr(
        "app.routes.upload_routes.generate_presigned_put_url",
        mock_generate_presigned_put_url,
    )

    response = client.post(
        "/upload/presigned-url",
        json={"fileName": "../../my soap.jpg", "contentType": "image/jpeg"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["key"].startswith("products/")
    assert body["key"].endswith("my-soap.jpg")
    assert body["uploadUrl"].startswith("https://example-bucket.s3.amazonaws.com/")
