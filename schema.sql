DROP TABLE IF EXISTS groupe;
DROP TABLE IF EXISTS commentaire;

CREATE TABLE groupe (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nom TEXT UNIQUE NOT NULL,
	description TEXT NOT NULL
);

CREATE TABLE commentaire (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	auteur TEXT DEFAULT "Anonyme",
	commentaire TEXT NOT NULL,
	groupe INTEGER NOT NULL,
	creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (groupe) REFERENCES groupe(id)
);

INSERT INTO groupe(nom, description) VALUES ('Muse', 'Créé en 1994.');
INSERT INTO commentaire (auteur, commentaire, groupe) VALUES ('Toto', "Super groupe", (SELECT id FROM groupe WHERE nom = 'Muse'));
INSERT INTO commentaire (auteur, commentaire, groupe) VALUES ('Tata', "J'adore !", (SELECT id FROM groupe WHERE nom = 'Muse'));
INSERT INTO groupe(nom, description) VALUES ('Linkin Park', 'Créé en 1996.');
INSERT INTO commentaire (auteur, commentaire, groupe) VALUES ('Pallo', "J'écoute ce groupe tous les soirs, génial !", (SELECT id FROM groupe WHERE nom = 'Linkin Park'));
INSERT INTO groupe(nom, description) VALUES ('Green Day', 'Créé en 1987.');