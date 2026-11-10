from app import create_app, db
from app.models import AuditLog, Comment, SupportRequest, User

PASSWORD = "Password123"


def make_user(name, email, role, active=True):
    user = User(name=name, email=email, role=role, active=active)
    user.set_password(PASSWORD)
    return user


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        alice = make_user("Alice Admin", "alice.admin@novadesk.local", "admin")
        amir = make_user("Amir Agent", "amir.agent@novadesk.local", "agent")
        sara = make_user("Sara Support", "sara.support@novadesk.local", "agent")
        victor = make_user("Victor Viewer", "victor.viewer@novadesk.local", "viewer")
        nina = make_user("Nina Inactive", "nina.inactive@novadesk.local", "viewer", active=False)
        users = [alice, amir, sara, victor, nina]
        db.session.add_all(users)
        db.session.flush()

        data = [
            ("Factuurgegevens aanpassen", "Klant vraagt aanpassing van factuuradres.", "Aster BV", "finance@aster.example", "billing", "medium", "new", amir),
            ("Technische fout bij uploaden bijlage", "Bijlage uploaden geeft foutmelding in klantportaal.", "Bluebird NV", "help@bluebird.example", "technical", "high", "in_progress", sara),
            ("Vraag over contractverlenging", "Klant vraagt informatie over verlenging.", "Canvas Group", "info@canvas.example", "sales", "low", "waiting", None),
            ("Loginprobleem bij klantportaal", "Gebruiker kan niet aanmelden.", "Delta Services", "it@delta.example", "technical", "urgent", "new", sara),
            ("Zoekresultaten tonen oude aanvragen", "Gebruiker vindt verouderde gegevens terug.", "Echo Labs", "support@echo.example", "technical", "medium", "in_progress", amir),
            ("Dringende vraag over serviceonderbreking", "Klant meldt mogelijk onderbroken dienst.", "Fluxx", "ops@fluxx.example", "technical", "urgent", "waiting", None),
            ("Klant ontvangt geen bevestigingsmail", "Bevestiging na aanvraag komt niet toe.", "Greenfield", "admin@greenfield.example", "general", "high", "new", sara),
            ("Onjuiste status zichtbaar in overzicht", "Aanvraag lijkt afgewerkt maar staat open.", "Horizon", "team@horizon.example", "general", "medium", "resolved", amir),
            ("Nieuwe klant wil onboardinginformatie", "Vraag naar documentatie en planning.", "Iris Consulting", "hello@iris.example", "sales", "medium", "new", None),
            ("Vraag over rapportering openstaande dossiers", "Teamlead vraagt duidelijkere rapportering.", "Jupiter Foods", "lead@jupiter.example", "general", "low", "closed", alice),
            ("Klant meldt trage response", "Applicatie reageert traag op vrijdagmiddag.", "Kite Logistics", "ops@kite.example", "technical", "high", "in_progress", sara),
            ("Aanvraag prioriteit urgent niet zichtbaar", "Urgente aanvraag werd te laat opgemerkt.", "Lima Health", "care@lima.example", "general", "urgent", "new", amir),
            ("Wijziging contactpersoon", "Klant wil nieuwe contactpersoon registreren.", "Metro Works", "info@metro.example", "sales", "low", "waiting", sara),
            ("Foutmelding zonder uitleg", "Gebruiker ziet technische foutpagina.", "Northwind", "support@northwind.example", "technical", "high", "new", None),
            ("Vraag over bestaande offerte", "Sales moet dossier terugvinden.", "Orion Partners", "sales@orion.example", "sales", "medium", "closed", amir),
            ("Factuur niet gevonden", "Klant vindt factuur niet in portaal.", "Polar Retail", "billing@polar.example", "billing", "medium", "in_progress", sara),
            ("Contractdata controleren", "Teamlead vraagt controle van datums.", "Quartz", "admin@quartz.example", "general", "low", "resolved", alice),
            ("API foutmelding klantportaal", "Klant ziet fout bij synchronisatie.", "River Tech", "dev@river.example", "technical", "urgent", "waiting", sara),
            ("Aanvraag dubbel geregistreerd", "Zelfde klantaanvraag lijkt twee keer te bestaan.", "Solaris", "service@solaris.example", "general", "medium", "new", amir),
            ("Vraag over upgradepakket", "Klant vraagt commerciële informatie.", "Tango Media", "contact@tango.example", "sales", "low", "closed", None),
            ("Betalingsgegevens onduidelijk", "Klant begrijpt factuurgegevens niet.", "Umbra", "finance@umbra.example", "billing", "medium", "waiting", sara),
            ("Systeemmelding bij aanpassen status", "Admin ziet geen duidelijke bevestiging.", "Vertex", "admin@vertex.example", "general", "high", "in_progress", alice),
            ("Incident buiten kantooruren", "Klant meldt urgent probleem in weekend.", "Wave Corp", "ops@wave.example", "technical", "urgent", "new", None),
            ("Rapport bevat gesloten aanvragen", "Dashboard lijkt gesloten aanvragen mee te tellen.", "Xeno", "data@xeno.example", "general", "medium", "resolved", amir),
            ("Zoeken op klantnaam lukt niet", "Gebruiker zoekt klant maar krijgt geen resultaten.", "Yellow Stone", "info@yellow.example", "sales", "medium", "in_progress", sara),
        ]

        requests = []
        for title, description, customer_name, customer_email, category, priority, status, assignee in data:
            item = SupportRequest(
                title=title,
                description=description,
                customer_name=customer_name,
                customer_email=customer_email,
                category=category,
                priority=priority,
                status=status,
                assigned_to_id=assignee.id if assignee else None,
            )
            db.session.add(item)
            requests.append(item)
        db.session.flush()

        comments = [
            Comment(request_id=requests[0].id, user_id=amir.id, body="Klant gevraagd om extra factuurgegevens."),
            Comment(request_id=requests[1].id, user_id=sara.id, body="Uploadprobleem lijkt reproduceerbaar."),
            Comment(request_id=requests[3].id, user_id=sara.id, body="Wacht op feedback van klant."),
            Comment(request_id=requests[5].id, user_id=alice.id, body="Urgente opvolging nodig."),
            Comment(request_id=requests[10].id, user_id=sara.id, body="Traagheid nog niet kunnen reproduceren."),
            Comment(request_id=requests[11].id, user_id=amir.id, body="Prioriteit staat op urgent, maar lijst toont weinig verschil."),
            Comment(request_id=requests[17].id, user_id=sara.id, body="Externe API kan betrokken zijn."),
            Comment(request_id=requests[24].id, user_id=sara.id, body="Zoeken via titel werkt wel."),
        ]
        db.session.add_all(comments)

        db.session.add_all([
            AuditLog(user_id=alice.id, action="seed", entity_type="system", entity_id=None, message="Initial seed data created"),
            AuditLog(user_id=amir.id, action="create", entity_type="request", entity_id=requests[0].id, message=f"Request {requests[0].id} created"),
            AuditLog(user_id=sara.id, action="update", entity_type="request", entity_id=requests[1].id, message=f"Request {requests[1].id} updated"),
            AuditLog(user_id=alice.id, action="update", entity_type="request", entity_id=requests[7].id, message=f"Request {requests[7].id} moved to resolved"),
        ])

        db.session.commit()
        print("Seed completed.")
        print("Login accounts use password: Password123")


if __name__ == "__main__":
    seed()
