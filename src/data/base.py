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
Data model and repository contracts for the exam system.

This module defines the core data structures (entities) and abstract
interfaces used by the application to interact with question data,
independently of the underlying storage technology (Excel, Access,
SQLite, etc.).

This file MUST NOT contain:
- Business logic
- File access
- Web or UI related code
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


# ============================================================
# Repository exceptions
# ============================================================

class DataRepositoryError(Exception):
    """
    Base exception for repository-related errors.
    """


class DataRepositoryLockedError(DataRepositoryError):
    """
    Raised when the data source is locked or cannot be accessed.

    Example: Excel file is open in another application.
    """


class DataRepositoryNotAvailableError(DataRepositoryError):
    """
    Raised when the data source is missing or invalid.
    """


# ============================================================
# Domain models
# ==========================================================

@dataclass
class AnswerOption:
    """
    Represents a single answer option for a question.

    Attributes:
        key:
            Identifier of the option (e.g. "A", "B", "C", "D").
        text:
            Text shown to the user for this option.
        explanation:
            Optional feedback text explaining why the option is
            correct or incorrect.
    """
    key: str
    text: str
    explanation: Optional[str] = None


@dataclass
class Question:
    """
    Represents a single exam question.

    Attributes:
        id:
            Logical identifier of the question (column 'NOMBRE' in Excel).
        statement:
            Question statement shown to the user.
        options:
            List of available answer options.
        correct_option:
            Key of the correct option (e.g. "A", "B", "C" or "D").
        topic:
            Optional topic or unit to which the question belongs.
        question_type:
            Optional question type (e.g. VAR, TEST, etc.).
        study_notes:
            Optional personal notes for study purposes.
        flagged:
            Indicates whether the question is marked for review (REV).
    """
    id: str
    statement: str
    options: List[AnswerOption]
    correct_option: str
    topic: Optional[str] = None
    question_type: Optional[str] = None
    study_notes: Optional[str] = None
    flagged: bool = False


@dataclass
class AnswerResult:
    """
    Represents the final answer selected by the user for a question.

    This object represents ONLY the final decision that must be persisted.
    Intermediate selections are never stored in the database.

    Attributes:
        question_id:
            Identifier of the answered question.
        selected_option:
            Option chosen by the user as the final answer.
        correct:
            Indicates whether the selected option is correct.
    """
    question_id: str
    selected_option: str
    correct: bool


# ============================================================
# Repository contract
# ============================================================

class QuestionRepository(ABC):
    """
    Abstract base class defining the contract for question repositories.

    Concrete implementations of this class provide access to question
    data stored in a specific data source (Excel, Access, SQLite, etc.).

    The rest of the application works exclusively with this interface
    and must remain independent from the actual storage mechanism.
    """

    @abstractmethod
    def open(self) -> None:
        """
        Opens the underlying data source.

        This method is invoked automatically when used as a context
        manager and must prepare the repository for reading/writing.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """
        Closes the underlying data source.

        This method must release any acquired resources and persist
        pending changes if necessary.
        """
        raise NotImplementedError

    def __enter__(self):
        """
        Enters the context manager and opens the data source.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager and closes the data source.
        """
        self.close()

    @abstractmethod
    def get_random_question(self) -> Question:
        """
        Returns a random question from the data source.

        Returns:
            A randomly selected Question instance.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_questions(self):
        """
        Returns an iterable over all available questions.

        Returns:
            An iterable of Question instances.
        """
        raise NotImplementedError

    @abstractmethod
    def mark_as_seen(self, question_id: str) -> None:
        """
        Marks a question as seen.

        This operation typically sets the VIS flag in the data source.

        Args:
            question_id:
                Identifier of the question to mark as seen.
        """
        raise NotImplementedError

    @abstractmethod
    def save_answer(self, result: AnswerResult) -> None:
        """
        Persists the final answer for a question.

        Implementations must update:
        - COR (last result)
        - OK or KO counters

        Args:
            result:
                Final answer result selected by the user.
        """
        raise NotImplementedError

    @abstractmethod
    def reset_statistics(self) -> None:
        """
        Resets all statistics for all questions.

        This operation must reset:
        - VIS
        - COR
        - REV
        - OK
        - KO
        """
        raise NotImplementedError
        

    @abstractmethod
    def calculate_global_stats(self):
        pass

    @abstractmethod
    def get_question_detail(self, question_id: str):
        pass
        
    @abstractmethod
    def get_question_raw(self, question_id: str) -> dict:
        pass

    @abstractmethod
    def update_question_raw(self, question_id: str, data: dict) -> None:
        pass
