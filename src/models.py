import json


class Task:
    def __init__(
        self, id: int, titol: str, assignatura: str, estat: str = "pendent"
    ) -> None:
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, dades: dict) -> "Task":
        return cls(
            id=dades["id"],
            titol=dades["titol"],
            assignatura=dades["assignatura"],
            estat=dades.get("estat", "pendent"),
        )

    @classmethod
    def from_json(cls, cadena: str) -> "Task":
        return cls.from_dict(json.loads(cadena))
