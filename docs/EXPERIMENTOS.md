# Experimentos — Archivo TIC IA

Ejecutados en localhost (`http://127.0.0.1:5001`) el 2026-10-18 con `gpt-4.1-mini` y 6 documentos indexados de la carpeta *2.3 Agente documental*:

`tec01_aws_rds.pdf`, `tec02_docker_contenedores.pdf`, `tec03_redes_vlan_direccionamiento.pdf`, `tec04_ciberseguridad_owasp.pdf`, `tec05_iot_mqtt.pdf`, `tec06_git_github_flujo.pdf`.

## Pruebas automáticas

```
$ pytest -q
7 passed
```

## Experimentos A y B: misma pregunta sin y con File Search

**Pregunta:** «¿Qué motores de bases de datos soporta AWS RDS según los documentos y qué ventajas menciona?»

| Criterio | A: sin File Search (`use_search=false`) | B: con File Search (`use_search=true`) |
|---|---|---|
| Motores | Aurora, MySQL, MariaDB, PostgreSQL, Oracle, SQL Server (conocimiento general del modelo). | Los mismos seis, con detalles propios del documento (Aurora separa cómputo y almacenamiento; licencias de SQL Server). |
| Ventajas | Genéricas: gestión automatizada, Multi-AZ, escalabilidad, seguridad. | Las del documento: Multi-AZ con conmutación automática, réplicas de lectura, respaldos e instantáneas, VPC, grupos de seguridad, KMS, TLS. |
| Evidencia | Ninguna. Aun así **afirma «Según los documentos indexados»**, sin haber consultado ningún documento. | Recupera fragmentos del Vector Store. |
| Fuentes | Ninguna. | `tec01_aws_rds.pdf` (anotación `file_citation`). |
| Precisión | Correcta en lo general, pero no verificable y con una procedencia falsa. | Ajustada al material del curso y verificable con el enlace a Drive. |

**Observación:** sin RAG el modelo puede responder bien a un tema conocido, pero inventa la procedencia. Por eso la cita verificable importa más que el contenido mismo.

## Consultas documentales (con File Search)

| Tipo | Pregunta | Resultado | Fuentes |
|---|---|---|---|
| Localizar | ¿Qué archivos hablan de AWS RDS? | Identifica un solo archivo y resume su contenido. | `tec01_aws_rds.pdf` |
| Resumir (tema ausente) | Resume qué es VPC Peering según los documentos. | «No se encontró información específica…». Reconoce que la evidencia es insuficiente. | — |
| Comparar | Compara Docker y contenedores con Git y GitHub: objetivos y herramientas. | Comparación por objetivos y conceptos de cada práctica. | `tec02_docker_contenedores.pdf`, `tec06_git_github_flujo.pdf` |

Los enlaces de las fuentes abren los archivos originales en `drive.google.com` (la interfaz solo acepta enlaces https de Drive o Docs).

## Sincronización incremental

| Acción | added | updated | removed | unchanged | errors |
|---|---|---|---|---|---|
| Sincronizar sin cambios | 0 | 0 | 0 | 6 | 0 |
| Agregar documento con dato exclusivo | _pendiente_ | | | | |
| Modificar un documento de prueba | _pendiente_ | | | | |
| Eliminar el documento de prueba | _pendiente_ | | | | |

## Verificación en Vercel

| Prueba | Resultado |
|---|---|
| `GET /api/health` | `{"status":"ok","configured":true}` |
| `GET /api/documents` | 6 documentos (leídos del Vector Store, sin enlaces). |
| `POST /api/ask` sin contraseña | 401 |
| `POST /api/ask` con contraseña («¿Qué es MQTT?») | Respuesta con fuente `tec05_iot_mqtt.pdf`. |
| `POST /api/sync` | 403 (solo localhost) |
| Secretos en el HTML y JS públicos | No aparecen. |

## Conclusión

Recuperar información documental convierte una respuesta plausible en una respuesta comprobable. RAG no elimina las alucinaciones: el modelo puede omitir citas o interpretar mal un fragmento. Sí permite verificar cada afirmación contra el documento original y que el agente reconozca cuando el tema no está en la carpeta autorizada.
