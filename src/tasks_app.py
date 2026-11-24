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


def modificar_tasca(
    identificador, titol=None, assignatura=None, data_limit=None, estat=None
):
    tasques = carregar_tasques()
    tasca = next((item for item in tasques if item.id == identificador), None)
    if tasca is None:
        print(f"No s'ha trobat cap tasca amb ID {identificador}.")
        raise SystemExit(1)
    if titol is None and assignatura is None and data_limit is None and estat is None:
        print("Cal indicar almenys un atribut per modificar.")
        raise SystemExit(1)
    if titol is not None:
        tasca.titol = titol
    if assignatura is not None:
        tasca.assignatura = assignatura
    if data_limit is not None:
        tasca.data_limit = data_limit
    if estat is not None:
        tasca.estat = estat
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] modificada amb èxit")


def completar_tasca(identificador):
    tasques = carregar_tasques()
    tasca = next((item for item in tasques if item.id == identificador), None)
    if tasca is None:
        print(f"No s'ha trobat cap tasca amb ID {identificador}.")
        raise SystemExit(1)
    tasca.estat = "completada"
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] marcada com a completada")


def obtenir_alerta(tasca, avui):
    if tasca.estat != "pendent" or not tasca.data_limit:
        return ""
    data_limit = date.fromisoformat(tasca.data_limit)
    if data_limit < avui:
        return "[CADUCADA]"
    if (data_limit - avui).days < 7:
        return "[URGENT]"
    return ""


def llistar_tasques(avui=None):
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    if avui is None:
        avui = date.today()
    for tasca in tasques:
        linia = (
            f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
            f" - estat: {tasca.estat}"
        )
        alerta = obtenir_alerta(tasca, avui)
        if alerta:
            linia += f" {alerta}"
        print(linia)


def main():
    analitzador = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    comandaments = analitzador.add_subparsers(dest="comandament", required=True)

    afegir = comandaments.add_parser("add", help="Afegir una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")
    afegir.add_argument(
        "--due", type=validar_data_limit, help="Data límit (YYYY-MM-DD)"
    )

    modificar = comandaments.add_parser(
        "edit", aliases=["update", "modify"], help="Modificar una tasca existent"
    )
    modificar.add_argument(
        "--id", type=int, required=True, help="Identificador de la tasca"
    )
    modificar.add_argument("--title", help="Nou títol de la tasca")
    modificar.add_argument("--subject", help="Nova assignatura de la tasca")
    modificar.add_argument(
        "--due", type=validar_data_limit, help="Nova data límit (YYYY-MM-DD)"
    )
    modificar.add_argument(
        "--estat",
        "--status",
        dest="estat",
        choices=["pendent", "completada"],
        help="Nou estat de la tasca",
    )

    completar = comandaments.add_parser(
        "done",
        aliases=["complete", "completar"],
        help="Marcar una tasca com a completada",
    )
    completar.add_argument(
        "--id", type=int, required=True, help="Identificador de la tasca"
    )

    comandaments.add_parser("list", help="Llistar totes les tasques")

    arguments = analitzador.parse_args()
    if arguments.comandament == "add":
        afegir_tasca(arguments.title, arguments.subject, arguments.due)
    elif arguments.comandament in ("edit", "update", "modify"):
        modificar_tasca(
            arguments.id,
            arguments.title,
            arguments.subject,
            arguments.due,
            arguments.estat,
        )
    elif arguments.comandament in ("done", "complete", "completar"):
        completar_tasca(arguments.id)
    elif arguments.comandament == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
