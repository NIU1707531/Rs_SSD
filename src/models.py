import json


class Task:
    def __init__(
        self,
        id: int,
        titol: str,
        assignatura: str,
        estat: str = "pendent",
        data_limit: str | None = None,
    ) -> None:
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat
        self.data_limit = data_limit

    def to_dict(self) -> dict:
        dades = {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }
        if self.data_limit is not None:
            dades["data_limit"] = self.data_limit
        return dades

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, dades: dict) -> "Task":
        return cls(
            id=dades["id"],
            titol=dades["titol"],
            assignatura=dades["assignatura"],
            estat=dades.get("estat", "pendent"),
            data_limit=dades.get("data_limit"),
        )

    @classmethod
    def from_json(cls, cadena: str) -> "Task":
        return cls.from_dict(json.loads(cadena))
