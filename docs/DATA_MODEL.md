# Data Model – Table / Sheet `BD`

This document describes the **official data model** for the table or sheet named **`BD`** used by **Exam‑Web**.

The same structure applies consistently across:

* Microsoft **Excel** (`.xlsx`, `.xlsm`)
* Microsoft **Access** (`.mdb`, `.accdb`)
* **SQLite** (`.db`)

The definition below is based on the canonical SQL schema used by the project.

\---

## 📌 General rules

* Each **row represents a single question**
* Column names **must not be changed**
* Column order **must be preserved**
* Values are case‑sensitive where indicated
* The table contains **both persistent data and per‑session state flags**

\---

## 🗂 Table definition (reference)

The authoritative schema is:

```sql
CREATE TABLE "BD" (
	"UN"      INTEGER,
	"NOMBRE"  TEXT,
	"TIPO"    TEXT,
	"PREGUNTA" TEXT,
	"A"       TEXT,
	"B"       TEXT,
	"C"       TEXT,
	"D"       TEXT,
	"RA"      TEXT,
	"RB"      TEXT,
	"RC"      TEXT,
	"RD"      TEXT,
	"R"       TEXT,
	"VIS"     INTEGER,
	"COR"     INTEGER,
	"REV"     INTEGER,
	"ESTUDIO" TEXT,
	"Filtro"  INTEGER,
	"OK"      INTEGER,
	"KO"      INTEGER
);
```

\---

## 📖 Field‑by‑field description

### 🔑 `UN`

**Unique numeric identifier of the question.**

* Integer value
* Must be unique
* Must never change once assigned

\---

### 🏷 `NOMBRE`

**Logical name or category of the question.**

* Free text
* Can be used to group questions by topic or source

\---

### 🧩 `TIPO`

**Question type.**

Typical values depend on the exam definition (e.g. theory, practice, regulation).

\---

### 📝 `PREGUNTA`

**Full statement of the question.**

* Long text
* May include line breaks
* Rendered as plain text in the web interface

\---

### 🅰 `A`, 🅱 `B`, 🅲 `C`, 🅳 `D`

**Answer options.**

* Each field contains the text for one answer option
* Must not be empty
* Displayed dynamically in the web UI

\---

### 📘 `RA`, `RB`, `RC`, `RD`

**Explanation or rationale for each answer option.**

* Optional explanatory text
* Shown after answering a question
* Can be empty if no explanation is required

\---

### ✅ `R`

**Correct answer indicator.**

Valid values:

```
A
B
C
D
```

Rules:

* Exactly one character
* Uppercase
* Must correspond to one of the answer options

\---

### 👁 `VIS`

**Visited flag.**

* `0` → question not yet shown
* `1` → question has been shown at least once

This value is **updated automatically** by the system.

\---

### ✔ `COR`

**Last answer correctness flag.**

* `0` → last attempt was incorrect
* `1` → last attempt was correct

\---

### 🔁 `REV`

**Review flag.**

* `0` → normal question
* `1` → marked for review by the user

Used to prioritise questions during selection.

\---

### 📚 `ESTUDIO`

**Study notes associated with the question.**

* Long text
* Shown after answering
* Intended for explanations, summaries or reminders

\---

### 🧮 `Filtro`

**Filtering flag.**

* Integer value
* Used internally for selective question pools
* Exact semantics depend on exam configuration

\---

### ✅ `OK`

**Total number of correct answers (historical).**

* Integer ≥ 0
* Incremented each time the question is answered correctly

\---

### ❌ `KO`

**Total number of incorrect answers (historical).**

* Integer ≥ 0
* Incremented each time the question is answered incorrectly

\---

## 📐 Example record

|UN|NOMBRE|TIPO|PREGUNTA|A|B|C|D|R|VIS|COR|REV|OK|KO|
|-:|-|-|-|-|-|-|-|-|-:|-:|-:|-:|-:|
|12|Redes|Test|¿Qué protocolo usa HTTP?|TCP|UDP|FTP|SMTP|A|1|1|0|5|1|

\---

## ✅ Notes

* Do not rename columns
* Do not remove columns
* Always keep numeric flags as integers (`0` or `1`)
* Ensure the `BD` structure is identical across platforms

\---

© 2024–2026 Antonio Teodomiro Márquez Muñoz (Naidel)
Licensed under GPL‑3.0‑or‑later

