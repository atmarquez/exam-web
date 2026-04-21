# This file is part of Servidor de Exámenes Exam-Web by Naidel.
#
# Copyright (C) 2024–2026 by Naidel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
ui_about.py

Diálogo “Acerca de…” para Servidor de Exámenes Exam‑Web (versión Windows).

Este módulo implementa una ventana modal independiente que muestra:
- Identidad de la aplicación
- Metadatos (versión, build, autor, contacto)
- Descripción general
- Enlaces oficiales del proyecto
- Información básica de licencia GPLv3

IMPORTANTE:
- Solo interfaz gráfica (Tkinter)
- No contiene lógica de negocio
- Usa app_meta como fuente única de información
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import app_meta


class AboutDialog(tk.Toplevel):
    """Diálogo 'Acerca de…' de Exam-Web."""

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self.title("Acerca de")
        self.resizable(False, False)
        self.transient(parent)   # Ventana hija
        self.grab_set()           # Modal

        self._build_ui()
        self._center(parent)

    # ---------------------------------------------------------
    # Construcción de la interfaz
    # ---------------------------------------------------------
    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.grid(row=0, column=0)

        # -----------------------------------------------------
        # Título
        # -----------------------------------------------------
        title = ttk.Label(
            main,
            text=app_meta.APP_NAME,
            font=("Segoe UI", 14, "bold"),
            anchor="center",
            justify="center",
        )
        title.grid(row=0, column=0, pady=(0, 6))

        # -----------------------------------------------------
        # Metadatos
        # -----------------------------------------------------
        meta = (
            f"Versión: {app_meta.APP_VERSION}\n"
            f"Build: {app_meta.APP_BUILD}\n"
            f"Autor: {app_meta.APP_AUTHOR}\n"
            f"Contacto: {app_meta.APP_EMAIL}\n"
            f"{app_meta.APP_COPYRIGHT}"
        )

        meta_label = ttk.Label(
            main,
            text=meta,
            justify="center",
            anchor="center",
        )
        meta_label.grid(row=1, column=0, pady=(0, 10))

        # -----------------------------------------------------
        # Descripción
        # -----------------------------------------------------
        desc = ttk.Label(
            main,
            text=app_meta.APP_DESCRIPTION,
            wraplength=420,
            justify="center",
        )
        desc.grid(row=2, column=0, pady=(0, 12))

        # -----------------------------------------------------
        # Enlaces
        # -----------------------------------------------------
        links_frame = ttk.LabelFrame(main, text="Enlaces útiles")
        links_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        def link(text: str, url: str):
            lbl = ttk.Label(
                links_frame,
                text=text,
                foreground="#0066cc",
                cursor="hand2",
            )
            lbl.bind("<Button-1>", lambda e: webbrowser.open(url))
            lbl.pack(anchor="w", padx=10, pady=2)

        link("🌐 Página del proyecto", app_meta.APP_URL_PROJECT)
        link("📄 Repositorio", app_meta.APP_URL_REPO)
        link("🐞 Reportar errores", app_meta.APP_URL_ISSUES)
        link("📘 Documentación", app_meta.APP_URL_DOCS)
        link("⚖ Licencia GNU GPL v3", app_meta.APP_URL_GPL)

        # -----------------------------------------------------
        # Licencia (resumen)
        # -----------------------------------------------------
        lic_frame = ttk.LabelFrame(main, text="Licencia")
        lic_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        lic_text = (
            "Este programa es software libre, distribuido bajo la\n"
            "Licencia Pública General GNU versión 3 (GPLv3).\n\n"
            "Puedes usarlo, estudiar, modificar y redistribuirlo\n"
            "bajo los términos de dicha licencia.\n\n"
            "Se distribuye SIN NINGUNA GARANTÍA."
        )

        ttk.Label(
            lic_frame,
            text=lic_text,
            justify="left",
            wraplength=420,
        ).pack(padx=10, pady=6)

        # -----------------------------------------------------
        # Botón cerrar
        # -----------------------------------------------------
        btn = ttk.Button(main, text="Cerrar", command=self.destroy)
        btn.grid(row=5, column=0, pady=(6, 0))

    # ---------------------------------------------------------
    # Utilidades
    # ---------------------------------------------------------
    def _center(self, _parent=None):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = self.winfo_width()
        height = self.winfo_height()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"+{x}+{y}")
