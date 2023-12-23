from dataclasses import dataclass
from typing import Callable


@dataclass
class Weights:

    complexity: int = 0
    beauty: int = 0  # end-user beauty
    development_speed: int = 0


@dataclass
class Answer:

    text: str
    weights: Weights


@dataclass
class Question:

    text: str
    answers: list[Answer]


@dataclass
class Form:

    title: str
    questions: list[Question]
    calculate_result: Callable
