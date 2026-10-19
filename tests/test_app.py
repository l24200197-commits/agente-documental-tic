from dataclasses import replace
import pytest
from fastapi.testclient import TestClient
import app.main as main
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def no_ask_password(monkeypatch):
    # Las pruebas no dependen de la contraseña definida en el .env local.
    monkeypatch.setattr(main, "settings", replace(main.settings, ask_password=""))

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "Archivo TIC" in r.text

def test_health():
    assert client.get("/api/health").status_code == 200

def test_documents():
    r = client.get("/api/documents")
    assert r.status_code == 200
    assert isinstance(r.json()["documents"], list)

def test_question_validation():
    r = client.post("/api/ask", json={"question": "a"})
    assert r.status_code == 422

def test_sync_not_public():
    # FastAPI TestClient IP ficticia no loopback: bloqueado por diseño.
    r = client.post("/api/sync")
    assert r.status_code == 403

def test_ask_requires_password(monkeypatch):
    monkeypatch.setattr(main, "settings", replace(main.settings, ask_password="secreta"))
    r = client.post("/api/ask", json={"question": "¿Qué es RAG?"}, headers={"X-Access-Key": "incorrecta"})
    assert r.status_code == 401

def test_documents_fallback_to_vector_store(monkeypatch):
    # Sin manifiesto se lista el Vector Store (caso Vercel).
    monkeypatch.setattr(main.SyncService, "load_manifest", staticmethod(lambda: {"vector_store_id": "vs_1", "documents": {}}))
    monkeypatch.setattr(main.SyncService, "remote_documents", staticmethod(lambda store: [{"name": "a.pdf", "url": None}]))
    monkeypatch.setattr(main, "settings", replace(main.settings, openai_api_key="sk-test", vector_store_id=""))
    r = client.get("/api/documents").json()
    assert r["indexed"] == 1 and r["documents"][0]["name"] == "a.pdf"
