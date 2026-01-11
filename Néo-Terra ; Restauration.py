import random
import json
import os
from datetime import datetime

class Ingredient:
    def __init__(self, nom, quantite, frais):
        self.nom = nom
        self.quantite = quantite
        self.frais = frais

class Plat:
    def __init__(self, nom, ingredients, temps_preparation, prix):
        self.nom = nom
        self.ingredients = ingredients
        self.temps_preparation = temps_preparation
        self.prix = prix

class Client:
    def __init__(self, nom, patience, budget):
        self.nom = nom
        self.patience = patience
        self.budget = budget

class Employe:
    def __init__(self, nom, competence, salaire):
        self.nom = nom
        self.competence = competence
        self.salaire = salaire

class Quete:
    def __init__(self, nom, description, recompense):
        self.nom = nom
        self.description = description
        self.recompense = recompense
        self.complete = False

class BotConseiller:
    def __init__(self):
        self.conseils = {
            "gestion": "Assurez-vous de toujours avoir assez d'ingrédients en stock pour éviter les pénuries.",
            "plats": "Privilégiez les plats avec un bon rapport qualité-prix pour maximiser vos profits.",
            "clients": "Satisfaire les clients est crucial pour la réputation de votre restaurant.",
            "reputation": "Une bonne réputation attire plus de clients et vous permet d'acheter des ingrédients de meilleure qualité.",
            "employes": "Embaucher des employés compétents peut grandement améliorer l'efficacité de votre restaurant."
        }

    def donner_conseil(self, sujet):
        return self.conseils.get(sujet, "Je n'ai pas de conseil spécifique pour ce sujet.")

class PNJ:
    def __init__(self, nom, dialogue, relation_bonus, objet_donné=None, quête=None):
        self.nom = nom
        self.dialogue = dialogue
        self.relation_bonus = relation_bonus
        self.objet_donné = objet_donné
        self.quête = quête

    def interagir(self, joueur):
        for ligne in self.dialogue:
            print(ligne)
        joueur.relations += self.relation_bonus
        if self.objet_donné and random.random() < 0.7:
            joueur.inventaire.append(self.objet_donné)
            print(f"🎁 {self.nom} vous donne : {self.objet_donné}.")
        if self.quête:
            print(f"📜 {self.nom} vous propose une quête : {self.quête['description']}")
            choix = input("Accepter ? (o/n) ").strip().lower()
            if choix == "o":
                joueur.quêtes_en_cours.append(self.quête)
                print(f"Quête acceptée : {self.quête['objectif']}")
        print(f"👥 Relations : {joueur.relations}")

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
        self.relations = 0
        self.inventaire = []
        self.quêtes_en_cours = []

    def ajouter_score(self, points):
        self.score += points
        print(f"🏆 +{points} points ! Score total : {self.score}")

class Restaurant:
    def __init__(self, nom):
        self.nom = nom
        self.ingredients = []
        self.plats = []
        self.clients = []
        self.employes = []
        self.reputation = 0
        self.argent = 1000
        self.jour = 1
        self.quetes = []
        self.bot = BotConseiller()
        self.joueur = Joueur("Mick")

    def ajouter_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def ajouter_plat(self, plat):
        self.plats.append(plat)

    def embaucher_employe(self, employe):
        self.employes.append(employe)

    def servir_client(self, client):
        self.clients.append(client)

    def preparer_plat(self, plat):
        for ingredient in plat.ingredients:
            found = False
            for inv_ingredient in self.ingredients:
                if inv_ingredient.nom == ingredient.nom and inv_ingredient.quantite >= 1:
                    found = True
                    inv_ingredient.quantite -= 1
                    break
            if not found:
                print(f"Ingrédient manquant : {ingredient.nom}")
                return False
        print(f"Plat '{plat.nom}' préparé avec succès!")
        return True

    def mise_a_jour_reputation(self, satisfaction):
        self.reputation += satisfaction

    def ajouter_argent(self, montant):
        self.argent += montant

    def retirer_argent(self, montant):
        if self.argent >= montant:
            self.argent -= montant
            return True
        else:
            print("Pas assez d'argent!")
            return False

    def ajouter_quete(self, quete):
        self.quetes.append(quete)

    def completer_quete(self, nom_quete):
        for quete in self.quetes:
            if quete.nom == nom_quete:
                quete.complete = True
                self.argent += quete.recompense
                self.joueur.ajouter_score(quete.recompense)
                print(f"Quête '{quete.nom}' complétée ! Récompense : {quete.recompense}€")
                return True
        print("Quête non trouvée.")
        return False

    def passer_jour(self):
        self.jour += 1
        print(f"\n--- Jour {self.jour} ---")

def generer_client():
    noms = ["Client1", "Client2", "Client3", "Client4", "Client5"]
    nom = random.choice(noms)
    patience = random.randint(10, 30)
    budget = random.randint(20, 100)
    return Client(nom, patience, budget)

def afficher_tableau_scores():
    try:
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                scores = json.load(f)
            print("\n===== TABLEAU DES SCORES =====")
            for i, (nom, data) in enumerate(sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True), 1):
                print(f"{i}. {nom} : {data['score']} pts | Jours : {data['jours']} | Réputation : {data['reputation']}")
        else:
            print("Aucun score enregistré.")
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des scores : {e}")

def enregistrer_score(joueur, restaurant):
    try:
        scores = {}
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                scores = json.load(f)
        scores[joueur.nom] = {
            "score": joueur.score,
            "jours": restaurant.jour,
            "reputation": restaurant.reputation,
            "date": str(datetime.now())
        }
        with open("scores.json", "w") as f:
            json.dump(scores, f)
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement du score : {e}")

def main():
    # Initialisation du restaurant
    restaurant = Restaurant("Chez Mick")

    # Ajout de nombreux ingrédients
    ingrédients = [
        Ingredient("Poisson", 10, True),
        Ingredient("Crevettes", 15, True),
        Ingredient("Légumes", 20, True),
        Ingredient("Riz", 30, False),
        Ingredient("Ail", 10, True),
        Ingredient("Beurre", 10, False),
        Ingredient("Tomates", 15, True),
        Ingredient("Oignons", 15, True),
        Ingredient("Poivrons", 15, True),
        Ingredient("Pommes de terre", 20, False),
        Ingredient("Carottes", 15, False),
        Ingredient("Poulet", 10, True),
        Ingredient("Bœuf", 10, True),
        Ingredient("Pâtes", 20, False),
        Ingredient("Fromage", 10, False),
        Ingredient("Crème", 10, False),
        Ingredient("Champignons", 10, True),
        Ingredient("Salade", 15, True),
        Ingredient("Pommes", 10, True),
        Ingredient("Bananes", 10, True),
        Ingredient("Fraise", 10, True),
        Ingredient("Chocolat", 10, False),
        Ingredient("Sucre", 20, False),
        Ingredient("Farine", 20, False),
        Ingredient("Œufs", 10, True),
        Ingredient("Lait", 10, True),
        Ingredient("Pain", 10, False),
        Ingredient("Vin", 5, False),
        Ingredient("Bière", 5, False),
        Ingredient("Eau", 50, False)
    ]
    for ingredient in ingrédients:
        restaurant.ajouter_ingredient(ingredient)

    # Ajout de nombreux plats
    plats = [
        Plat("Grillade de poisson", [ingrédients[0]], 10, 15),
        Plat("Crevettes grillées", [ingrédients[1]], 8, 12),
        Plat("Poisson aux légumes", [ingrédients[0], ingrédients[2]], 12, 18),
        Plat("Riz aux crevettes", [ingrédients[1], ingrédients[3]], 10, 14),
        Plat("Poisson frit", [ingrédients[0]], 15, 16),
        Plat("Crevettes à l'ail", [ingrédients[1], ingrédients[4]], 10, 14),
        Plat("Crevettes au beurre", [ingrédients[1], ingrédients[5]], 12, 16),
        Plat("Salade de légumes", [ingrédients[2], ingrédients[6]], 5, 10),
        Plat("Légumes grillés", [ingrédients[2], ingrédients[7], ingrédients[8]], 8, 12),
        Plat("Riz frit", [ingrédients[3], ingrédients[2]], 10, 12),
        Plat("Paella", [ingrédients[3], ingrédients[0], ingrédients[1], ingrédients[2]], 20, 25),
        Plat("Plat du chef", [ingrédients[0], ingrédients[1], ingrédients[2], ingrédients[3], ingrédients[4], ingrédients[5]], 25, 30),
        Plat("Pommes de terre rôties", [ingrédients[9]], 10, 8),
        Plat("Carottes rôties", [ingrédients[10]], 8, 7),
        Plat("Poulet grillé", [ingrédients[11]], 12, 14),
        Plat("Bœuf grillé", [ingrédients[12]], 15, 18),
        Plat("Pâtes aux champignons", [ingrédients[13], ingrédients[14]], 12, 15),
        Plat("Pâtes à la crème", [ingrédients[13], ingrédients[15]], 10, 12),
        Plat("Salade César", [ingrédients[16], ingrédients[11], ingrédients[17]], 10, 14),
        Plat("Tarte aux pommes", [ingrédients[18], ingrédients[19], ingrédients[20]], 15, 12),
        Plat("Bananes flambées", [ingrédients[19], ingrédients[20], ingrédients[21]], 10, 10),
        Plat("Fraise au chocolat", [ingrédients[20], ingrédients[21]], 5, 8),
        Plat("Omelette aux champignons", [ingrédients[22], ingrédients[14]], 10, 10),
        Plat("Crêpes", [ingrédients[23], ingrédients[22], ingrédients[24]], 12, 10),
        Plat("Gâteau au chocolat", [ingrédients[21], ingrédients[20], ingrédients[23]], 20, 15),
        Plat("Sandwich au poulet", [ingrédients[17], ingrédients[11]], 8, 10),
        Plat("Sandwich au bœuf", [ingrédients[17], ingrédients[12]], 10, 12),
        Plat("Pâtes au fromage", [ingrédients[13], ingrédients[15]], 10, 12),
        Plat("Riz au poulet", [ingrédients[3], ingrédients[11]], 12, 14),
        Plat("Riz au bœuf", [ingrédients[3], ingrédients[12]], 15, 16),
        Plat("Pommes de terre au fromage", [ingrédients[9], ingrédients[15]], 10, 10),
        Plat("Carottes au beurre", [ingrédients[10], ingrédients[5]], 8, 8),
        Plat("Salade de fruits", [ingrédients[18], ingrédients[19], ingrédients[20]], 5, 8),
        Plat("Poulet aux légumes", [ingrédients[11], ingrédients[2]], 12, 14),
        Plat("Bœuf aux légumes", [ingrédients[12], ingrédients[2]], 15, 16),
        Plat("Poulet à la crème", [ingrédients[11], ingrédients[15]], 12, 14),
        Plat("Bœuf à la crème", [ingrédients[12], ingrédients[15]], 15, 16),
        Plat("Frites", [ingrédients[9]], 10, 5),
        Plat("Purée de pommes de terre", [ingrédients[9], ingrédients[24]], 10, 8),
        Plat("Soupe de légumes", [ingrédients[2], ingrédients[10], ingrédients[7]], 10, 8),
        Plat("Soupe de poisson", [ingrédients[0], ingrédients[7], ingrédients[6]], 12, 10),
        Plat("Soupe de poulet", [ingrédients[11], ingrédients[10], ingrédients[7]], 10, 9),
        Plat("Soupe de bœuf", [ingrédients[12], ingrédients[10], ingrédients[7]], 12, 10),
        Plat("Pizza", [ingrédients[17], ingrédients[15], ingrédients[6]], 15, 12),
        Plat("Tarte aux fraises", [ingrédients[20], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux pommes", [ingrédients[18], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte au chocolat", [ingrédients[21], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte à la banane", [ingrédients[19], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte à la crème", [ingrédients[15], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux champignons", [ingrédients[14], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux légumes", [ingrédients[2], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte au poulet", [ingrédients[11], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte au bœuf", [ingrédients[12], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte au poisson", [ingrédients[0], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte aux crevettes", [ingrédients[1], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte aux pommes de terre", [ingrédients[9], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux carottes", [ingrédients[10], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux oignons", [ingrédients[7], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux poivrons", [ingrédients[8], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux tomates", [ingrédients[6], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux ail", [ingrédients[4], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux fromage", [ingrédients[15], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux œufs", [ingrédients[22], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux lait", [ingrédients[24], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux pain", [ingrédients[17], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux vin", [ingrédients[25], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte aux bière", [ingrédients[26], ingrédients[20], ingrédients[23]], 15, 12),
        Plat("Tarte aux eau", [ingrédients[27], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux sucre", [ingrédients[21], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux farine", [ingrédients[23], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux chocolat", [ingrédients[21], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux fraise", [ingrédients[20], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux pommes", [ingrédients[18], ingrédients[20], ingrédients[23]], 15, 10),
        Plat("Tarte aux bananes", [ingrédients[19], ingrédients[20], ingrédients[23]], 15, 10)
    ]
    for plat in plats:
        restaurant.ajouter_plat(plat)

    # Ajout d'employés
    cuisinier = Employe("Cuisinier", "cuisine", 500)
    serveur = Employe("Serveur", "service", 400)
    restaurant.embaucher_employe(cuisinier)
    restaurant.embaucher_employe(serveur)

    # Ajout de PNJ
    pnj1 = PNJ("Dr. Elena", ["'Vite, entrez ! Ils nous traquent...'", "'Prenez ça. Ça pourrait vous sauver.'", "'Ne faites pas confiance à ce que vous voyez. Rien n'est réel ici.'"], 15, "Potion de soin")
    pnj2 = PNJ("L'Homme aux yeux vides", ["'Ils sont partout...' *il regarde derrière vous*", "'Ne va pas dans les égouts. J'AI VU DES CHOSES.'", "*Il rit hystériquement.* 'Vous aussi vous êtes un leurre ?'", "*Il chuchote* 'Le code... le code pour sortir... c'est...' *il s'effondre*"], -10, None)
    pnj3 = PNJ("Dr. Kael", ["'Ah, un nouveau sujet d'expérience !' *il rit*", "'Je peux vous aider... pour un prix.'", "'La vérité ? Cette simulation est une prison. Et vous en êtes la clé.'"], -20, "Clé de laboratoire")

    # Ajout de quêtes
    quete1 = Quete("Premier plat", "Préparez votre premier plat.", 100)
    quete2 = Quete("Client satisfait", "Satisfaire un client avec un plat.", 150)
    quete3 = Quete("Embaucher un employé", "Embauchez un nouveau cuisinier.", 200)
    quete4 = Quete("Réputation élevée", "Atteignez une réputation de 10.", 300)
    quete5 = Quete("Plat spécial", "Préparez le plat du chef.", 250)
    restaurant.ajouter_quete(quete1)
    restaurant.ajouter_quete(quete2)
    restaurant.ajouter_quete(quete3)
    restaurant.ajouter_quete(quete4)
    restaurant.ajouter_quete(quete5)

    # Ajout de clients
    for _ in range(5):
        restaurant.servir_client(generer_client())

    # Boucle principale du jeu
    while restaurant.reputation < 1000 and restaurant.reputation >= -50:
        print("\n--- Nouvelle journée au restaurant ---")
        print(f"Argent: {restaurant.argent}, Réputation: {restaurant.reputation}, Jour: {restaurant.jour}")
        print(f"Score: {restaurant.joueur.score}")

        # Afficher les options principales
        print("\nQue voulez-vous faire ?")
        print("1. Préparer un plat")
        print("2. Embaucher un employé")
        print("3. Servir un client")
        print("4. Interagir avec un PNJ")
        print("5. Voir les quêtes")
        print("6. Parler au bot conseiller")
        print("7. Voir le tableau des scores")
        print("8. Passer au jour suivant")
        print("9. Quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            print("\nPlats disponibles :")
            for i, plat in enumerate(restaurant.plats):
                print(f"{i+1}. {plat.nom} - Prix: {plat.prix}, Temps de préparation: {plat.temps_preparation}")

            choix_plat = input("Choisissez un plat à préparer (ou 'annuler' pour revenir en arrière) : ")
            if choix_plat.lower() == 'annuler':
                continue

            try:
                choix_plat = int(choix_plat) - 1
                if 0 <= choix_plat < len(restaurant.plats):
                    plat_choisi = restaurant.plats[choix_plat]
                    if restaurant.preparer_plat(plat_choisi):
                        # Calculer la satisfaction du client
                        satisfaction = min(10, plat_choisi.prix // 2 + (20 - plat_choisi.temps_preparation))
                        restaurant.mise_a_jour_reputation(satisfaction)
                        restaurant.ajouter_argent(plat_choisi.prix)
                        restaurant.joueur.ajouter_score(plat_choisi.prix)
                        print(f"Client satisfait ! Satisfaction: {satisfaction}, Argent gagné: {plat_choisi.prix}")
                        if not quete1.complete:
                            restaurant.completer_quete("Premier plat")
                        if plat_choisi.nom == "Plat du chef" and not quete5.complete:
                            restaurant.completer_quete("Plat spécial")
                    else:
                        print("Impossible de préparer le plat.")
                else:
                    print("Numéros de plat invalide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro de plat.")

        elif choix == "2":
            print("\nEmployés disponibles à embaucher :")
            print("1. Cuisinier (500€)")
            print("2. Serveur (400€)")

            employe_choisi = input("Choisissez un employé à embaucher (ou 'annuler' pour revenir en arrière) : ")
            if employe_choisi.lower() == 'annuler':
                continue

            if employe_choisi == "1":
                if restaurant.retirer_argent(500):
                    restaurant.embaucher_employe(Employe("Cuisinier2", "cuisine", 500))
                    print("Un nouveau cuisinier a été embauché !")
                    if not quete3.complete:
                        restaurant.completer_quete("Embaucher un employé")
            elif employe_choisi == "2":
                if restaurant.retirer_argent(400):
                    restaurant.embaucher_employe(Employe("Serveur2", "service", 400))
                    print("Un nouveau serveur a été embauché !")
            else:
                print("Option invalide.")

        elif choix == "3":
            if restaurant.clients:
                client = restaurant.clients.pop(0)
                print(f"\nServir {client.nom} :")
                print(f"Budget du client: {client.budget}€")

                print("\nPlats disponibles :")
                for i, plat in enumerate(restaurant.plats):
                    print(f"{i+1}. {plat.nom} - Prix: {plat.prix}")

                choix_plat = input("Choisissez un plat à servir (ou 'annuler' pour revenir en arrière) : ")
                if choix_plat.lower() == 'annuler':
                    continue

                try:
                    choix_plat = int(choix_plat) - 1
                    if 0 <= choix_plat < len(restaurant.plats):
                        plat_choisi = restaurant.plats[choix_plat]
                        if client.budget >= plat_choisi.prix:
                            client.budget -= plat_choisi.prix
                            restaurant.ajouter_argent(plat_choisi.prix)
                            restaurant.joueur.ajouter_score(plat_choisi.prix)
                            print(f"{client.nom} a été servi avec {plat_choisi.nom}.")
                            satisfaction = min(10, plat_choisi.prix // 2)
                            restaurant.mise_a_jour_reputation(satisfaction)
                            print(f"Satisfaction du client: {satisfaction}")
                            if not quete2.complete:
                                restaurant.completer_quete("Client satisfait")
                        else:
                            print(f"{client.nom} n'a pas assez d'argent pour ce plat.")
                    else:
                        print("Numéros de plat invalide.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer un numéro de plat.")
            else:
                print("Aucun client à servir pour le moment.")

        elif choix == "4":
            print("\nPNJ disponibles :")
            print("1. Dr. Elena")
            print("2. L'Homme aux yeux vides")
            print("3. Dr. Kael")

            choix_pnj = input("Choisissez un PNJ pour interagir (ou 'annuler' pour revenir en arrière) : ")
            if choix_pnj.lower() == 'annuler':
                continue

            if choix_pnj == "1":
                pnj1.interagir(restaurant.joueur)
            elif choix_pnj == "2":
                pnj2.interagir(restaurant.joueur)
            elif choix_pnj == "3":
                pnj3.interagir(restaurant.joueur)
            else:
                print("Option invalide.")

        elif choix == "5":
            print("\nQuêtes disponibles :")
            for i, quete in enumerate(restaurant.quetes):
                statut = "Complétée" if quete.complete else "En cours"
                print(f"{i+1}. {quete.nom} - {quete.description} (Récompense: {quete.recompense}€) - {statut}")

        elif choix == "6":
            print("\nQuels conseils souhaitez-vous ?")
            print("1. Gestion des ingrédients")
            print("2. Préparation des plats")
            print("3. Interactions avec les clients")
            print("4. Amélioration de la réputation")
            print("5. Gestion des employés")

            sujet = input("Choisissez un sujet (ou 'annuler' pour revenir en arrière) : ")
            if sujet.lower() == 'annuler':
                continue

            sujets = {
                "1": "gestion",
                "2": "plats",
                "3": "clients",
                "4": "reputation",
                "5": "employes"
            }
            conseil = restaurant.bot.donner_conseil(sujets.get(sujet, ""))
            print(f"\nConseil du bot : {conseil}")

        elif choix == "7":
            afficher_tableau_scores()

        elif choix == "8":
            restaurant.passer_jour()
            # Ajouter de nouveaux clients chaque jour
            for _ in range(random.randint(1, 5)):
                restaurant.servir_client(generer_client())
            # Vérifier si la quête de réputation est complétée
            if restaurant.reputation >= 10 and not quete4.complete:
                restaurant.completer_quete("Réputation élevée")

        elif choix == "9":
            print("Merci d'avoir joué à Chef de la Côte !")
            enregistrer_score(restaurant.joueur, restaurant)
            break

        else:
            print("Option invalide, veuillez réessayer.")

    # Fin du jeu
    if restaurant.reputation >= 1000:
        print("\n===== FIN DE PARTIE =====")
        print("Félicitations ! Votre restaurant est devenu une légende culinaire !")
        print(f"Score final : {restaurant.joueur.score}")
        enregistrer_score(restaurant.joueur, restaurant)
        afficher_tableau_scores()
    elif restaurant.reputation < -50:
        print("\n===== FIN DE PARTIE =====")
        print("Désolé, votre restaurant a fait faillite...")
        print(f"Score final : {restaurant.joueur.score}")
        enregistrer_score(restaurant.joueur, restaurant)
        afficher_tableau_scores()

if __name__ == "__main__":
    main()

