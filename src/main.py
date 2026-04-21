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
main.py

Panel de control para el servidor de exámenes Exam-Web by Naidel.
Permite configurar el origen de datos, parámetros de red y ciclo
de vida del servidor web, manteniéndolo accesible desde la bandeja
del sistema de Windows.

Autor: Tú 🙂
"""

import json
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from typing import Dict, Optional
import threading
import webbrowser
import pystray
from PIL import Image
from pystray import MenuItem as TrayItem
from collections import deque
from datetime import datetime
from threading import Thread

import app_meta
from ui_about import AboutDialog
from exam_server import run_server, stop_flask_server

server_thread = None
server_running = False  

# ============================================================
# LOG FILE
# ============================================================
LOG_FILE = Path("exam-web.log")

# ============================================================
# CONSTANTES Y VARIABLES GLOBALES
# ============================================================

CONFIG_FILE: Path = Path("config.json")
DEFAULT_CONFIG: Dict = {
    "data_file": "",
    "port": 5000,
    "protocol": "HTTP",
    "cert_file": "",
    "key_file": "",
    "auto_start_server": False,
    "start_minimized": False,
}

tray_icon: Optional[pystray.Icon] = None

# ============================================================
# CLASES
# ============================================================

class LogManager:
    def __init__(self, max_lines=2000):
        self.lock = threading.Lock()
        self.buffer = deque(maxlen=max_lines)
        self.console_window = None

        # Guardar stdout real SI existe (PyInstaller puede ponerlo a None)
        self.real_stdout = sys.__stdout__ if sys.__stdout__ else None

        # Abrimos fichero de log
        self.log_file = open(LOG_FILE, "a", encoding="utf-8")

    def write(self, text):
        if not text:
            return

        # 🔥 PASO CLAVE: convertir bytes → str
        if isinstance(text, bytes):
            try:
                text = text.decode("utf-8", errors="replace")
            except Exception:
                text = str(text)

        with self.lock:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")

            if not text.startswith("["):
                text = timestamp + text

            # 1️⃣ Guardar en fichero
            self.log_file.write(text)
            self.log_file.flush()

            # 2️⃣ Guardar en memoria
            self.buffer.append(text)

            # 3️⃣ Consola en vivo (Tkinter)
            if self.console_window:
                self.console_window.append_text(text)

            # 4️⃣ Consola real (si existe)
            if self.real_stdout:
                try:
                    self.real_stdout.write(text)
                    self.real_stdout.flush()
                except UnicodeEncodeError:
                    safe_text = text.encode(
                        self.real_stdout.encoding or "cp1252",
                        errors="replace"
                    ).decode(self.real_stdout.encoding or "cp1252")
                    self.real_stdout.write(safe_text)
                    self.real_stdout.flush()

    def flush(self):
        pass

    def attach_console(self, console_window):
        with self.lock:
            self.console_window = console_window
            # Cargar histórico al abrir la consola
            for line in self.buffer:
                self.console_window.append_text(line)

    def detach_console(self):
        with self.lock:
            self.console_window = None        

    def shutdown(self):
        """
        Desconecta recursos dependientes de la UI antes de cerrar la aplicación.
        """
        with self.lock:
            self.console_window = None


class LogConsole(tk.Toplevel):
    def __init__(self, master, log_manager: LogManager):
        super().__init__(master)
        self.log_manager = log_manager

        self.title("Consola de logs")
        self.geometry("900x400")

        self.text = tk.Text(self, wrap="word", state="disabled")
        self.text.pack(fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Conectar al logger
        self.log_manager.attach_console(self)

    def append_text(self, text):
        self.text.configure(state="normal")
        self.text.insert("end", text)
        self.text.see("end")
        self.text.configure(state="disabled")

    def on_close(self):
        self.log_manager.detach_console()
        self.destroy()
        
# ============================================================
# CONFIGURACIÓN (JSON)
# ============================================================

def load_config() -> Dict:
    """
    Load configuration from config.json if present.
    If the file is missing or corrupted, default values are used.

    Returns
    -------
    Dict
        Configuration dictionary.
    """
    if CONFIG_FILE.exists():
        try:
            stored = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return {**DEFAULT_CONFIG, **stored}
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict) -> None:
    """
    Persist the configuration to config.json.

    Parameters
    ----------
    config : Dict
        Configuration dictionary to persist.
    """
    CONFIG_FILE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ============================================================
# UTILIDADES
# ============================================================

def app_base_dir() -> Path:
    """
    Devuelve el directorio donde está el ejecutable o main.py.

    - python main.py  -> carpeta del proyecto
    - Exam-Web.exe    -> carpeta del exe (NO _MEIPASS)
    """
    return Path(sys.argv[0]).resolve().parent


def open_help_html():
    """Abre la ayuda de la aplicación (HTML local)."""

    def _show():
        # Directorio raíz del programa (donde está main.py)
        base_dir = Path(__file__).resolve().parent

        # Ruta al fichero de ayuda
        help_file = base_dir / "docs" / "index.html"

        if not help_file.exists():
            print(f"❌ No se encuentra la ayuda: {help_file}")
            return

        url = help_file.as_uri()

        print(f"🌐 Abriendo página de ayuda del programa: {url}")
        webbrowser.open(url)

    # Ejecutar SIEMPRE en el hilo de Tkinter
    root.after(0, _show)

def open_exam_home():
    """Abre el navegador en la página principal del examen según la configuración actual."""

    def _show():
        # Comprobación de servidor
        if not server_thread or not server_thread.is_alive():
            messagebox.showwarning(
                "Servidor no iniciado",
                "El servidor no está en ejecución.\n\n"
                "Inícialo antes de abrir el examen."
            )
            return

        protocol = protocol_var.get().lower()
        port = port_var.get().strip() or "5000"
        url = f"{protocol}://127.0.0.1:{port}/"

        print(f"🌐 Abriendo página principal del examen: {url}")
        webbrowser.open(url)

    # ✅ Ejecutar SIEMPRE en el hilo de Tkinter
    root.after(0, _show)

def open_about_dialog():
    """Muestra el diálogo 'Acerca de...'."""
    show_about_dialog()

def detect_data_source(path: str) -> str:
    """
    Detect data source type based on file extension.

    Parameters
    ----------
    path : str
        Path to the data file.

    Returns
    -------
    str
        Human-readable data source name.
    """
    extension = Path(path).suffix.lower()
    if extension in (".xlsx", ".xls", ".xlsm"):
        return "Excel"
    if extension in (".mdb", ".accdb"):
        return "Access"
    if extension in (".db", ".sqlite"):
        return "SQLite"
    return "Desconocido"


def position_window_bottom_right(window: tk.Tk, margin: int = 100) -> None:
    """
    Position the given Tk window at the bottom-right corner of the screen.

    Parameters
    ----------
    window : tk.Tk
        Tkinter root window.
    margin : int
        Margin to screen borders in pixels.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = screen_width - width - margin
    y = screen_height - height - margin
    window.geometry(f"+{x}+{y}")


# ============================================================
# SERVIDOR
# ============================================================

def start_server():
    global server_thread
    global server_running

    # Evitar doble arranque
    if server_thread and server_thread.is_alive():
        print("ℹ️ El servidor ya está en ejecución")
        return

    cfg = current_config()

    if not cfg["data_file"]:
        messagebox.showwarning(
            "Datos no definidos",
            "Selecciona un fichero de datos antes de iniciar el servidor."
        )
        return
    
    def _run():
        #try:
        run_server(
            data_file=cfg["data_file"],
            port=cfg["port"],
            protocol=cfg["protocol"],
            cert_file=cfg["cert_file"],
            key_file=cfg["key_file"],
        )
        #except Exception as e:
        #    print(f"❌ Error en el servidor: {e}")
        #    status_var.set("❌ Error en el servidor")

    # 🔥 AQUÍ está la clave: el servidor va en un hilo
    
    server_thread = Thread(target=_run, daemon=True)
    server_thread.start()
    
    server_running = True
    status_var.set(f"🟢 Servidor en ejecución en puerto {cfg['port']}")
    print(f"🟢 Servidor en ejecución en puerto {cfg['port']}")

def stop_server():
    global server_running

    if not server_running:
        print("ℹ️ El servidor ya está parado")
        return

    stop_flask_server()

    server_running = False
    status_var.set("🔴 Servidor parado")
    print("🔴 Servidor parado")


# ============================================================
# BANDEJA DEL SISTEMA (SYSTRAY)
# ============================================================

def create_systray_icon(root: tk.Tk) -> None:
    global tray_icon

    def restore_window():
        root.deiconify()
        root.lift()
        root.focus_force()

    def show_window(icon=None, item=None):
        root.after(0, restore_window)

    def exit_application(icon=None, item=None):
        def _close():
            stop_server()
            if tray_icon:
                tray_icon.stop()
            root.quit()
            root.destroy()
        root.after(0, _close)

    icon_path = app_base_dir() / "static" / "Icono.png"
    try:
        if icon_path.exists():
            image = Image.open(icon_path)
        else:
            print(f"⚠️ Icono no encontrado: {icon_path}")
            image = Image.new("RGB", (64, 64), "blue")
    except Exception as e:
        print(f"⚠️ Error cargando icono: {e}")
        image = Image.new("RGB", (64, 64), "blue")
    
    tray_icon = pystray.Icon(
        "Exam-Web by Naidel",
        image,
        "Servidor de Exámenes Exam-Web by Naidel",
        menu=pystray.Menu(
            TrayItem(
                "Mostrar",
                show_window,
                default=True,   # ✅ CLAVE ABSOLUTA
            ),
            TrayItem("Iniciar examen", open_exam_home),
            TrayItem("Ayuda", open_help_html),
            TrayItem("Acerca de...", open_about_dialog),
            TrayItem("Salir", exit_application),
        ),
    )

    tray_icon.run_detached()


# ============================================================
# INTERFAZ GRÁFICA
# ============================================================


def browse_data_file() -> None:
    """Open file dialog to select a data file."""
    file_path = filedialog.askopenfilename(
        title="Seleccionar fichero de datos",
        filetypes=[
            ("Datos soportados", "*.xlsx *.xls *.xlsm *.mdb *.accdb *.db *.sqlite"),
            ("Todos los ficheros", "*.*"),
        ],
    )
    if file_path:
        data_file_var.set(file_path)
        data_source_var.set(detect_data_source(file_path))


def browse_cert_file() -> None:
    """Select TLS certificate file."""
    path = filedialog.askopenfilename(title="Seleccionar cert.pem")
    if path:
        cert_var.set(path)


def browse_key_file() -> None:
    """Select TLS private key file."""
    path = filedialog.askopenfilename(title="Seleccionar key.pem")
    if path:
        key_var.set(path)


def minimize_to_tray() -> None:
    """Hide the main window (send to system tray)."""
    save_config(current_config())
    root.withdraw()


def current_config() -> Dict:
    """
    Build current configuration dictionary from UI state.

    Returns
    -------
    Dict
        Current configuration values.
    """
    return {
        "data_file": data_file_var.get(),
        "port": int(port_var.get() or 5000),
        "protocol": protocol_var.get(),
        "cert_file": cert_var.get(),
        "key_file": key_var.get(),
        "auto_start_server": auto_start_var.get(),
        "start_minimized": start_minimized_var.get(),
    }

def exit_program():
    print("🚪 Cerrando aplicación...")

    # Parar servidor si está activo
    try:
        if server_running:
            stop_flask_server()
    except Exception:
        pass

    # Logger
    try:
        log_manager.shutdown()
    except Exception:
        pass

    # Systray
    try:
        if tray_icon:
            tray_icon.stop()
    except Exception:
        pass

    root.quit()
    root.destroy()

def show_main_window(icon=None, item=None):
    print("🖱️ Doble clic en el icono de la bandeja")

    root.after(0, restore_window)
    
def restore_window():
    root.deiconify()
    root.lift()
    root.focus_force()

def show_about_dialog():
    """
    Muestra el diálogo 'Acerca de…' de Exam‑Web.
    Evita abrir múltiples instancias simultáneas.
    """
    global about_dialog

    if about_dialog is None or not about_dialog.winfo_exists():
        about_dialog = AboutDialog(root)
    else:
        about_dialog.lift()
        about_dialog.focus_force()

def resource_path(relative_path: str) -> Path:
    """
    Devuelve la ruta absoluta a un recurso, compatible con ejecución normal
    y con aplicaciones empaquetadas con PyInstaller.
    """
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS
        base_path = Path(sys._MEIPASS)  # type: ignore
    except Exception:
        # Ejecución normal
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path
    
# ============================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================================

log_manager = LogManager()
sys.stdout = log_manager
sys.stderr = log_manager

config = load_config()

log_console_window = None
about_dialog = None

print(f"== {app_meta.APP_NAME} ==")
print(f"Versión {app_meta.APP_VERSION} | Build {app_meta.APP_BUILD}")
print(f"Licencia: {app_meta.__license__}")

def open_log_console():
    global log_console_window
    if log_console_window is None or not log_console_window.winfo_exists():
        log_console_window = LogConsole(root, log_manager)
    else:
        log_console_window.lift()

root = tk.Tk()
root.title(f"{app_meta.APP_NAME} (v.{app_meta.APP_VERSION}-{app_meta.APP_BUILD})")


try:
    icon_path = app_base_dir() / "static" / "Icono.png"
    if icon_path.exists():
        icon = tk.PhotoImage(file=str(icon_path))
        root.iconphoto(True, icon)
    else:
        print(f"⚠️ Icono no encontrado: {icon_path}")
except Exception as e:
    print(f"⚠️ No se pudo cargar el icono de la aplicación: {e}")

root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

def on_ctrl_c(event=None):
    print("⌨️ CTRL+C detectado")
    exit_program()
    
root.bind_all("<Control-c>", on_ctrl_c)

# Variables vinculadas a la UI
data_file_var = tk.StringVar(value=config["data_file"])
data_source_var = tk.StringVar(
    value=detect_data_source(config["data_file"]) if config["data_file"] else ""
)
port_var = tk.StringVar(value=str(config["port"]))
protocol_var = tk.StringVar(value=config["protocol"])
cert_var = tk.StringVar(value=config["cert_file"])
key_var = tk.StringVar(value=config["key_file"])
auto_start_var = tk.BooleanVar(value=config["auto_start_server"])
start_minimized_var = tk.BooleanVar(value=config["start_minimized"])
status_var = tk.StringVar(value="🔴 Servidor parado")

# Layout
row = 0
tk.Label(root, text="Fichero de datos").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=data_file_var, width=40).grid(row=row, column=1)
tk.Button(root, text="Examinar", command=browse_data_file).grid(row=row, column=2)

row += 1
tk.Label(root, text="Origen detectado").grid(row=row, column=0, sticky="w")
tk.Label(root, textvariable=data_source_var).grid(row=row, column=1, sticky="w")

row += 1
tk.Label(root, text="Puerto").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=port_var).grid(row=row, column=1, sticky="w")

row += 1
tk.Label(root, text="Protocolo").grid(row=row, column=0, sticky="w")
tk.OptionMenu(root, protocol_var, "HTTP", "HTTPS").grid(row=row, column=1, sticky="w")

row += 1
tk.Label(root, text="Certificado (cert.pem)").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=cert_var, width=40).grid(row=row, column=1)
tk.Button(root, text="Examinar", command=browse_cert_file).grid(row=row, column=2)

row += 1
tk.Label(root, text="Clave (key.pem)").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=key_var, width=40).grid(row=row, column=1)
tk.Button(root, text="Examinar", command=browse_key_file).grid(row=row, column=2)

row += 1
tk.Checkbutton(
    root, text="Iniciar servidor automáticamente", variable=auto_start_var
).grid(row=row, column=0, columnspan=2, sticky="w")

row += 1
tk.Checkbutton(
    root, text="Iniciar programa minimizado", variable=start_minimized_var
).grid(row=row, column=0, columnspan=2, sticky="w")

row += 1

# Zona de botones
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=10)

tk.Button(
    buttons_frame,
    text="► Iniciar servidor",
    command=start_server
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="🟥 Parar servidor",
    command=stop_server
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="📜 Ver log",
    command=open_log_console
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="💾 Guardar",
    command=lambda: save_config(current_config()),
    width=12
).pack(side="left", padx=5)

tk.Button(
    buttons_frame,
    text="🚪 Salir",
    command=exit_program,
    width=12
).pack(side="left", padx=5)

row += 1

# Estado del servidor (debajo de los botones)
tk.Label(root, textvariable=status_var).grid(row=row, column=0, columnspan=2, sticky="w")

# Posicionar ventana
position_window_bottom_right(root)

# Crear bandeja del sistema
create_systray_icon(root)

# Arranque automático
if auto_start_var.get():
    start_server()

if start_minimized_var.get():
    root.withdraw()

root.mainloop()