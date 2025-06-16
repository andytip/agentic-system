from fastapi.testclient import TestClient
from main import app
import sys

client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_ask(monkeypatch):
    class FakeResponse:
        def __init__(self, content):
            self.choices = [type("c", (), {"message": {"content": content}})]

    def fake_create(*args, **kwargs):
        return FakeResponse("Hello from OpenAI")

    fake_module = type(
        "m",
        (),
        {
            "ChatCompletion": type(
                "cc", (), {"create": staticmethod(fake_create)}
            )
        },
    )
    monkeypatch.setitem(sys.modules, "openai", fake_module)
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    response = client.post("/ask", json={"prompt": "Hi"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Hello from OpenAI"}
