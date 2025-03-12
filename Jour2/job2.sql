/usr/local/mysql/bin/mysql -u root -p

USE LaPlateforme;

CREATE TABLE etage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    numero INT NOT NULL,
    superficie INT NOT NULL
);

CREATE TABLE salle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_etage INT NOT NULL,
    capacite INT NOT NULL,
    FOREIGN KEY (id_etage) REFERENCES etage(id) ON DELETE CASCADE
);

SHOW TABLES;

DESCRIBE etage;
DESCRIBE salle;
