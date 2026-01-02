from dataclasses import dataclass

@dataclass
class Package:
    destination: tuple  # (x, y)
    weight: float
    priority: int

@dataclass
class Vehicle:
    capacity: float
    packages: list