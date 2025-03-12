CREATE DATABASE Entreprise;
USE Entreprise;

CREATE TABLE employe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    salaire DECIMAL(10, 2),
    id_service INT
);

INSERT INTO employe (nom, prenom, salaire, id_service)
VALUES
('Dupont', 'Pierre', 3500, 1),
('Lemoine', 'Claire', 2500, 2),
('Martin', 'Paul', 4500, 3),
('Durand', 'Lucie', 3200, 2);

CREATE TABLE service (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255)
);

INSERT INTO service (nom)
VALUES
('Développement'),
('Marketing'),
('Ressources Humaines');

SELECT * FROM employe WHERE salaire > 3000;

SELECT e.nom AS nom_employe, e.prenom AS prenom_employe, e.salaire, s.nom AS nom_service
FROM employe e
JOIN service s ON e.id_service = s.id;
