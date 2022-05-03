import sqlite3
import os
from random import randrange

#create databases and all tables
def create_tables():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()

    cur.execute(''' CREATE TABLE pokemon
(id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(25)
);''')

    cur.execute(''' CREATE TABLE user
(id INTEGER PRIMARY KEY AUTOINCREMENT,
did VARCHAR(40)
);''')

    cur.execute(''' CREATE TABLE userpokemon
(id INTEGER PRIMARY KEY AUTOINCREMENT,
did VARCHAR(40),
pid VARCHAR(40),
lvl VARCHAR(4),
maxhp int(3),
hp int(3),
item VARCHAR(40),
exp int(3)
);''')

    cur.execute(''' CREATE TABLE spawnedpokemon
(id INTEGER PRIMARY KEY AUTOINCREMENT,
pid VARCHAR(40),
lvl VARCHAR(4),
maxhp int(10),
item VARCHAR(40),
caught int(1),
hp int(10)
);''')

    cur.execute(''' CREATE TABLE skills
(id INTEGER PRIMARY KEY AUTOINCREMENT,
pid VARCHAR(40),
sname VARCHAR(40),
damage int(3)
);''')

    cur.execute(''' CREATE TABLE userprimepokemon
(id INTEGER PRIMARY KEY AUTOINCREMENT,
did VARCHAR(40),
upid VARCHAR(40)
);''')



# get all characters from folder and add them to database, make sure every 
# gif or image is named after the character only

def pokemon_2_db():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()

    for pkmn in os.listdir('./static/pokemon/pokemon-normal'):
        print(pkmn[:-4])
        cur.execute('INSERT INTO pokemon (name) VALUES ("{0}");'.format(pkmn[:-4]))
        cur.execute('COMMIT;')

#print all characters you have in the database
def check_pkmn_db():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM pokemon;')
    for pkmn in cur.fetchall():
        print(pkmn)

#register a users discord id to the database
def register_user(did):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    print(did)
    cur.execute('INSERT INTO user (did) VALUES ({0});'.format(did))
    cur.execute('COMMIT;')

#check if user exist by discord id
def chk_user_exist(did):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT did FROM user WHERE did = {0}'.format(did))
    if cur.fetchall() == []:
        return False
    else:
        return True

#create the users inventory param1 is
#def create_user_inventory(did):
#   con = sqlite3.connect('pokemon.db')
#  cur = con.cursor()
# print(did)
# cur.execute('INSERT INTO user (did) VALUES ({0});'.format(did))
#cur.execute('COMMIT;')


def spawn_random_pkmn():
    #banned pokemon ids will go in this list if you dont want to spawn them
    banned_list = []

    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    #gerenate a randome id from 220 pkmn
    pid = randrange(1,40)
    while pid not in banned_list:
        cur.execute('SELECT name FROM pokemon WHERE id = {0};'.format(pid))
        name = cur.fetchone()[0]
        lvl = randrange(1,30)
        hp = int(100+lvl*2)
        item = 0
        spawn_pkmon_to_db(pid,lvl,hp,item)
        return name, lvl, hp
    spawn_random_pkmn()

#ADD spawned pokemon to db with a the value of caught as 0 for no.
def spawn_pkmon_to_db(pid,lvl,maxhp,item):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    print(pid)
    cur.execute('INSERT INTO spawnedpokemon (pid,lvl,maxhp,item,caught,hp) VALUES ({0},{1},{2},{3},{4},{5});'.format(pid,lvl,maxhp,item,'0',maxhp))
    cur.execute('COMMIT;')

#CHECK the db for the last spawned pokemon
def chk_lastspawned():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM spawnedpokemon ORDER BY ID DESC LIMIT 1')
    return cur.fetchone()

#CHANGE last spawned pokemon to caught 1 so no one can catch the same pokemon
def lastspawned_got():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('UPDATE spawnedpokemon SET caught = 1 WHERE caught = 0')
    cur.execute('COMMIT;')
    return cur.fetchone()

def attack_lastspawned():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM spawnedpokemon ORDER BY ID DESC LIMIT 1')
    pokemon = cur.fetchone()
    cur.execute('UPDATE spawnedpokemon SET hp = {0} WHERE id = {1}'.format(pokemon[6]-20, pokemon[0] ))
    cur.execute('COMMIT;')
    return cur.fetchone()

def lastspawned_attack_player():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM userpokemon ORDER BY ID DESC LIMIT 1')
    pokemon = cur.fetchone()
    cur.execute('UPDATE spawnedpokemon SET hp = {0} WHERE id = {1}'.format(pokemon[6]-20, pokemon[0] ))
    cur.execute('COMMIT;')
    return cur.fetchone()

def lastspawned_hp():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM spawnedpokemon ORDER BY ID DESC LIMIT 1')
    pokemon = cur.fetchone()
    cur.execute('UPDATE spawnedpokemon SET hp = {0} WHERE id = {1}'.format(pokemon[6]-20, pokemon[0] ))
    cur.execute('COMMIT;')
    return cur.fetchone()



#CATCH the pokemon
def catch_pokemon(did,pid,lvl,item):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    print(did)
    cur.execute('INSERT INTO userpokemon (did, pid, lvl, item) VALUES ({0},{1},{2},{3});'.format(did,pid,lvl,item))
    cur.execute('COMMIT;')

#GET list of all pokemon owned by user by discord id
def get_user_pokemon(did):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM userpokemon WHERE did = {0}'.format(did))
    return cur.fetchall()

#GET name of pokemon by their ID
def get_pokemon_name(pid):
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT name FROM pokemon WHERE id = {0}'.format(pid))
    return cur.fetchall()

#GIVE all characters a normal attack that does 20 damage
def give_normal_skill():
    con = sqlite3.connect('pokemon.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM pokemon')
    for pokemon in cur.fetchall():
        print(pokemon[0])
    cur.execute('INSERT INTO skills (pid,sname,damage) VALUES ({0},"attack",20)'.format(pokemon[0]))
    cur.execute('COMMIT;')




'''
create_tables()
pokemon_2_db()
check_pkmn_db()
give_normal_skill()
#get_user_pokemon(239357844573388800)
'''
