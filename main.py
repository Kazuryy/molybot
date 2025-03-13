import discord
import datetime
import json
import asyncio
import random
import os
from discord import app_commands
from discord.ui import Modal, TextInput
from discord.ext import commands
from notionportal import NotionAPI, DATABASE_TOKEN, list_origine, nombre_prod_reg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_TOKEN = os.getenv("DATABASE_ID")

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

# Event: on_ready
@bot.event
async def on_ready():
    print('Molybot is Up and Ready!!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

def has_allowed_role():
    def predicate(interaction: discord.Interaction):
        allowed_roles = [1230258831595016234, 833042720968015972]  # Remplace avec tes ID de rôles
        return any(role.id in allowed_roles for role in interaction.user.roles)
    return app_commands.check(predicate)

##################################
##            Général           ##
##################################

# Help command
@bot.tree.command(name="help", description="Répertoire des commandes")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        colour=0x0ab6a1,
        title="Liste des commandes",
        description="Voici les commandes utilisables"
    )
    embed.add_field(name='/say', value='Say something you want to say', inline=False)
    embed.add_field(name='/hello', value='Say hello !', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Check command
@bot.tree.command(name="check", description="Vérifier si les commandes slash fonctionnent correctement")
async def check(interaction: discord.Interaction):
    await interaction.response.defer()
    msg = await interaction.followup.send(f"Hey {interaction.user.mention} ! Les interactions fonctionnent bien !")
    await asyncio.sleep(15)
    await msg.delete()

# Say command
@bot.tree.command(name="say", description="Je dis ce que tu veux dire")
@app_commands.describe(thing_to_say="Je dois dire quoi ?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said `{thing_to_say}`")

# Sondage Modal
class SondageModal(Modal, title='Formulaire de Sondage'):
    nom = TextInput(
        label='Votre nom',
        style=discord.TextStyle.short,
        placeholder='Entrez votre nom',
        max_length=50,
        required=True
    )
    commentaire = TextInput(
        label='Votre commentaire',
        style=discord.TextStyle.long,
        placeholder='Laissez un commentaire (optionnel)',
        max_length=300,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Merci {self.nom.value} ! Votre commentaire a été reçu.", 
            ephemeral=True
        )

# Formulaire command
@bot.tree.command(name="formulaire", description="Ouvre un formulaire de sondage")
async def formulaire(interaction: discord.Interaction):
    await interaction.response.send_modal(SondageModal())

################################################
##            Commandes Utilitaires           ##
################################################

# Clear Messages command
@bot.tree.command(name="sup", description="Supprimer n messages")
@has_allowed_role()
@app_commands.describe(message="Nombre de message à supprimer")
async def sup(interaction: discord.Interaction, message: int):
    await interaction.response.defer(ephemeral=True)
    
    def is_not_pinned(msg):
        return not msg.pinned

    deleted = await interaction.channel.purge(limit=message, check=is_not_pinned)
    await interaction.followup.send(f"{len(deleted)} message(s) ont été supprimé(s)", ephemeral=True)

# Spam command
@bot.tree.command(name="spam", description="Envoie n fois le message qui m'est donné")
@has_allowed_role()
@app_commands.describe(message="Je vais dire quoi ?", number="Combien de fois je dois le dire ?", time="Supprimer le message après combien de temps")
async def spam(interaction: discord.Interaction, message: str, number: int, time: int = 30):
    await interaction.response.defer(ephemeral=True)
    
    async def send_and_delete(message: str, delay: int):
        msg = await interaction.followup.send(message)
        await asyncio.sleep(delay)
        await msg.delete()

    tasks = [send_and_delete(message, time) for _ in range(number)]
    await asyncio.gather(*tasks)
    await interaction.followup.send(f"{number} message(s) ont été envoyés et seront supprimés après {time} secondes.", ephemeral=True)

##########################################
##         Commandes Notion bot         ##
##########################################

# Commande command
@bot.tree.command(name="commande", description="Commander un produit")
@app_commands.describe(product="Quel produit voulez-vous commander ?", quantity="Combien de produit voulez-vous commander ?")
async def commande(interaction: discord.Interaction, product: str, quantity: int):
    notion_api = NotionAPI()
    name = product
    origine = list_origine[random.randint(0, 4)]  # Origine aléatoire
    nombre_produits = quantity
    estimation_prix = 1000
    addrow = notion_api.add_row(DATABASE_TOKEN, name, origine, nombre_produits, estimation_prix)
    print(addrow)
    await interaction.response.send_message(f"Votre commande de {quantity} {product} a été prise en compte")

##########################################
##         Commandes Modération         ##
##########################################

# Load user counts from a JSON file
def load_user_counts():
    try:
        with open('user_counts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user counts to a JSON file
def save_user_counts(user_counts):
    with open('user_counts.json', 'w') as file:
        json.dump(user_counts, file, indent=4)

# Sanction command
@bot.tree.command(name="sanction", description="Sanctionner un utilisateur pour une raison précise.")
@app_commands.describe(membre="Qui doit être sanctionné ?", temps="Combien de temps mute cette personne ?", raison="Quelle est la raison de cette sanction ?")
async def sanction(interaction: discord.Interaction, membre: discord.Member, temps: int, raison: str):
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
        await membre.edit(timed_out_until=discord.utils.utcnow() + newtime, reason=raison)
        await interaction.response.send_message(f"{membre.mention} a été **mute** pour la {mute_count} fois pour : {raison}.")

# Unsanction command
@bot.tree.command(name="unsanction", description="Retirer la sanction d'un utilisateur")
async def unsanction(interaction: discord.Interaction, member: discord.Member):
    user_counts = load_user_counts()
    mute_count = user_counts.get(str(member.id), 0)
    mute_count -= 1
    user_counts[str(member.id)] = mute_count
    save_user_counts(user_counts)
    await member.timeout(None)
    await interaction.response.send_message(f"{member.name} est unmute.")

# Run the bot with your token
bot.run(TOKEN)