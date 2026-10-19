# Conclusiones — Práctica 2.3

**Agentes de IA y File Search.** Un agente documental no busca en Internet. Responde desde una carpeta autorizada de Google Drive que se indexa en un Vector Store de OpenAI. En los experimentos, sin File Search el modelo respondió de forma convincente pero afirmó haber usado «documentos indexados» que nunca consultó. Con File Search la respuesta coincidió con el material del curso y trajo la cita del PDF. Ante un tema ausente (VPC Peering) reconoció que no había evidencia. RAG no elimina los errores, pero los vuelve verificables.

**Drive API y OAuth 2.0.** Drive API solo obtiene los archivos. OAuth decide con qué permiso se obtienen (`drive.readonly`, limitado a una carpeta). La indexación semántica y la generación son etapas distintas que ocurren en OpenAI.

**OOP y FastAPI.** Separar `DriveService`, `SyncService` y `AgentService` permitió probar cada responsabilidad por separado y adaptar el proyecto a Vercel sin tocar el flujo local. FastAPI expone los endpoints, valida las solicitudes con Pydantic y sirve el frontend.

**Git/GitHub.** El historial de commits documenta cada cambio y `.gitignore` evita publicar `.env`, `credentials.json`, `token.json` y el manifiesto. Un secreto que llega a GitHub debe revocarse; no basta con borrarlo.

**Vercel y variables de entorno.** Las funciones serverless no conservan archivos ni pueden abrir un navegador para OAuth Desktop. Por eso se eligió una arquitectura híbrida: la sincronización se hace en local y Vercel consulta el Vector Store configurado mediante variables de entorno. La migración completa requeriría OAuth Web, sesiones y almacenamiento persistente cifrado.

**Seguridad de la API Key.** `OPENAI_API_KEY` vive solo en el servidor (`.env` en local, variables de entorno en Vercel) y nunca llega al navegador. Como `/api/ask` no tenía autenticación, se protegió con una contraseña compartida para que nadie consuma la clave sin autorización.
