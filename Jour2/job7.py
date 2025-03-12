import mysql.connector

class Employe:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.cursor = self.conn.cursor()

    def create_employe(self, nom, prenom, salaire, id_service):
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (nom, prenom, salaire, id_service))
        self.conn.commit()
        print(f"Employé {nom} {prenom} ajouté avec succès.")

    def get_employes(self):
        query = "SELECT * FROM employe"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Salaire: {row[3]}, Service ID: {row[4]}")

    def update_salaire(self, id, nouveau_salaire):
        query = "UPDATE employe SET salaire = %s WHERE id = %s"
        self.cursor.execute(query, (nouveau_salaire, id))
        self.conn.commit()
        print(f"Salaire de l'employé ID {id} mis à jour à {nouveau_salaire} €.")

    def delete_employe(self, id):
        query = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()
        print(f"Employé ID {id} supprimé.")

    def get_employes_par_salaire(self, salaire_min):
        query = "SELECT * FROM employe WHERE salaire > %s"
        self.cursor.execute(query, (salaire_min,))
        result = self.cursor.fetchall()
        for row in result:
            print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Salaire: {row[3]}, Service ID: {row[4]}")

    def close(self):
        self.cursor.close()
        self.conn.close()

db_host = "localhost"      # Adresse du serveur
db_user = "root"           # Nom d'utilisateur
db_password = "#####"   # Mot de passe
db_name = "Entreprise"     # Nom de la base de données

employe_manager = Employe(db_host, db_user, db_password, db_name)

# Ajouter un employé
employe_manager.create_employe("Bernard", "Jacques", 3200, 1)

# Récupérer tous les employés
employe_manager.get_employes()

# Mettre à jour un salaire
employe_manager.update_salaire(1, 3700)

# Supprimer un employé
employe_manager.delete_employe(2)

# Récupérer les employés avec un salaire supérieur à 3000 €
employe_manager.get_employes_par_salaire(3000)

# Fermer la connexion
employe_manager.close()
