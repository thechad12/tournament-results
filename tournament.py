#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE FROM matches";
    db_cursor.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    db_cursor = conn.cursor()
    query = "DELETE FROM players";
    db_cursor.execute(query)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn= connect()
    db_cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM players";
    db_cursor.execute(query)
    results = db_cursor.fetchone()[0]
    return results
    conn.close()

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    db_cursor.execute(query, (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "SELECT players.id, players.name, wins.wins, count.num_matches\
                        FROM players, wins, count\
                        WHERE players.id = wins.id AND\
                        players.id = count.id ORDER BY wins DESC";
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    db_cursor = conn.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)";
    db_cursor.execute(query, (int(winner), int(loser)))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    num = int(countPlayers())
    pairings = []
    if (num > 0):
        for i in range (num):
            if (i % 2 == 0):
                id1 = standings[i][0]
                name1 = standings[i][1]
                id2 = standings[i + 1][0]
                name2 = standings[i + 1][1]
                pair = (id1, name1, id2, name2)
                pairings.append(pair)
    return pairings