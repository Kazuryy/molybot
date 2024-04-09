import discord
import datetime
import json
import asyncio
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
bot.remove_command("help")





@bot.event
async def on_ready():
    print('Molybot is Up and Ready!!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)










##################################
##            Général           ##
##################################


# Help
@bot.tree.command(name="help", description="Répertoire des commandes")
async def help(interaction: discord.Integration):


    embed = discord.Embed(
        colour= 0x0ab6a1,
        title= "Lites de commandes",
        description= "Voici les commandes utilisables"
    )

    embed.add_field(name='/say', value='Say something you want to say', inline=False)
    embed.add_field(name='/hello', value='Say hello !', inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)






# Test de réponse
@bot.tree.command(name="check", description="Vérifier si les commandes slash fonctionnent correctement",)
async def check(interaction: discord.Integration):
    await interaction.response.defer()
    msg = await interaction.followup.send(f"Hey {interaction.user.mention} ! Les interactions fonctionnent bien !")
    await asyncio.sleep(15)
    await msg.delete()






#Commande Say
@bot.tree.command(name="say", description="Je dis ce que tu veux dire")
@app_commands.describe(thing_to_say = "What should i say ?")
async def say(interraction: discord.Interaction, thing_to_say : str):
    await interraction.response.send_message(f"{interraction.user.name} said `{thing_to_say}`")

















################################################
##            Commandes Utilitaires           ##
################################################


#Commande Clear Messages
@bot.tree.command(name="sup", description="Supprimer n messages")
@app_commands.describe(message = "Nombre de message à supprimer")
async def sup(interaction: discord.Interaction, message : int):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=message)
    await interaction.followup.send(f"{message} ont été supprimé(s)") # ephemeral message







#Spam de messages
@bot.tree.command(name="spam", description="Envoie n fois le message qui m'est donné")
@app_commands.describe(message = "Je vais dire quoi ?", number = "Combien de fois je dois le dire ?", time = "Supprimer le message après combien de temps")
async def spam(interaction, message: str, number: int, time: int = 30):
    await interaction.response.defer()
    messages = []

    for temp in range(number):
        msg = await interaction.followup.send(f"{message}")
        messages.append(msg)

    await asyncio.sleep(time)
    for msg in messages:
        await msg.delete()












##########################################
##         Commandes Modération         ##  
##########################################


 
def load_user_counts():
    """   Load user counts from a JSON file (create the file if it doesn't exist)   """

    try:
        with open('user_counts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_counts(user_counts):
    """   Save user counts to a JSON file   """

    with open('user_counts.json', 'w') as file:
        json.dump(user_counts, file, indent=4)






#Commande de Sanction
@bot.tree.command(name="sanction", description="Sanctionner un utilisateur pour une raison précise. Fonctinnement dans rules")
@app_commands.describe(membre="Qui doit être sanctionné ?",temps="Combien de temps mute cette personne ?",raison="Quelle est la raison de cette sanction ?")
async def sanction(interaction: discord.Integration, membre: discord.Member, temps: int, raison: str):
    user_counts = load_user_counts()
    mute_count = user_counts.get(str(membre.id), 0)
    mute_count += 1
    user_counts[str(membre.id)] = mute_count
    save_user_counts(user_counts)

    if mute_count == 10:
        await membre.kick(reason="Muted 10 times")
        await interaction.response.send_message(f"{interaction.user.mention} a **kick** {membre.mention} du serveur pour : {raison}.")
    elif mute_count == 20:
        await membre.ban(reason="Kicked 2 Times")
        await interaction.response.send_message(f"{interaction.user.mention} a bannit {membre.mention} du serveur pour : {raison}.")
    else:
        newtime = datetime.timedelta(seconds=int(temps))
        await membre.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(seconds=temps), reason=raison)
        await interaction.response.send_message(f"{membre.mention} a été **mute** pour la {mute_count} fois pour : {raison}.")








#Commande remove sanction
@bot.tree.command(name="unsanction", description="Retirer la sanction d'un utilisateur")
async def unsanction(interaction: discord.Integration, member: discord.Member):
    user_counts = load_user_counts()
    mute_count = user_counts.get(str(member.id), 0)
    mute_count -= 1
    user_counts[str(member.id)] = mute_count
    save_user_counts(user_counts)
    await member.timeout(None)
    await interaction.response.send_message(f"{member.name} est unmute.")





# Run the bot with your token
bot.run(TOKEN) #MolyBot
#bot.run() #Elbot
