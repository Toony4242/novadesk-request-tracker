# NovaDesk Request Tracker

Interne demoapplicatie voor het opvolgen van klantaanvragen bij NovaDesk.

Deze starterapp hoort bij de projectopdracht IT Landscape. De applicatie is bewust niet perfect. Je opdracht is om de applicatie professioneel te verkennen, problemen te onderzoeken, issues te maken, Docker/CI/CD op te zetten en documentatie te schrijven.

## Technologie

- Python
- Flask
- SQLite
- Flask-Login
- pytest

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 seed.py
flask run
```

Op Windows kan het activeren van de virtual environment anders verlopen.

## Testaccounts

De seed data bevat enkele gebruikers. Het standaardwachtwoord is ??? (Vraag maar aan Wim)

Voorbeelden:

- alice.admin@novadesk.local
- amir.agent@novadesk.local
- sara.support@novadesk.local
- victor.viewer@novadesk.local

## Tests

```bash
pytest
```

## Opmerking

Deze documentatie is nog niet volledig. Vul ze aan tijdens de projectopdracht.
