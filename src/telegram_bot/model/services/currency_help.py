from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Course:
    exchange_rate: float
    nominal: int
    name: str
