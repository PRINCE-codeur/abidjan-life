print("==============================")
print("   MA CALCULATRICE PYTHON")
print("==============================")

nom = input("Comment tu t'appelles ? ")

print()
print("Bienvenue", nom, "!")
print("Voici ta calculatrice.")

while True:
    print()
    print("======= MENU =======")
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Quitter")
    print("====================")

    choix = input("Choisis une operation (1-5) : ")

    if choix == "5":
        print("Merci", nom, "!")
        print("A bientot !")
        break

    if choix not in ["1", "2", "3", "4"]:
        print("Choix invalide. Reessaie.")
        continue

    try:
        nombre1 = float(input("Entre le premier nombre : "))
        nombre2 = float(input("Entre le deuxieme nombre : "))

        if choix == "1":
            resultat = nombre1 + nombre2
            print("Resultat :", resultat)

        elif choix == "2":
            resultat = nombre1 - nombre2
            print("Resultat :", resultat)

        elif choix == "3":
            resultat = nombre1 * nombre2
            print("Resultat :", resultat)

        elif choix == "4":
            if nombre2 == 0:
                print("Erreur : division par zero impossible.")
            else:
                resultat = nombre1 / nombre2
                print("Resultat :", resultat)

    except ValueError:
        print("Erreur : entre uniquement des nombres.")

print("Fin du programme.")