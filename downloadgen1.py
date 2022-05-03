import re
import os
import requests

def dl_nm_pkmon():
    os.chdir('./pokemon/pokemon-normal')
    r = requests.get('https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/')
    text = r.text
    ree = re.findall(r'.*src="(.*/normal-sprite.*\.gif)".*',text)
    for pk in ree:
        pkmname = re.findall(r'.*normal-sprite/(.*)\.gif', pk)
        print(pk)
        print(pkmname)
        r2 = requests.get(pk)
        open('{0}.gif'.format(pkmname[0]), 'wb').write(r2.content)


def dl_nm_back_pkmon():
    os.chdir('./pokemon/pokemon-normal-back')
    r = requests.get('https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/')
    text = r.text
    ree = re.findall(r'.*src="(.*sprites-models/normal-back.*\.gif)".*',text)
    for pk in ree:
        pkmname = re.findall(r'.*sprites-models/normal-back/(.*)\.gif', pk)
        print(pk)
        print(pkmname)
        r2 = requests.get(pk)

        open('{0}.gif'.format(pkmname[0]), 'wb').write(r2.content)


def dl_shny_pkmon():
    os.chdir('./pokemon/pokemon-shny')
    r = requests.get('https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/')
    text = r.text
    ree = re.findall(r'.*src="(.*shiny-sprite.*\.gif)".*',text)
    for pk in ree:
        pkmname = re.findall(r'.*shiny-sprite/(.*)\.gif', pk)
        print(pk)
        print(pkmname)
        r2 = requests.get(pk)

        open('{0}.gif'.format(pkmname[0]), 'wb').write(r2.content)

def dl_shny_back_pkmon():
    os.chdir('./pokemon/pokemon-shny-back')
    r = requests.get('https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/')
    text = r.text
    ree = re.findall(r'.*src="(.*sprites-models/shiny-back/.*\.gif)".*',text)
    for pk in ree:
        pkmname = re.findall(r'.*sprites-models/shiny-back/(.*)\.gif', pk)
        print(pk)
        print(pkmname)
        r2 = requests.get(pk)

        open('{0}.gif'.format(pkmname[0]), 'wb').write(r2.content)

dl_nm_back_pkmon()
