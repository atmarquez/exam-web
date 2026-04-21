**Language:** English | [Español](README_ES.md)

# 📝 Exam‑Web by Naidel

![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![Backend](https://img.shields.io/badge/Backend-Flask-black.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Release](https://img.shields.io/badge/Release-v0.85.5-orange.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/atmarquez/exam-web)
![Last commit](https://img.shields.io/github/last-commit/atmarquez/exam-web)


**Exam‑Web** is a desktop application for Windows that allows you to manage and run a **local web‑based exam server**, designed for training, self‑assessment and exam simulation.

The project separates **server control (Windows GUI)** from the **exam experience (web interface)**, providing a clean, flexible and reusable study tool.

---

## 🚀 Features

### 🖥️ Windows Desktop Control
- Start and stop the web exam server
- Select question database (Excel, Access or SQLite)
- Configure port and protocol (HTTP / HTTPS)
- Optional TLS configuration for HTTPS
- Auto‑start server
- Minimize to system tray
- Integrated live log console
- Persistent configuration (`config.json`)

### 🌐 Web Exam Interface
- Multiple‑choice questions
- Answer randomization
- Per‑question and session timers
- Progressive visual alerts
- Session and global statistics
- Question review flags
- Access to glossary, graphics and annotations
- Calculator and database viewer

---

## 🧱 Supported Data Sources

- ✅ Microsoft Excel (`.xls`, `.xlsx`, `.xlsm`)
- ✅ Microsoft Access (`.mdb`, `.accdb`)
- ✅ SQLite (`.db`, `.sqlite`)

The data source is detected automatically.

---

## 🛠️ Technologies Used

- Python 3
- Tkinter (desktop GUI)
- Flask (web server)
- Werkzeug (embedded WSGI server)
- pystray (system tray)
- Pillow (images)
- HTML / CSS / JavaScript

---

## ▶️ How to Run (development)

```bash
python main.py
```

---

## 📦 Building the Windows Executable

The project is designed to be packaged with **PyInstaller**.

```bash
pyinstaller main.spec
```

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0 or later (GPL‑3.0‑or‑later)**.

---

## ❤️ Support the Project

👉 https://paypal.me/atmarquez

© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)

---

🧠 Designed for study, practice and real‑exam simulation.
