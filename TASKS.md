\# TASKS.md - Tasks\_app



\## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.



\### Tasques d'Execució:

\- \[x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02) 

\- \[x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.

\- \[x] Tasca 1.3: Desenvolupar Tasks\_app a `src/tasks\_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)

\- \[x] Tasca 1.4: Crear test d'integració a `test/test\_tasks\_app.py` segons els escenaris GS-01, GS-02 i GS-03.

\- \[x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).


## Increment 2: Dates Límit, Edició, Compleció i Alertes
Objectiu: Afegir data límit (`--due`), modificació per `--id`, marcatge de tasca completada i alertes `[CADUCADA]` / `[URGENT]` al llistat.

### Tasques d'Execució:
- [x] Tasca 2.1: Actualitzar el model `Task` a `src/models.py` per suportar el camp opcional de data límit (`data_limit`) i la serialització/desserialització JSON mantenint compatibilitat amb tasques anteriors. (Requisit RF-05)[cite: 3, 6]
- [x] Tasca 2.2: Actualitzar `add` a `src/tasks_app.py` perquè accepti `--due YYYY-MM-DD` i validar el format de data. (Requisit RF-05, Escenari GS-04)[cite: 3, 6]
- [x] Tasca 2.3: Implementar a `src/tasks_app.py` la modificació d'atributs d'una tasca identificada per `--id <ID>`. (Requisit RF-06, Escenari GS-05)[cite: 3, 6]
- [x] Tasca 2.4: Implementar a `src/tasks_app.py` la funcionalitat per marcar una tasca com a completada (`--id <ID>`). (Requisit RF-07, Escenari GS-06)[cite: 3, 6]
- [x] Tasca 2.5: Actualitzar `list` a `src/tasks_app.py` perquè en tasques pendents mostri `[CADUCADA]` si la data límit és anterior a la data actual o `[URGENT]` si falta menys de 7 dies. (Requisits RF-08 i RF-09, Escenaris GS-07 i GS-08)[cite: 3, 6]
- [ ] Tasca 2.6: Ampliar els tests a `test/test_tasks_app.py` amb els escenaris GS-04 a GS-08 i verificar que tots passen amb `python3 -m pytest test`.[cite: 4, 6]
