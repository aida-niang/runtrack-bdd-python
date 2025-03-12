import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",        # Adresse du serveur MySQL
    user="root",             # Nom d'utilisateur MySQL
    password="Benhamath@97",  # Mot de passe
    database="LaPlateforme"  # Nom de la base de données
)

# Créer un curseur pour exécuter des requêtes
cursor = conn.cursor()

# Requête SQL pour calculer la capacité totale de toutes les salles
query = "SELECT SUM(capacite) FROM salle"

# Exécution de la requête
cursor.execute(query)

# Récupération du résultat
resultat = cursor.fetchone()

# Affichage du résultat
if resultat:
    capacite_totale = resultat[0]  # La somme des capacités
    print(f"La capacité totale des salles est de {capacite_totale} personnes")

# Fermeture du curseur et de la connexion
cursor.close()
conn.close()
