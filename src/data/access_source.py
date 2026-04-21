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
Access-based implementation of the QuestionRepository interface.

This module provides a safe and robust adapter for using an Access
file as the persistent storage of exam questions and statistics.
"""

import pyodbc
import random
import time
from pathlib import Path
from typing import Iterable

from data.base import (
    Question,
    AnswerOption,
    AnswerResult,
    QuestionRepository,
)


class AccessQuestionRepository(QuestionRepository):
    """
    Repository that stores and retrieves exam questions from
    a Microsoft Access (.mdb / .accdb) database.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self._conn = None
        self._cursor = None

    # ---------------------------------------------------------
    # Context manager support (with ... as repo)
    # ---------------------------------------------------------

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ---------------------------------------------------------
    # Connection handling
    # ---------------------------------------------------------

    def open(self):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + str(self.file_path) + ';'
        )
        self._conn = pyodbc.connect(conn_str)
        self._cursor = self._conn.cursor()

    def close(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def get_all_questions(self) -> Iterable[Question]:
        sql = "SELECT * FROM BD"
        rows = self._cursor.execute(sql).fetchall()

        for row in rows:
            yield self._row_to_question(row)

    def get_question_by_id(self, question_id: str) -> Question | None:
        sql = "SELECT * FROM BD WHERE NOMBRE = ?"
        row = self._cursor.execute(sql, question_id).fetchone()
        if not row:
            return None
        return self._row_to_question(row)

    def get_random_question(
        self,
        filtro_revisados: str = "Todos",
        filtro_fallados: str = "Todos",
    ):
        """
        Réplica exacta de la lógica de Excel, manteniendo el comportamiento intacto.
        La única diferencia es que la selección aleatoria se hace sobre una lista
        de filas cargadas desde Access.
        """

        # Cargar todas las filas (equivalente a iter_rows)
        rows = self._cursor.execute("SELECT * FROM BD").fetchall()

        if not rows:
            raise RuntimeError("No valid question found")

        total_questions = len(rows)
        max_attempts = total_questions * 2

        # ✅ Reseed como hace Excel internamente
        random.seed(time.time_ns())

        last_candidate = None

        for _ in range(max_attempts):

            # Selección aleatoria de fila (equivalente a randint en Excel)
            row = random.choice(rows)

            vis = row.VIS or 0
            cor = row.COR or 0
            rev = row.REV or 0

            # PRIORIDAD ABSOLUTA: revisadas (solo si salen en este intento)
            if rev == 1:
                return self._row_to_question(row)

            allow_no_revisados = True
            allow_fallados = True

            # Filtro: solo no revisados
            if filtro_revisados not in ("Todos", "", None):
                if rev == 1:
                    allow_no_revisados = False

            # Filtro: solo fallados
            if filtro_fallados not in ("Todos", "", None):
                if cor == 1:
                    allow_fallados = False
                else:
                    # Prioridad implícita a falladas
                    allow_no_revisados = True

            if allow_no_revisados and allow_fallados:
                last_candidate = row
                break

        # Si no se encontró perfecta, devolver última candidata válida
        if last_candidate is not None:
            return self._row_to_question(last_candidate)

        # Caso extremo: devolver cualquiera
        return self._row_to_question(random.choice(rows))

    # ---------------------------------------------------------
    # Updates
    # ---------------------------------------------------------

    def mark_as_seen(self, question_id: str):
        sql = "UPDATE BD SET VIS = 1 WHERE NOMBRE = ?"
        self._cursor.execute(sql, question_id)
        self._conn.commit()

    def save_answer(self, result: AnswerResult):
        if result.correct:
            sql = """
                UPDATE BD
                SET
                    OK = OK + 1,
                    COR = 1
                WHERE NOMBRE = ?
            """
        else:
            sql = """
                UPDATE BD
                SET
                    KO = KO + 1,
                    COR = 0
                WHERE NOMBRE = ?
            """

        self._cursor.execute(sql, result.question_id)
        self._conn.commit()

    def set_review_flag(self, question_id: str, flagged: bool):
        sql = "UPDATE BD SET REV = ? WHERE NOMBRE = ?"
        self._cursor.execute(sql, int(flagged), question_id)
        self._conn.commit()

    def reset_statistics(self):
        sql = """
            UPDATE BD
            SET
                VIS = 0,
                COR = 0,
                REV = 0,
                OK  = 0,
                KO  = 0
        """
        self._cursor.execute(sql)
        self._conn.commit()

    # ---------------------------------------------------------
    # Row conversion
    # ---------------------------------------------------------

    def _row_to_question(self, row) -> Question:
        options = [
            AnswerOption("A", row.A, row.RA),
            AnswerOption("B", row.B, row.RB),
            AnswerOption("C", row.C, row.RC),
            AnswerOption("D", row.D, row.RD),
        ]

        return Question(
            id=str(row.NOMBRE),
            statement=str(row.PREGUNTA),
            options=options,
            correct_option=str(row.R),
            topic=str(row.UN),
            question_type=str(row.TIPO),
            study_notes=row.ESTUDIO,
            flagged=bool(row.REV),
        )
        
    def calculate_global_stats(self):
        sql = """
            SELECT
                COUNT(*) AS total_questions,
                SUM(VIS) AS seen_questions,
                SUM(OK) AS total_ok,
                SUM(KO) AS total_ko
            FROM BD
        """
        row = self._cursor.execute(sql).fetchone()

        total_questions = row.total_questions or 0
        seen_questions = row.seen_questions or 0
        total_correct = row.total_ok or 0
        total_incorrect = row.total_ko or 0

        total_attempts = total_correct + total_incorrect

        return {
            "correct": total_correct,
            "incorrect": total_incorrect,
            "percentage": round(
                (total_correct / total_attempts) * 100, 2
            ) if total_attempts > 0 else 0,
            "total_questions": total_questions,
            "seen_questions": seen_questions,
            "seen_percentage": round(
                (seen_questions / total_questions) * 100, 2
            ) if total_questions > 0 else 0,
        }

    def get_question_detail(self, question_id: str):
        sql = "SELECT * FROM BD WHERE NOMBRE = ?"
        row = self._cursor.execute(sql, question_id).fetchone()

        if not row:
            return None

        return {
            "question": self._row_to_question(row),
            "vis": int(row.VIS or 0),
            "cor": int(row.COR or 0),
            "rev": bool(row.REV),
            "ok": int(row.OK or 0),
            "ko": int(row.KO or 0),
    }

    def get_question_raw(self, question_id: str) -> dict:
        sql = "SELECT * FROM BD WHERE NOMBRE = ?"
        row = self._cursor.execute(sql, question_id).fetchone()

        if not row:
            raise ValueError("Pregunta no encontrada")

        data = {}
        for column in row.cursor_description:
            name = column[0].upper()
            value = getattr(row, column[0])
            data[name] = "" if value is None else value

        return data

    def update_question_raw(self, question_id: str, data: dict) -> None:
        fields = []
        values = []

        for field, value in data.items():
            if field == "NOMBRE":
                continue
            fields.append(f"{field} = ?")
            values.append(value)

        sql = f"""
            UPDATE BD
            SET {", ".join(fields)}
            WHERE NOMBRE = ?
        """

        values.append(question_id)
        self._cursor.execute(sql, values)
        self._conn.commit()