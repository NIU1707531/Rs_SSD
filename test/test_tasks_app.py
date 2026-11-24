import json
import subprocess
import sys
from datetime import date, timedelta
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


def desar_tasques(registres):
    FITXER_TASQUES.write_text(
        json.dumps(registres, ensure_ascii=False), encoding="utf-8"
    )


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


def test_creacio_amb_data_limit():
    sortida = executar(
        "add",
        "--title",
        "Lliurament 2",
        "--subject",
        "RS",
        "--due",
        "2026-12-15",
    )
    assert sortida == "Tasca [ID: 1] creada amb èxit\n"
    tasques = json.loads(FITXER_TASQUES.read_text(encoding="utf-8"))
    assert tasques == [
        {
            "id": 1,
            "titol": "Lliurament 2",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-15",
        }
    ]


def test_modificacio_dun_atribut_per_id():
    desar_tasques(
        [
            {
                "id": 1,
                "titol": "Practica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ]
    )
    sortida = executar("edit", "--id", "1", "--title", "Pràctica 1")
    assert sortida == "Tasca [ID: 1] modificada amb èxit\n"
    tasques = json.loads(FITXER_TASQUES.read_text(encoding="utf-8"))
    assert tasques == [
        {"id": 1, "titol": "Pràctica 1", "assignatura": "RS", "estat": "pendent"}
    ]


def test_marcar_tasca_completada():
    desar_tasques(
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ]
    )
    sortida = executar("done", "--id", "1")
    assert sortida == "Tasca [ID: 1] marcada com a completada\n"
    tasques = json.loads(FITXER_TASQUES.read_text(encoding="utf-8"))
    assert tasques == [
        {"id": 1, "titol": "Pràctica 1", "assignatura": "RS", "estat": "completada"}
    ]


def test_llistat_tasca_caducada():
    data_caducada = str(date.today() - timedelta(days=14))
    desar_tasques(
        [
            {
                "id": 1,
                "titol": "Lliurament caducat",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": data_caducada,
            }
        ]
    )
    assert executar("list") == (
        "[1] Lliurament caducat (RS) - estat: pendent [CADUCADA]\n"
    )


def test_llistat_tasca_urgent():
    data_urgent = str(date.today() + timedelta(days=4))
    desar_tasques(
        [
            {
                "id": 1,
                "titol": "Lliurament urgent",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": data_urgent,
            }
        ]
    )
    assert executar("list") == (
        "[1] Lliurament urgent (RS) - estat: pendent [URGENT]\n"
    )


def test_sense_alerta_en_completades_i_dates_llunyanes():
    data_llunyana = str(date.today() + timedelta(days=14))
    desar_tasques(
        [
            {
                "id": 1,
                "titol": "Caducada completada",
                "assignatura": "RS",
                "estat": "completada",
                "data_limit": str(date.today() - timedelta(days=14)),
            },
            {
                "id": 2,
                "titol": "Lliurament llunyà",
                "assignatura": "SO",
                "estat": "pendent",
                "data_limit": data_llunyana,
            },
        ]
    )
    sortida = executar("list")
    assert sortida == (
        "[1] Caducada completada (RS) - estat: completada\n"
        "[2] Lliurament llunyà (SO) - estat: pendent\n"
    )
