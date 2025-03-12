import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",        # Adresse du serveur MySQL
    user="root",             # Nom d'utilisateur MySQL
    password="#####",  # Mot de passe
    database="LaPlateforme"  # Nom de la base de données
)

# Créer un curseur pour exécuter des requêtes
cursor = conn.cursor()

# Requête SQL pour calculer la superficie totale de tous les étages
query = "SELECT SUM(superficie) FROM etage"

# Exécution de la requête
cursor.execute(query)

# Récupération du résultat
resultat = cursor.fetchone()

# Affichage du résultat
if resultat:
    superficie_totale = resultat[0]  # La somme des superficies
    print(f"La superficie de La Plateforme est de {superficie_totale} m2")

# Fermeture du curseur et de la connexion
cursor.close()
conn.close()
