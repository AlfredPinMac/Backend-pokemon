# Reporte de Vulnerabilidades con Nuclei - Pokémon Backend API

## 📋 Resumen del Escaneo
- **Objetivo analizado:** `http://127.0.0.1:5000` (Pokémon Backend API Service)
- **Herramienta:** ProjectDiscovery Nuclei v3.11.1
- **Fecha:** Octubre 2026
- **Total de plantillas evaluadas:** 6,330+ (CVEs, exposures, misconfigurations, auth, APIs)
- **Total de hallazgos:** 14 alertas (Informational / Misconfiguration)

---

## 🔍 Hallazgos Principales

### 1. CORS Misconfiguration: Arbitrary Origin Reflection
- **Severidad:** Media / Info
- **Detalle:** Nuclei verificó que el endpoint responde favorablemente a orígenes cruzados arbitrarios (`cors_origin="https://127.0.0.1%60.hwfm2.com"`).
- **Impacto:** Permite que aplicaciones web de terceros hagan llamadas autenticadas si las credenciales o tokens se comparten indebidamente.
- **Remediación:** Limitar la política CORS explícitamente al origen del Dashboard frontend.

### 2. Exposición de Endpoints de Documentación
- **Rutas identificadas:**
  - `GET /docs` (Swagger UI interactivo)
  - `GET /redoc` (ReDoc)
  - `GET /openapi.json` (Esquema OpenAPI)
- **Severidad:** Info / Reconocimiento
- **Impacto:** Permite a usuarios no autenticados conocer los endpoints protegidos (`/api/pokemons`, `/api/pokemons/{id}`), los esquemas de datos requeridos y la necesidad del token JWT `Bearer`.
- **Remediación:** Configurar `docs_url=None`, `redoc_url=None`, `openapi_url=None` en FastAPI para entornos productivos.

### 3. Cabeceras de Seguridad HTTP Faltantes
Faltan cabeceras defensivas para mitigar ataques basados en navegador:
- `Content-Security-Policy (CSP)`
- `Strict-Transport-Security (HSTS)`
- `X-Frame-Options`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy`
- `Permissions-Policy`
- `Cross-Origin-Opener-Policy (COOP)`
- `Cross-Origin-Embedder-Policy (COEP)`
- `Cross-Origin-Resource-Policy (CORP)`
- `X-Permitted-Cross-Domain-Policies`

---

## 📁 Archivos Relacionados
- `reports/nuclei-backend-results.jsonl`: Archivo JSON Lines con detalle técnico completo y solicitudes HTTP.
- `reports/nuclei-backend-report.txt`: Registro de coincidencias.
