"""Punto de entrada para Vercel.

Vercel importa app.py con el nombre de módulo "app", lo que tapa al paquete app/
y rompe `from app.main import app`. Este archivo tiene otro nombre y evita el choque.
En local se sigue usando `python app.py`.
"""
from app.main import app
