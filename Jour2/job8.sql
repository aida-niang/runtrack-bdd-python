CREATE DATABASE zoo;
USE zoo;

CREATE TABLE animal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    race VARCHAR(255),
    id_cage INT,
    date_naissance DATE,
    pays_origine VARCHAR(255),
    FOREIGN KEY (id_cage) REFERENCES cage(id)
);

CREATE TABLE cage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    superficie INT,
    capacite_max INT
);
