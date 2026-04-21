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
app_meta.py

Metadatos globales de la aplicación Servidor de Exámenes Exam-Web by Naidel.

Este fichero centraliza información descriptiva y estática del proyecto,
como nombre, versión, autor y URLs oficiales.

Su objetivo es:
- Evitar constantes duplicadas repartidas por el código.
- Facilitar que la información de "Acerca de..." tenga una única fuente.
- Simplificar el versionado, branding y enlaces del proyecto.

IMPORTANTE:
- Este fichero NO contiene lógica.
- Este fichero NO debe importar otros módulos del proyecto.
- Solo debe contener constantes simples (strings, números).
"""

# Metadato de licencia legible por herramientas y scripts.
# Se declara aquí para reforzar la información legal del proyecto,
# aunque la licencia principal se define también en main.py.
__license__ = "GPL-3.0-or-later"


# ------------------------------------------------------------
# Identidad de la aplicación
# ------------------------------------------------------------

# Nombre completo mostrado al usuario.
# Puede incluir autor o branding si se desea.
APP_NAME = "Servidor de Exámenes Exam-Web by Naidel"
APP_ID = "exam-web"

# Versión de la aplicación.
# RECOMENDACIÓN:
# - Mantener este valor sincronizado con releases y CHANGELOG.
# - Usar un esquema consistente (semver o similar).
APP_VERSION = "0.85.5"
APP_ESTADO = "Estable"

# Identificador de build.
# Suele representar la fecha de compilación o liberación.
# Útil para diagnóstico y soporte.
APP_BUILD = "2026.04.22"

# Descripción corta de la aplicación.
# Se utiliza normalmente en:
# - Diálogos "Acerca de..."
# - Metadatos de instaladores
# - Documentación básica
APP_DESCRIPTION = "El Servidor de Exámenes Exam‑Web by Naidel es una aplicación de escritorio que permite gestionar y lanzar un servidor web de exámenes de forma sencilla, flexible y multiplataforma, orientada a la preparación y práctica de tests tipo examen"

# Autor principal del proyecto.
APP_AUTHOR = "Antonio Teodomiro Márquez Muñoz (Naidel)"

# Email del autor principal del proyecto.
APP_EMAIL = "atmarquez@gmail.com"

# Texto de copyright mostrado al usuario.
# NOTA:
# - No sustituye al encabezado legal de cada fichero.
# - Es meramente informativo / visual.
APP_COPYRIGHT = "© 2024–2026 by Naidel"


# ------------------------------------------------------------
# URLs oficiales del proyecto
# ------------------------------------------------------------

# Página principal del proyecto (si existe).
# Puede ser una web pública o una landing page.
APP_URL_PROJECT = "https://atmarquez.github.io/exam-web/"

# Repositorio de código fuente.
# Normalmente GitHub, GitLab u otro proveedor.
APP_URL_REPO = "https://github.com/atmarquez/exam-web"

# URL para reportar errores o solicitar mejoras.
# Debe apuntar a issues, tickets o sistema similar.
APP_URL_ISSUES = "https://github.com/atmarquez/exam-web/issues"

# Documentación oficial del proyecto.
# Puede ser una web, wiki o directorio dentro del repo.
APP_URL_DOCS = "https://github.com/atmarquez/exam-web/wiki"

# Enlace oficial a la licencia GNU GPL v3.
# Se utiliza habitualmente en diálogos "Acerca de..."
# y avisos legales.
APP_URL_GPL = "https://www.gnu.org/licenses/gpl-3.0.html"

# URL para donar.
APP_URL_DONATE = "https://paypal.me/atmarquez"