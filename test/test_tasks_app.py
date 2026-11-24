import json
import subprocess
import sys
from pathlib import Path

import pytest

ARREL = Path(__file__).resolve().parent.parent
FITXER_TASQUES = ARREL / "data" / "tasks.json"


@pytest.fixture(autouse=True)
def aillar_fitxer_tasques():
    original = (
        FITXER_TASQUES.read_text(encoding="utf-8")
        if FITXER_TASQUES.exists()
        else None
    )
    FITXER_TASQUES.write_text("[]", encoding="utf-8")
    yield
    if original is None:
        FITXER_TASQUES.unlink()
    else:
        FITXER_TASQUES.write_text(original, encoding="utf-8")


def executar(*arguments):
    resultat = subprocess.run(
        [sys.executable, str(ARREL / "src" / "tasks_app.py"), *arguments],
        cwd=ARREL,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultat.stdout


def test_creacio_correcta_duna_tasca():
    sortida = executar("add", "--title", "Pràctica 1", "--subject", "RS")
    assert sortida == "Tasca [ID: 1] creada amb èxit\n"
    tasques = json.loads(FITXER_TASQUES.read_text(encoding="utf-8"))
    assert tasques == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_llistar_tasques_buit():
    assert executar("list") == "Registre de tasques buit.\n"


def test_llistar_tasques_registrades():
    FITXER_TASQUES.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "titol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    assert executar("list") == (
        "[1] Pràctica 1 (RS) - estat: pendent\n"
        "[2] Examen parcial (SO) - estat: pendent\n"
    )
