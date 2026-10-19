# 2.3 Agente documental con Google Drive — Archivo TIC IA

Proyecto académico de **Inteligencia artificial aplicada a las TIC**, Tecnológico Nacional de México, campus Pachuca. Continuación de **2.2 Agente investigador**: se reemplaza la búsqueda pública Web Search por recuperación documental de **Google Drive**, **OpenAI Vector Stores** y **File Search (RAG)**.

## Propósito pedagógico

El alumno comprenderá que una organización necesita consultar documentos propios y autorizados, no solamente Internet. Identificará el papel de OAuth, Google Drive API, sincronización, indexación semántica, recuperación de contexto, respuestas sustentadas y trazabilidad mediante fuentes. Comparará respuestas **sin** y **con** acceso documental, observará qué sucede al modificar una fuente y realizará todas las pruebas iniciales en **localhost**. El despliegue a Vercel es un **reto autónomo**, no una configuración lista para producción.

## Arquitectura

- `app/main.py`: FastAPI, endpoints REST, frontend estático y protección local de sincronización.
- `app/core/config.py`: configuración y secretos cargados desde `.env`.
- `app/models/documento.py`: modelos de solicitud y respuesta.
- `app/services/drive_service.py`: OAuth Desktop, listado limitado a una carpeta y descarga/exportación de archivos.
- `app/services/sync_service.py`: Vector Store, manifiesto de archivos, altas, cambios y bajas.
- `app/services/agent_service.py`: Responses API + File Search y fuentes verificadas por anotaciones de archivo.
- `index.html` y `assets/`: interfaz Bootstrap 5 y clases JavaScript.
- `data/manifest.json`: estado local del índice (no se publica).

## 1. Requisitos

Python 3.11+, VS Code, Git, cuentas de Google Cloud y OpenAI API con créditos, navegador y documentos de prueba autorizados. **Las claves y los archivos de Drive no se incluyen en el ZIP.**

## 2. Configuración Google Drive

1. En [Google Cloud Console](https://console.cloud.google.com/), crea un proyecto y habilita **Google Drive API**.
2. Configura **Google Auth Platform**, pantalla de consentimiento y usuarios de prueba si corresponde.
3. Crea credenciales OAuth 2.0 de tipo **Desktop app** y descarga el archivo a la raíz del proyecto como `credentials.json`.
4. Crea una carpeta de Google Drive con **al menos cinco** documentos autorizados. Admite PDF, TXT y Google Docs nativos. Extrae el ID de su URL `/folders/ID`.
5. Este ejercicio utiliza el alcance `drive.readonly` para lectura; puede exigir validaciones adicionales al distribuir una app real. Usa una cuenta y una carpeta de laboratorio sin datos personales.

## 3. Preparar proyecto en Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env`: define `OPENAI_API_KEY`, un `OPENAI_MODEL` compatible con File Search y `GOOGLE_DRIVE_FOLDER_ID`. `VECTOR_STORE_ID` se deja vacío la primera vez: el sistema lo guardará en el manifiesto. No insertes claves en el código ni en el navegador.

## 4. Ejecutar localmente

```powershell
python app.py
```

Abre <http://127.0.0.1:5000>. Usa **Sincronizar desde Drive** para autenticar Google, descargar/exportar los archivos autorizados e indexarlos. La primera ejecución abre el navegador OAuth en la computadora donde está corriendo Python. Después escribe preguntas sobre el contenido. Para ensayar recuperación, desactiva **File Search (RAG)** y repite exactamente la misma pregunta.

**Importante:** la sincronización usa una solicitud HTTP en localhost. Si estableces `LOCAL_ADMIN_KEY`, proporciona la cabecera `X-Admin-Key` mediante Thunder Client para `/api/sync` (el botón web no envía claves administrativas). Ejecuta el backend en `127.0.0.1`, no en `0.0.0.0`.

## 5. Endpoints

| Método | Ruta | Función |
|---|---|---|
| GET | `/api/health` | Comprueba configuración y servidor. |
| GET | `/api/documents` | Documentos ya indexados (manifiesto local). |
| POST | `/api/sync` | Indexa cambios, requiere cliente desde loopback. |
| POST | `/api/ask` | Pregunta con `question` y `use_search`. |

Ejemplo JSON para Thunder Client:

```json
{"question": "¿Qué documentos tratan sobre AWS RDS?", "use_search": true}
```

## 6. Experimentos

1. Ejecuta una pregunta muy específica presente en los archivos **sin File Search**.
2. Repite **con File Search**: inspecciona contenido y fuentes (anotaciones verificadas).
3. Prueba temas ausentes: el agente debe declarar insuficiencia de información.
4. Agrega un documento con un dato singular, sincroniza y vuelve a preguntar.
5. Modifica un documento, vuelve a sincronizar y verifica que no se duplican registros en el manifiesto.
6. Elimina un documento de prueba del Drive autorizado, sincroniza y comprueba que desaparece del manifiesto.

**Limitaciones:** las búsquedas RAG pueden generar errores; comprueba siempre las respuestas contra las fuentes. La eliminación del índice tiene **consistencia eventual** y puede tardar en reflejarse. Los resultados sin citas explícitas no se presentan como fuentes. La actualización de un mismo archivo puede crear cargos transitorios mientras se reemplaza el anterior.

## 7. Pruebas automáticas

```powershell
pytest -q
```

Las pruebas son locales y no requieren claves reales ni consumen OpenAI.

## 8. Git/GitHub y reto autónomo Vercel

```powershell
git init
git add .
git commit -m "chore: estructura inicial del agente documental"
```

Publica solamente el código; confirma `.gitignore`. **NO publiques este proyecto en Vercel sin adaptaciones de seguridad.** OAuth Desktop, `token.json`, `manifest.json`, la ausencia de sesiones de usuario y el endpoint de preguntas no son adecuados para Internet abierto. Para producción, investiga OAuth tipo **Web application**, redirecciones autorizadas, sesiones, almacenamiento persistente de tokens, control de acceso documental por usuario, protección del endpoint `/api/ask`, persistencia compartida del índice y cuotas. Los archivos locales de una función serverless pueden ser efímeros. Las variables de entorno deben configurarse en la plataforma, nunca en el frontend.

## 9. Costos y privacidad

OpenAI cobra por el uso de modelos, búsqueda y almacenamiento según su tarifario vigente. No subas a OpenAI documentos confidenciales, datos personales o material sin permiso del propietario. El material descargado se transmite a OpenAI para indexación. Revoca y rota cualquier credencial filtrada, incluso si ya fue borrada de GitHub.

## Entrega

Repositorio GitHub con historia de commits, URL de Vercel si culminas el reto (o documentación del bloqueo), y conclusiones sobre OAuth, Google Drive API, RAG, File Search, FastAPI, OOP, Git/GitHub y seguridad.

## 10. Reto Vercel: adaptaciones realizadas

**Producción:** <https://agente-documental-tic-rouge.vercel.app> · **Repositorio:** <https://github.com/l24200197-commits/agente-documental-tic>

Se eligió una **arquitectura híbrida**: la sincronización Drive → Vector Store se ejecuta solo en localhost (OAuth Desktop + `token.json`), y Vercel únicamente consulta el Vector Store ya indexado. Así Vercel nunca guarda tokens de Google.

| Problema en Vercel | Adaptación |
|---|---|
| Vercel importa `app.py` como módulo `app` y tapa el paquete `app/`. | Punto de entrada `api/index.py` (`from app.main import app`) y `vercel.json` con `rewrites` de todas las rutas hacia la función e `includeFiles` para `index.html`, `assets/` y `app/`. |
| Sistema de archivos efímero: no existe `data/manifest.json`. | `VECTOR_STORE_ID` como variable de entorno; `/api/documents` lista los archivos del Vector Store si no hay manifiesto; las citas usan el nombre real del archivo subido. |
| `/api/ask` público consumiría la API Key de cualquiera. | Contraseña compartida `ASK_PASSWORD` (cabecera `X-Access-Key`, comparación con `hmac.compare_digest`). |
| `/api/sync` requiere OAuth en el navegador del servidor. | Sigue protegido por `local_only`: en Vercel responde 403. |
| Secretos locales. | `.vercelignore` excluye `.env`, `credentials.json`, `token.json` y `data/manifest.json`. |

**Variables de entorno en Vercel (Production):** `OPENAI_API_KEY`, `OPENAI_MODEL`, `VECTOR_STORE_ID`, `GOOGLE_DRIVE_FOLDER_ID`, `ASK_PASSWORD`. Ninguna aparece en `index.html` ni en `assets/js`; el navegador solo envía la contraseña que escribe el usuario.

**Despliegue:** `vercel --prod` desde la raíz (Vercel CLI). Error encontrado: `ModuleNotFoundError: app.main` por el choque de nombres descrito arriba. Se corrigió con `api/index.py`.

**Puerto local:** en macOS el puerto 5000 lo ocupa el Receptor AirPlay; se usa `PORT=5001` en `.env`.

### OAuth para producción (investigación, no implementado)

El ZIP usa `InstalledAppFlow` (cliente **Desktop**), que abre un navegador en la máquina que ejecuta Python y guarda `token.json` en disco. En serverless no hay navegador ni disco persistente: cada invocación puede iniciar en un contenedor nuevo y perder `token.json` y `manifest.json`. Para sincronizar desde Vercel haría falta:

1. Un cliente OAuth de tipo **Web application** con URI de redirección autorizada (`https://<dominio>/api/oauth/callback`) y el flujo `google_auth_oauthlib.flow.Flow` con parámetro `state` contra CSRF.
2. **Sesiones** de usuario (cookie firmada `HttpOnly`, `Secure`, `SameSite=Lax`) para saber quién autorizó.
3. **Almacenamiento persistente y cifrado** del refresh token y del manifiesto (por ejemplo Vercel KV/Upstash Redis, Postgres o Blob), nunca en el sistema de archivos de la función.
4. Control de acceso por usuario a las carpetas de Drive, cuotas y límites de consumo en `/api/ask`.
5. Mover la sincronización a una tarea en segundo plano (Vercel Cron o cola), porque la indexación puede superar el tiempo máximo de la función.

Por estas razones el bloqueo se documenta y la sincronización permanece local.

## 11. Evidencias

- Experimentos y comparación sin/con File Search: [docs/EXPERIMENTOS.md](docs/EXPERIMENTOS.md)
- Conclusiones: [docs/CONCLUSIONES.md](docs/CONCLUSIONES.md)
