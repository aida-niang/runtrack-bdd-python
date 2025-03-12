import mysql.connector

class Zoo:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.cursor = self.conn.cursor()

    def add_animal(self, nom, race, id_cage, date_naissance, pays_origine):
        query = """
        INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (nom, race, id_cage, date_naissance, pays_origine))
        self.conn.commit()
        print(f"Animal {nom} ajouté avec succès.")

    def remove_animal(self, animal_id):
        query = "DELETE FROM animal WHERE id = %s"
        self.cursor.execute(query, (animal_id,))
        self.conn.commit()
        print(f"Animal ID {animal_id} supprimé.")

    def update_animal(self, animal_id, nom=None, race=None, id_cage=None, date_naissance=None, pays_origine=None):
        query = "UPDATE animal SET "
        params = []
        if nom: query += "nom = %s, "; params.append(nom)
        if race: query += "race = %s, "; params.append(race)
        if id_cage: query += "id_cage = %s, "; params.append(id_cage)
        if date_naissance: query += "date_naissance = %s, "; params.append(date_naissance)
        if pays_origine: query += "pays_origine = %s, "; params.append(pays_origine)
        query = query.rstrip(', ')  # Remove the last comma
        query += " WHERE id = %s"
        params.append(animal_id)

        self.cursor.execute(query, tuple(params))
        self.conn.commit()
        print(f"Animal ID {animal_id} mis à jour.")

    def add_cage(self, superficie, capacite_max):
        query = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
        self.cursor.execute(query, (superficie, capacite_max))
        self.conn.commit()
        print(f"Cage ajoutée avec superficie {superficie} m2 et capacité maximale {capacite_max} animaux.")

    def remove_cage(self, cage_id):
        query = "DELETE FROM cage WHERE id = %s"
        self.cursor.execute(query, (cage_id,))
        self.conn.commit()
        print(f"Cage ID {cage_id} supprimée.")

    def update_cage(self, cage_id, superficie=None, capacite_max=None):
        query = "UPDATE cage SET "
        params = []
        if superficie: query += "superficie = %s, "; params.append(superficie)
        if capacite_max: query += "capacite_max = %s, "; params.append(capacite_max)
        query = query.rstrip(', ')  # Remove the last comma
        query += " WHERE id = %s"
        params.append(cage_id)

        self.cursor.execute(query, tuple(params))
        self.conn.commit()
        print(f"Cage ID {cage_id} mise à jour.")

    def list_animals(self):
        query = "SELECT * FROM animal"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(f"ID: {row[0]}, Nom: {row[1]}, Race: {row[2]}, Cage ID: {row[3]}, Date de naissance: {row[4]}, Pays d'origine: {row[5]}")

    def list_animals_in_cage(self):
        query = """
        SELECT cage.id, cage.superficie, animal.nom, animal.race
        FROM cage
        LEFT JOIN animal ON cage.id = animal.id_cage
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            print(f"Cage ID: {row[0]}, Superficie: {row[1]} m2, Animal: {row[2] if row[2] else 'Aucun'}, Race: {row[3] if row[3] else 'N/A'}")

    def total_cage_area(self):
        query = "SELECT SUM(superficie) FROM cage"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print(f"La superficie totale de toutes les cages est de {result[0]} m2.")

    def close(self):
        self.cursor.close()
        self.conn.close()

db_host = "localhost"
db_user = "root"
db_password = "#####"
db_name = "zoo"

zoo_manager = Zoo(db_host, db_user, db_password, db_name)

# Ajouter une cage
zoo_manager.add_cage(100, 5)

# Ajouter des animaux
zoo_manager.add_animal("Lion", "Panthera leo", 1, "2015-06-15", "Afrique")
zoo_manager.add_animal("Tigre", "Panthera tigris", 1, "2016-08-22", "Asie")

# Afficher tous les animaux
zoo_manager.list_animals()

# Afficher les animaux dans leurs cages
zoo_manager.list_animals_in_cage()

# Calculer la superficie totale des cages
zoo_manager.total_cage_area()

# Mettre à jour un animal
zoo_manager.update_animal(1, nom="Lionceau")

# Supprimer un animal
zoo_manager.remove_animal(2)

# Supprimer une cage
zoo_manager.remove_cage(1)

# Fermer la connexion à la base de données
zoo_manager.close()
