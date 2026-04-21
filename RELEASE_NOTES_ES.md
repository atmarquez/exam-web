
# 📦 Exam‑Web v0.85.5 – Notas de la Versión

**Fecha de lanzamiento:** 21 de abril de 2026  
**Estado:** Versión estable

---

## ✨ Descripción general

La versión **v0.85.5** marca un hito importante en la evolución de **Exam‑Web**.  
Se trata de la primera versión **estable y distribuible** de la aplicación de escritorio, con el servidor web de exámenes **embebido directamente en la aplicación**.

Exam‑Web ofrece ahora una experiencia unificada:
- Control nativo desde Windows
- Interfaz web local de exámenes
- Arranque y parada limpios del servidor
- Comportamiento consistente tanto en modo desarrollo como en ejecutable

---

## ✅ Funcionalidades principales

### 🖥️ Aplicación de Escritorio

- Interfaz gráfica para iniciar y detener el servidor
- Minimización a la bandeja del sistema
- Restaurar y cerrar desde el icono de bandeja
- Configuración persistente
- Consola de logs integrada en tiempo real

### 🌐 Servidor Web Embebido

- Servidor Flask local integrado en la aplicación
- Sin procesos externos
- Parada y reinicio controlados
- Carga fiable de recursos estáticos en el ejecutable

### 📊 Sistema de Exámenes

- Preguntas tipo test (A / B / C / D)
- Aleatorización de respuestas
- Temporizadores por pregunta y por sesión
- Alertas visuales progresivas según el tiempo
- Estadísticas de sesión y acumuladas
- Marcado de preguntas para revisión
- Campo de estudio y explicación de respuestas
- Calculadora integrada
- Visor de base de datos desde la web

### 🧱 Fuentes de Datos

- Microsoft Excel (`.xls`, `.xlsx`, `.xlsm`)
- Microsoft Access (`.mdb`, `.accdb`)
- SQLite (`.db`)

Todas las fuentes comparten un **modelo de datos unificado y documentado**.

---

## 🔧 Mejoras técnicas

- Rediseño completo del ciclo de vida del servidor
- Ejecución del servidor dentro de la aplicación (sin `subprocess`)
- Uso de un servidor WSGI controlado
- Sistema de logging robusto para GUI y servidor
- Resolución correcta de recursos estáticos en ejecutables
- Cierre limpio sin errores de Tkinter ni hilos colgados
- Comportamiento idéntico en:
  - `python main.py`
  - Ejecutable generado con PyInstaller

---

## 🐞 Correcciones

- Eliminados problemas de apertura múltiple de instancias
- Corregido el problema de parada del servidor
- Solucionada la carga de imágenes en el ejecutable
- Corregidos errores de codificación en los logs
- Eliminadas excepciones al cerrar la aplicación
- Corregida la detección del estado real del servidor

---

## 📚 Documentación

- Documentación completa del modelo de datos (`BD`)
- Documentación separada en español e inglés
- DDL específicos para:
  - SQLite
  - Microsoft Access
  - Microsoft Excel
- Documentación preparada para GitHub

---

## ⚠️ Notas importantes

- La aplicación está diseñada para **Windows**
- La carpeta `static/` debe estar junto al ejecutable
- Los ficheros de configuración y log son locales

---

## 🚀 Próximos pasos

En versiones futuras se contempla:
- Mejoras de interfaz
- Nuevos modos de examen
- Estadísticas avanzadas
- Preparación de la versión `v1.0`

---

## ❤️ Apoyo al proyecto

Exam‑Web es software libre.

Si te resulta útil, puedes apoyar su desarrollo:

👉 https://paypal.me/atmarquez

---

© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)  
Licencia GPL‑3.0‑or‑later
