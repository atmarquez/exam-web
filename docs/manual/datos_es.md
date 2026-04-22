
# Modelo de datos (BD)

Este documento describe el **modelo de datos principal** utilizado por Exam-Web para almacenar las preguntas del examen.

La información se guarda en una **tabla u hoja llamada `BD`**, compatible con:
- Microsoft Excel
- Microsoft Access
- SQLite

---

## Finalidad de la tabla `BD`

La tabla `BD` contiene **todas las preguntas y sus estadísticas asociadas**.  
Cada fila representa **una pregunta única**.

Se almacenan:
- El contenido de la pregunta
- Las respuestas posibles
- La respuesta correcta
- Explicaciones y material de estudio
- Contadores históricos de aciertos y fallos
- Estados de control (vistos, revisión, filtros)

---

## Campos principales

### Identificación
- **UN**: identificador único de la pregunta
- **NOMBRE**: categoría o bloque temático
- **TIPO**: tipo de pregunta

### Contenido
- **PREGUNTA**: texto completo de la pregunta
- **A, B, C, D**: opciones de respuesta
- **RA, RB, RC, RD**: explicación asociada a cada opción
- **R**: respuesta correcta (A, B, C o D)

### Estado y control
- **VIS**: indica si la pregunta ha sido mostrada
- **COR**: indica si la última respuesta fue correcta
- **REV**: marca manual para revisión
- **Filtro**: campo interno de filtrado

### Estudio y estadísticas
- **ESTUDIO**: texto de apoyo o estudio
- **OK**: número total de aciertos
- **KO**: número total de fallos

---

## Reglas importantes

- No cambiar los nombres de los campos
- No alterar el orden de las columnas
- Los valores lógicos se almacenan como 0 o 1
- El campo **R** debe ser siempre A, B, C o D

---

Este modelo es el **contrato de datos oficial** del sistema Exam-Web.
