<div align="center">

# 🚖 App-Viajes  
### Plataforma de gestión de viajes — Cliente & Conductor  
Desarrollada con **Python + Flask + SQLite + Flask-Babel**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Estado-En%20Desarrollo-success)]()

</div>

---

## 📌 Descripción

**App-Viajes** es una aplicación web para gestionar viajes entre **clientes** y **conductores**.  
Funciones principales: registro, login, solicitar viaje, ver/cancelar viajes y soporte multilenguaje (ES/EN).

---

## ✨ Características destacadas

- Registro y autenticación para **cliente** y **conductor**.  
- Solicitud y gestión de viajes (crear, listar, cancelar).  
- Internacionalización con **Flask-Babel** (Español / Inglés).  
- Base de datos **SQLite** ligera incluida.  
- Plantillas organizadas y estilo CSS sencillo.

---

## ⚙️ Requisitos (local)

- Python 3.8+  
- pip (gestor de paquetes)

Instalar dependencias (recomendado en virtualenv):

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

## Si no usaste requirements.txt:
pip install flask flask-babel 

🚀 Ejecutar la app (local)
python app.py

🌐 Idiomas

Cambiá el idioma desde la UI (es / en).
Las traducciones se encuentran en translations/ y se compilan con:

pybabel compile -d translations

🛠️ Planes futuros / mejoras

Panel admin y asignación automática de conductor

Integración con API de mapas y rutas

Integración con pagos (MercadoPago)

Tests unitarios y CI (GitHub Actions)

📬 Autor

Enzo Gutiérrez
Proyecto personal

📄 Licencia

App-Viajes — MIT License. Ver archivo LICENSE.