from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class Name:
    domain: str
    name: str
    title: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    candidate: Optional[bool] = None
    invalid: Optional[bool] = None
    key: ClassVar[str] = "domain"
