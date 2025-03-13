import mysql.connector

# Connexion à la base de données
try:
    conn = mysql.connector.connect(
        host="localhost",  # Remplace si nécessaire
        user="root",       # Remplace si ton utilisateur MySQL est différent
        password="Benhamath@97",  # Remplace avec ton mot de passe MySQL
        database="LaPlateforme"
    )

    if conn.is_connected():
        print("✅ Connexion réussie à la base de données !")

    cursor = conn.cursor()

    # Exécuter la requête pour récupérer tous les étudiants
    cursor.execute("SELECT * FROM etudiant")

    # Récupérer et afficher les résultats
    etudiants = cursor.fetchall()

    print("\n📌 Liste des étudiants :")
    for etudiant in etudiants:
        print(etudiant)

except mysql.connector.Error as err:
    print(f"❌ Erreur : {err}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔌 Connexion fermée.")
