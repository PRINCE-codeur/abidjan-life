import json
import os
import random

FICHIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sauvegarde.json")

QUARTIERS = {
    "Abobo": 0.9,
    "Yopougon": 1.0,
    "Marcory": 1.1,
    "Cocody": 1.3,
    "Plateau": 1.5,
}
METIERS = {
    "Livreur": (3000, 6000),
    "Vendeur au marché": (2500, 5500),
    "Aide mécanicien": (3500, 7000),
}
PRIX_MOTO = 150000
PRIX_COMMERCE = 200000
ETAPES_MAISON = [("les fondations", 300000), ("les murs", 500000), ("le toit", 400000)]


def sauvegarder(e):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(e, f)
    print("Partie sauvegardée.")


def charger():
    try:
        with open(FICHIER, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def statut(e):
    print("\n--- STATUT ---")
    print(f"Jour {e['jour']} | Quartier : {e['quartier']}")
    print(f"Argent : {e['argent']} FCFA | Énergie : {e['energie']}/100")
    print(f"Moto : {'oui' if e['moto'] else 'non'} | Commerce : {'oui' if e['commerce'] else 'non'}")
    print(f"Maison : {e['maison']}/{len(ETAPES_MAISON)} étapes")


def fin_de_journee(e):
    e["jour"] += 1
    e["energie"] = 100
    e["argent"] = max(0, e["argent"] - 1000)
    print("\nTu dors. Nourriture et transport : -1000 FCFA.")
    if e["commerce"]:
        gain = random.randint(4000, 9000)
        e["argent"] += gain
        print(f"Ton commerce rapporte {gain} FCFA.")


def travailler(e):
    if e["energie"] < 30:
        print("Trop fatigué. Repose-toi d'abord.")
        return
    metier = random.choice(list(METIERS))
    bas, haut = METIERS[metier]
    gain = random.randint(bas, haut) * QUARTIERS[e["quartier"]]
    if e["moto"]:
        gain *= 1.3
    gain = int(gain)
    e["argent"] += gain
    e["energie"] -= 30
    print(f"Tu travailles comme {metier} à {e['quartier']} : +{gain} FCFA.")
    if random.random() < 0.15:
        e["argent"] = max(0, e["argent"] - 1500)
        print("Mauvaise surprise (embouteillage, pickpocket...) : -1500 FCFA.")


def voyager(e):
    noms = list(QUARTIERS)
    for i, nom in enumerate(noms, 1):
        print(f"{i}. {nom}")
    choix = input("Quartier ? ")
    if not choix.isdigit() or not 1 <= int(choix) <= len(noms):
        print("Choix invalide.")
        return
    cout = 300 if e["moto"] else 800
    if e["argent"] < cout:
        print("Pas assez d'argent pour le transport.")
        return
    e["argent"] -= cout
    e["quartier"] = noms[int(choix) - 1]
    print(f"Tu arrives à {e['quartier']} (transport : -{cout} FCFA).")


def acheter(e, cle, prix, message):
    if e[cle]:
        print("Tu l'as déjà.")
    elif e["argent"] < prix:
        print(f"Il te faut {prix} FCFA.")
    else:
        e["argent"] -= prix
        e[cle] = True
        print(message)


def construire(e):
    if e["maison"] >= len(ETAPES_MAISON):
        return
    nom, prix = ETAPES_MAISON[e["maison"]]
    if e["argent"] < prix:
        print(f"Pour {nom}, il te faut {prix} FCFA.")
        return
    e["argent"] -= prix
    e["maison"] += 1
    print(f"Tu as construit {nom} !")


def main():
    print("=== ABIDJAN LIFE ===")
    print("Objectif : construire ta maison. Bonne chance !")
    e = None
    if os.path.exists(FICHIER) and input("Continuer ta partie sauvegardée ? (o/n) ").lower() == "o":
        e = charger()
        if e is None:
            print("Sauvegarde illisible, nouvelle partie.")
    if e is None:
        e = {"jour": 1, "argent": 5000, "energie": 100, "quartier": "Yopougon",
             "moto": False, "commerce": False, "maison": 0}
    while e["maison"] < len(ETAPES_MAISON):
        statut(e)
        print("\n1. Travailler")
        print("2. Dormir (jour suivant)")
        print("3. Changer de quartier")
        print(f"4. Acheter une moto ({PRIX_MOTO} FCFA)")
        print(f"5. Ouvrir un commerce ({PRIX_COMMERCE} FCFA)")
        print("6. Construire la maison")
        print("7. Sauvegarder")
        print("0. Quitter")
        choix = input("> ").strip()
        if choix == "1":
            travailler(e)
        elif choix == "2":
            fin_de_journee(e)
        elif choix == "3":
            voyager(e)
        elif choix == "4":
            acheter(e, "moto", PRIX_MOTO, "Tu as une moto ! Tu gagnes plus et voyages moins cher.")
        elif choix == "5":
            acheter(e, "commerce", PRIX_COMMERCE, "Ton commerce est ouvert ! Revenu chaque jour.")
        elif choix == "6":
            construire(e)
        elif choix == "7":
            sauvegarder(e)
        elif choix == "0":
            if input("Sauvegarder avant de quitter ? (o/n) ").lower() == "o":
                sauvegarder(e)
            print("À bientôt !")
            return
        else:
            print("Choix invalide.")
    print(f"\nBRAVO ! Ta maison est terminée au jour {e['jour']} !")


main()
input("appuie sur entreé pour fermer")