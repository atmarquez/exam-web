
# 📦 Exam‑Web v0.85.5 – Release Notes

**Release date:** April 21, 2026  
**Status:** Stable release

---

## ✨ Overview

Version **v0.85.5** marks a major milestone in the evolution of **Exam‑Web**.  
It is the first **stable and distributable** desktop release, featuring a **fully embedded web exam server**.

---

## ✅ Key Features

- Native Windows desktop application with system tray
- Embedded Flask server (no external processes)
- Clean server start and stop controls
- Complete web‑based exam system
- Reliable static asset loading in packaged executables

---

## 🔧 Technical Improvements

- Complete redesign of server lifecycle
- Removal of `subprocess`‑based execution
- Clean WSGI server shutdown
- Robust logging system
- Identical behavior in Python and PyInstaller builds

---

## 🐞 Fixes

- Multiple instance spawning issues
- Server shutdown problems
- Missing static assets in executable builds
- Encoding issues in logs
- Application shutdown exceptions

---

## ❤️ Support

👉 https://paypal.me/atmarquez

© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)  
Licensed under GPL‑3.0‑or‑later
