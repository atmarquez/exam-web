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
SQLite-based implementation of the QuestionRepository interface.

This module provides a safe and robust adapter for using an SQLite (.db)
file as the persistent storage of exam questions and statistics.
"""
import sqlite3
import random
import time
from pathlib import Path

from data.base import (
    QuestionRepository,
    Question,
    AnswerOption,
    AnswerResult,
)

class SQLiteQuestionRepository(QuestionRepository):

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.conn = None
        self.cursor = None

    # ------------------------------
    # Context manager
    # ------------------------------

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ------------------------------
    # Connection handling
    # ------------------------------

    def open(self):
        self.conn = sqlite3.connect(self.file_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    # ------------------------------
    # Selección de preguntas
    # (lógica EXACTA de Excel)
    # ------------------------------

    def get_random_question(
        self,
        filtro_revisados="Todos",
        filtro_fallados="Todos",
    ):
        rows = self.cursor.execute("SELECT * FROM BD").fetchall()

        if not rows:
            raise RuntimeError("No valid question found")

        random.seed(time.time_ns())
        total = len(rows)
        max_attempts = total * 2

        last_candidate = None

        for _ in range(max_attempts):
            row = random.choice(rows)

            vis = row["VIS"] or 0
            cor = row["COR"] or 0
            rev = row["REV"] or 0

            # PRIORIDAD ABSOLUTA SOLO SI SALE EN EL AZAR
            if rev == 1:
                return self._row_to_question(row)

            allow_no_revisados = True
            allow_fallados = True

            if filtro_revisados not in ("Todos", "", None):
                if rev == 1:
                    allow_no_revisados = False

            if filtro_fallados not in ("Todos", "", None):
                if cor == 1:
                    allow_fallados = False
                else:
                    allow_no_revisados = True

            if allow_no_revisados and allow_fallados:
                last_candidate = row
                break

        if last_candidate is not None:
            return self._row_to_question(last_candidate)

        return self._row_to_question(random.choice(rows))

    # ------------------------------
    # Estadísticas globales
    # ------------------------------

    def calculate_global_stats(self):
        row = self.cursor.execute("""
            SELECT
                COUNT(*)            AS total_questions,
                SUM(VIS)            AS seen_questions,
                SUM(OK)             AS total_ok,
                SUM(KO)             AS total_ko
            FROM BD
        """).fetchone()

        total_attempts = (row["total_ok"] or 0) + (row["total_ko"] or 0)

        return {
            "correct": row["total_ok"] or 0,
            "incorrect": row["total_ko"] or 0,
            "percentage": round(
                ((row["total_ok"] or 0) / total_attempts) * 100, 2
            ) if total_attempts > 0 else 0,
            "total_questions": row["total_questions"] or 0,
            "seen_questions": row["seen_questions"] or 0,
            "seen_percentage": round(
                ((row["seen_questions"] or 0) / row["total_questions"]) * 100, 2
            ) if row["total_questions"] else 0,
        }

    # ------------------------------
    # Escrituras
    # ------------------------------

    def mark_as_seen(self, question_id: str):
        self.cursor.execute(
            "UPDATE BD SET VIS = 1 WHERE NOMBRE = ?",
            (question_id,),
        )

    def save_answer(self, result: AnswerResult):
        if result.correct:
            self.cursor.execute("""
                UPDATE BD
                SET OK = OK + 1,
                    COR = 1
                WHERE NOMBRE = ?
            """, (result.question_id,))
        else:
            self.cursor.execute("""
                UPDATE BD
                SET KO = KO + 1,
                    COR = 0
                WHERE NOMBRE = ?
            """, (result.question_id,))

    def set_review_flag(self, question_id: str, flagged: bool):
        self.cursor.execute(
            "UPDATE BD SET REV = ? WHERE NOMBRE = ?",
            (1 if flagged else 0, question_id),
        )

    def reset_statistics(self):
        self.cursor.execute("""
            UPDATE BD
            SET VIS = 0,
                COR = 0,
                REV = 0,
                OK  = 0,
                KO  = 0
        """)

    # ------------------------------
    # Detalle y edición
    # ------------------------------

    def get_question_detail(self, question_id: str):
        row = self.cursor.execute(
            "SELECT * FROM BD WHERE NOMBRE = ?",
            (question_id,),
        ).fetchone()

        if not row:
            return None

        return {
            "question": self._row_to_question(row),
            "vis": row["VIS"] or 0,
            "cor": row["COR"] or 0,
            "rev": bool(row["REV"]),
            "ok": row["OK"] or 0,
            "ko": row["KO"] or 0,
        }

    def get_question_raw(self, question_id: str) -> dict:
        row = self.cursor.execute(
            "SELECT * FROM BD WHERE NOMBRE = ?",
            (question_id,),
        ).fetchone()

        if not row:
            raise ValueError("Pregunta no encontrada")

        return {k.upper(): row[k] for k in row.keys()}

    def update_question_raw(self, question_id: str, data: dict) -> None:
        fields = []
        values = []

        for field, value in data.items():
            if field == "NOMBRE":
                continue
            fields.append(f"{field} = ?")
            values.append(value)

        values.append(question_id)

        self.cursor.execute(
            f"UPDATE BD SET {', '.join(fields)} WHERE NOMBRE = ?",
            values
        )

    # ------------------------------
    # Conversión
    # ------------------------------

    def _row_to_question(self, row):
        options = [
            AnswerOption("A", row["A"], row["RA"]),
            AnswerOption("B", row["B"], row["RB"]),
            AnswerOption("C", row["C"], row["RC"]),
            AnswerOption("D", row["D"], row["RD"]),
        ]

        return Question(
            id=row["NOMBRE"],
            statement=row["PREGUNTA"],
            options=options,
            correct_option=row["R"],
            topic=row["UN"],
            question_type=row["TIPO"],
            study_notes=row["ESTUDIO"],
            flagged=bool(row["REV"]),
        )
        
    def get_all_questions(self):
        rows = self.cursor.execute("SELECT * FROM BD").fetchall()
        for row in rows:
            yield self._row_to_question(row)