import discord
from discord.ext.commands import Bot
import os
import re
from random import randrange
import pkmndb


# spawn system triggers on messages, so do not
#  spawn if these commands were used

nscl = ['$pcatch', '$pgl', '$preg', '$attack 1']
bot = Bot(command_prefix='$')

#insert discord token here

TOKEN = '< discord-token >'

# on connect print this message

@bot.event
async def on_ready():
	print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
# register a discord user by discord id number
#  if they dont exist already!

        if message.content == '$preg':
                if pkmndb.chk_user_exist(message.author.id) == False:
                        print(message.author.id)
                        pkmndb.register_user(message.author.id)
                        await message.channel.send('you are now registered')
                else:
                        print('DisID alrdy exists')
                        print(message.author.id)
                        await message.channel.send('you are alrdy registered')

        #SPAWN. listen to all messages and have a chance 
        # to spawn a random character

        if len(message.content) >=2 and message.content not in nscl and message.author.id != 817800623524413460:              
                #10% chance to spawn a character
                if randrange(1,10) >= 1:
                        spawn = pkmndb.spawn_random_pkmn()
                        item_emojii = discord.utils.get(bot.emojis, name='pokeball')
                        embed = discord.Embed(title="A wild {0} appeared".format(spawn[0]), description="capture the character before someone else does.",color=int(0xFF0000))
                        embed.set_image(url='http://74.88.95.5/static/fighters/{0}.gif'.format(spawn[0]))
                        embed.add_field(name="Lvl:", value="{0}".format(spawn[1]))
                        embed.add_field(name="HP:", value="{0}/{1}".format(spawn[2], spawn[2]))
                        embed.add_field(name="Skills:", value="""Attack\n None\n None\n None""")
                        embed.add_field(name="Stats:", value="""Attack: 20\n Dodge: 20%\n Speed: 100\n Element: Dark""")
                        embed.add_field(name="Held Item:", value="{0}".format(item_emojii))
                        channel = bot.get_channel(898976100342980698)
                        await channel.send(embed=embed)
                else:pass

        #CATCH: capture the last pokemon that spawn if
        #  it hasn't been caught already

        if message.content == '$pcatch':
                did = message.author.id
                user = message.author.name
                if pkmndb.chk_user_exist(did) == True:
                        p = pkmndb.chk_lastspawned()
                        #if spawned pokemon isnt caught continue
                        
                        if p[5] == 0:
                                randnum = randrange(1,10)
                                #if pokemon hp is 50% or less increade chances
                                #  of catching by 10%

                                if p[3]/2 > p[6]:
                                        randnum + 1
                                        # 20% chance to catch pokemon + 10 if hp 50% 
                                        # or less if success catch else pass.

                                        if randnum >= 8:
                                                pkmndb.catch_pokemon(did,p[1],p[2],p[4])
                                                pkmndb.lastspawned_got()
                                                channel = bot.get_channel(819661217706016768)
                                                await channel.send('Congratz,{0} has caught a {1}'.format(user,pkmndb.get_pokemon_name(p[1])[0][0]))
                                        else:
                                                channel = bot.get_channel(819661217706016768)
                                                await channel.send('{0} Failed catching {1}'.format(user,pkmndb.get_pokemon_name(p[1])[0][0]))
                        else:
                                await message.channel.send('pokemon has alrdy been caught')
                else:
                        await message.channel.send('you are not registered')

        # Get the list of pokemon you own if
        # you are registered

        if message.content == '$pgl':
                did = message.author.id
                user = message.author.name
                if pkmndb.chk_user_exist(did) == True:
                        pkmnlist = []
                        for pkmn in pkmndb.get_user_pokemon(did):
                                pkmnlist.append(pkmn)
                        print(pkmnlist)
                        for p in pkmnlist:
                                name = pkmndb.get_pokemon_name(p[2])    
                                item_emojii = discord.utils.get(bot.emojis, name='pokeball')
                                embed = discord.Embed(title="{0}\nEffect:".format(name[0][0]), description="No effect",color=int(0xFF0000))
                                embed.set_image(url='http://74.88.95.5/static/fighters/{0}.gif'.format(name[0][0]))
                                embed.add_field(name="Lvl:", value="{0}".format(p[3]))
                                embed.add_field(name="HP:", value="{0}/{0}".format(100+2*int((p[3]))))
                                embed.add_field(name="Held Item:", value="{0}".format(item_emojii))
                                embed.add_field(name="Skills:", value="""Attack\n None\n None\n None""")
                                embed.add_field(name="Stats:", value="""Attack: 20\n Dodge: 20%\n Speed: 100\n Element: Dark""")
                                
                                await message.channel.send(embed=embed)
                else:
                        await message.channel.send('you are not registered')
        # attack last spawned pokemon with 1st attack

        if message.content == '$attack 1':
                did = message.author.id
                user = message.author.name
                if pkmndb.chk_user_exist(did) == True:
                        p = pkmndb.chk_lastspawned()
                        #if last spawned is uncaught or not dead do damage else pass

                        if p[5] == 0:
                                print('attack test')
                                channel = bot.get_channel(819630234277249034)
                                pkmndb.attack_lastspawned()
                                hpnow = pkmndb.chk_lastspawned()[6]
                                await channel.send('{0} attacked {1}, HP: {2}/{3}'.format(user,pkmndb.get_pokemon_name(p[1])[0][0],hpnow,p[3]))
                                #if hp is 0 or less show message
                                
                                if hpnow <=0:
                                        await channel.send('{0} killed {1} +999 exp'.format(user,pkmndb.get_pokemon_name(p[1])[0][0]))
                                        pkmndb.lastspawned_got()

bot.run(TOKEN)
