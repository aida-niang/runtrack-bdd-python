import mysql.connector

# Se connecter à la base de données
conn = mysql.connector.connect(
    host="localhost",     # Adresse du serveur MySQL
    user="root",          # Nom d'utilisateur MySQL
    password="#####",  # Mot de passe MySQL
    database="LaPlateforme"  # Nom de la base de données
)

# Créer un curseur pour exécuter des requêtes
cursor = conn.cursor()

# Requête SQL pour récupérer les noms et les capacités de la table "salle"
query = "SELECT nom, capacite FROM salle"

# Exécuter la requête
cursor.execute(query)

# Récupérer tous les résultats
resultats = cursor.fetchall()

# Afficher les résultats
for row in resultats:
    print(f"Nom: {row[0]}, Capacité: {row[1]}")

# Fermer le curseur et la connexion
cursor.close()
conn.close()
