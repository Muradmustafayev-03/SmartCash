from dataclasses import dataclass


@dataclass
class ProductUnit:
    name: str
    link: str
    description: str = None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
