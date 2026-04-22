
# Data model (BD)

This document describes the **main data model** used by Exam-Web to store exam questions.

Data is stored in a **table or sheet named `BD`**, compatible with:
- Microsoft Excel
- Microsoft Access
- SQLite

---

## Purpose of table `BD`

The `BD` table contains **all questions and their associated statistics**.
Each row represents **one unique question**.

It stores:
- Question content
- Possible answers
- Correct answer
- Explanations and study material
- Historical correct/incorrect counters
- Control flags (seen, review, filter)

---

## Main fields

### Identification
- **UN**: unique numeric question identifier
- **NOMBRE**: category or topic
- **TIPO**: question type

### Content
- **PREGUNTA**: full question text
- **A, B, C, D**: answer options
- **RA, RB, RC, RD**: explanation for each option
- **R**: correct answer (A, B, C or D)

### State and control
- **VIS**: indicates if the question has been shown
- **COR**: indicates whether the last answer was correct
- **REV**: manual review flag
- **Filtro**: internal filtering field

### Study and statistics
- **ESTUDIO**: study or explanation text
- **OK**: total correct answers
- **KO**: total incorrect answers

---

## Important rules

- Do not rename fields
- Do not change column order
- Boolean values are stored as 0 or 1
- Field **R** must always be A, B, C or D

---

This model is the **official data contract** of the Exam-Web system.
