# Changelog

All notable changes to this project will be documented in this file.

The format is based on **Keep a Changelog**, and this project adheres to
**Semantic Versioning** where applicable.

---

## [0.85.5] – 2026-04-21

### ✅ Added
- Embedded Flask web server running inside the desktop application.
- Integrated Windows GUI to start and stop the web exam server.
- System tray support (minimize, restore, exit).
- Live log console embedded in the GUI.
- Support for static web assets (images, help pages).
- Local HTML help pages (ES / EN).
- “About” dialog with project metadata.
- Automatic data source detection (Excel, Access, SQLite).
- Per‑question and per‑session timers with visual alerts.
- Question review flagging system.
- Integrated calculator and database viewer in the web UI.

### 🔧 Changed
- Server architecture redesigned to run in a background thread instead of an external process.
- Logging system adapted to support both `str` and `bytes` output streams.
- Server lifecycle fully controlled from the main application.
- Static files now served explicitly for compatibility with embedded WSGI server.
- Improved robustness when running as a PyInstaller executable.

### 🐞 Fixed
- Server start/stop inconsistencies when packaged as an executable.
- Multiple instance spawning issues.
- Logging crashes caused by encoding mismatches.
- Clean shutdown errors related to destroyed Tkinter widgets.
- Missing static assets in embedded server mode.
- Incorrect server state detection in the GUI.

### 🧹 Removed
- Dependency on `subprocess` for server execution.
- Use of command‑line flags for internal server control.
- Automatic script self‑relaunching logic.

---

## [0.8.x] – 2025-2026 (pre‑embedded architecture)

### Added
- Initial Flask‑based web interface.
- Question randomization and statistics tracking.
- Excel‑backed question repository.
- Basic session management.
- Review and reset mechanisms.

### Changed
- Progressive refactoring toward modular data sources.

### Fixed
- Multiple logic and persistence edge cases during question progression.

---

## [0.5.x] – 2024 (initial development)

### Added
- First working prototype based on Excel + VBA logic.
- Basic web‑based question flow.
- Core data model and repositories.

---

## Notes

- Versions prior to `0.85.5` were experimental and not packaged for end users.
- Version `0.85.5` marks the first **fully self‑contained and distributable desktop release**.

---
© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)