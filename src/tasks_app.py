import argparse
import json
import re
from datetime import date
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task

FITXER_TASQUES = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def validar_data_limit(cadena):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cadena):
        raise argparse.ArgumentTypeError(
            "La data límit ha de tenir el format YYYY-MM-DD"
        )
    try:
        date.fromisoformat(cadena)
    except ValueError as error:
        raise argparse.ArgumentTypeError("La data límit no és vàlida") from error
    return cadena


def carregar_tasques():
    if not FITXER_TASQUES.exists():
        FITXER_TASQUES.parent.mkdir(parents=True, exist_ok=True)
        FITXER_TASQUES.write_text("[]", encoding="utf-8")
    dades = json.loads(FITXER_TASQUES.read_text(encoding="utf-8"))
    return [Task.from_dict(registre) for registre in dades]


def desar_tasques(tasques):
    dades = [tasca.to_dict() for tasca in tasques]
    FITXER_TASQUES.write_text(
        json.dumps(dades, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def afegir_tasca(titol, assignatura, data_limit=None):
    tasques = carregar_tasques()
    identificador = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(identificador, titol, assignatura, data_limit=data_limit)
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] creada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(f"[{tasca.id}] {tasca.titol} ({tasca.assignatura}) - estat: {tasca.estat}")


def main():
    analitzador = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    comandaments = analitzador.add_subparsers(dest="comandament", required=True)

    afegir = comandaments.add_parser("add", help="Afegir una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")
    afegir.add_argument(
        "--due", type=validar_data_limit, help="Data límit (YYYY-MM-DD)"
    )

    comandaments.add_parser("list", help="Llistar totes les tasques")

    arguments = analitzador.parse_args()
    if arguments.comandament == "add":
        afegir_tasca(arguments.title, arguments.subject, arguments.due)
    elif arguments.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
