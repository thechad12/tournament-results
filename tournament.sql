--Drop views, tables, and database if it already exists
DROP DATABASE IF EXISTS tournament CASCADE;
DROP VIEW IF EXISTS standings CASCADE;
DROP VIEW IF EXISTS wins CASCADE;
DROP VIEW IF EXISTS losses CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;

--Create the database
CREATE DATABASE tournament;
--Connect to the database
\c tournament;
--Create table containing data about players
CREATE TABLE players (id SERIAL primary key,
						name text);
--Create table containing data about match-ups and results
CREATE TABLE matches (id SERIAL primary key,
						winner int references players(id),
						loser int references players(id));
--Create view to count the wins of a player
CREATE VIEW wins AS SELECT players.id, COUNT(matches.winner) as wins
				FROM players LEFT JOIN matches ON
				players.id = matches.winner GROUP BY players.id;
--Create view to count the losses of a player
CREATE VIEW losses AS SELECT players.id, COUNT(matches.loser) as losses
					FROM players LEFT JOIN matches ON
					players.id = matches.loser GROUP BY players.id;
--Create view to count total matches played by a player
CREATE VIEW count AS SELECT players.id, COUNT(matches) as num_matches FROM players LEFT JOIN matches
						on players.id = matches.winner or players.id = matches.loser GROUP BY players.id;
--Create view for the standings of the players in the tournament
CREATE VIEW standings AS SELECT players.id, players.name, wins.wins, losses.losses, count.num_matches
						FROM players, wins, losses, count
						WHERE players.id = wins.id AND
						players.id = losses.id AND
						players.id = count.id ORDER BY wins DESC;