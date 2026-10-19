"""Aplicación académica LOCAL. No desplegar públicamente sin autenticación de usuarios."""
import hmac
from pathlib import Path
from ipaddress import ip_address
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.models.documento import AskRequest, AskResponse
from app.services.sync_service import SyncService
from app.services.agent_service import AgentService

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Archivo TIC IA", version="1.0.0")
app.mount("/assets", StaticFiles(directory=ROOT / "assets"), name="assets")

def local_only(request: Request):
    """Defensa básica para el laboratorio; no equivale a autenticación pública."""
    host = request.client.host if request.client else ""
    try:
        if not ip_address(host).is_loopback: raise ValueError()
    except ValueError:
        raise HTTPException(status_code=403, detail="Sincronización disponible solo desde localhost")
    key = settings.local_admin_key
    if key and request.headers.get("X-Admin-Key") != key:
        raise HTTPException(status_code=401, detail="Clave administrativa incorrecta")

def require_ask_password(request: Request):
    """Contraseña compartida para consultar; la API key de OpenAI nunca sale del servidor."""
    expected = settings.ask_password
    if not expected: return
    given = request.headers.get("X-Access-Key", "")
    if not hmac.compare_digest(given.encode(), expected.encode()):
        raise HTTPException(status_code=401, detail="Contraseña de acceso incorrecta")

@app.get("/")
def index():
    return FileResponse(ROOT / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "configured": bool(settings.openai_api_key and settings.drive_folder_id)}

@app.get("/api/documents")
def documents():
    doc = SyncService.load_manifest()
    items = list(doc.get("documents", {}).values())
    store = settings.vector_store_id or doc.get("vector_store_id")
    # Sin manifiesto (sistema de archivos efímero en Vercel) se consulta el Vector Store.
    if not items and store and settings.openai_api_key:
        try:
            items = SyncService.remote_documents(store)
        except Exception:
            items = []
    return {"documents": items, "indexed": len(items), "vector_store_configured": bool(store)}

@app.post("/api/ask", response_model=AskResponse, dependencies=[Depends(require_ask_password)])
def ask(payload: AskRequest):
    try:
        if not settings.openai_api_key: raise ValueError("Falta OPENAI_API_KEY")
        return AgentService().ask(payload.question, payload.use_search)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=502, detail="Error al consultar OpenAI. Revisa el registro local.")

@app.post("/api/sync", dependencies=[Depends(local_only)])
def sync():
    try:
        if not settings.openai_api_key: raise ValueError("Falta OPENAI_API_KEY")
        return SyncService().sync()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Sincronización fallida: {exc}")
