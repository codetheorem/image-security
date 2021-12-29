from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)



def test_read_main():
    response = client.post("/fileencrypt",
    headers={"Content-Type": "multipart/form-data"},
    files={"file": open("tests/test_encrypt.py", "rb")}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "test.png","key": int}