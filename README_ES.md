**Language:** Español | [English](README.md)

# 📝 Exam‑Web by Naidel

![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![Backend](https://img.shields.io/badge/Backend-Flask-black.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Release](https://img.shields.io/badge/Release-v0.85.5-orange.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/atmarquez/exam-web)
![Last commit](https://img.shields.io/github/last-commit/atmarquez/exam-web)
[![GitHub Pages](https://github.com/atmarquez/exam-web/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/atmarquez/exam-web/actions/workflows/pages/pages-build-deployment)

**Exam‑Web** es una aplicación de escritorio para Windows que permite **gestionar y ejecutar un servidor web local de exámenes**, orientado a entrenamiento, autoevaluación y simulación de exámenes.

El proyecto separa claramente el **control del servidor (aplicación Windows)** de la **experiencia de examen (interfaz web)**.

---

## 🚀 Características

### 🖥️ Aplicación de Control
- Iniciar y detener el servidor web
- Selección de base de datos de preguntas
- Configuración de puerto y protocolo (HTTP / HTTPS)
- Soporte opcional de TLS
- Inicio automático del servidor
- Minimización a la bandeja del sistema
- Consola de logs integrada
- Configuración persistente (`config.json`)

### 🌐 Interfaz Web de Examen
- Preguntas tipo test
- Aleatorización de respuestas
- Temporizadores por pregunta y sesión
- Alertas visuales progresivas
- Estadísticas de sesión y globales
- Marcado de preguntas para revisión
- Acceso a glosario, gráficos y anotaciones
- Calculadora y visor de base de datos

---

## 🧱 Fuentes de Datos Soportadas

- ✅ Microsoft Excel (`.xls`, `.xlsx`, `.xlsm`)
- ✅ Microsoft Access (`.mdb`, `.accdb`)
- ✅ SQLite (`.db`, `.sqlite`)

La fuente de datos se detecta automáticamente.

---

## 🛠️ Tecnologías

- Python 3
- Tkinter
- Flask
- Werkzeug
- pystray
- Pillow
- HTML / CSS / JavaScript

---

## ▶️ Ejecución (desarrollo)

```bash
python main.py
```

---

## 📦 Compilación a ejecutable

```bash
pyinstaller main.spec
```

---

## 📄 Licencia

Licencia **GNU GPL v3 o posterior**.

---

## ❤️ Apoya el proyecto

👉 https://paypal.me/atmarquez

© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)

---

## 🌐 Documentación

The official documentation is available at:

👉 https://atmarquez.github.io/exam-web/

---

🧠 Designed for study, practice and real‑exam simulation.
