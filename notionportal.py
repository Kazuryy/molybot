import os
import sys
import random
from notion_client import Client
from dotenv import load_dotenv

NOTION_DATABASE_NAME = "Historique Delivery"

load_dotenv()
NOTI_TOKEN = os.getenv("NOTI_TOKEN")
DATABASE_TOKEN = os.getenv("DATABASE_TOKEN")

# Initialise le client avec ta clé d'API Notion
notion = Client(auth=NOTI_TOKEN)

print(f"Searching database '{NOTION_DATABASE_NAME}' ...", end="", flush=True)

list_origine = ["Europe", "Asie", "Amérique", "Océanie", "Afrique"]

nombre_prod_reg = {
    "Europe": [30500, 200000],
    "Asie": [30000, 600000],
    "Afrique": [10000, 50000],
    "Océanie": [30000, 80000],
    "Amérique": [30600, 900800]
}

prix_vente = {
    "Bâtiment": [100000, 105000, 200000],
    "Transport": [100000, 140000, 200000],
    "Logistique": [130000, 200000],
    "Santé": [140000, 200000, 300000],
    "Sécurité": [12000, 20000, 44000],
    "Éducation": [15000, 20000, 30000],
    "Administration": [270000, 350000, 500000],
    "Vente": [300000, 500000, 704000],
    "Agriculture": [20000, 30000, 58000],
    "Communication": [90000, 100000, 270000],
    "Artisanat": [50000, 60000, 102000],
    "Commerce": [500000, 600000, 890000]
}

try:
    search_database = notion.search(query=NOTION_DATABASE_NAME, filter={'property': 'object', 'value': 'database'})
    if len(search_database['results']) == 0:
        print(" not found!")
        sys.exit()
    print(" found!")
except Exception as e:
    print(f"Error searching database: {e}")
    sys.exit()

class NotionAPI:
    def add_row(self, database_id, name, origine, nombre_produits, estimation_prix):
        new_page = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Origine": {
                    "select": {
                        "name": origine
                    }
                },
                "Nombre de produits": {
                    "number": nombre_produits
                },
                "Estimation du Prix": {
                    "number": estimation_prix
                }
            }
        }
        try:
            response = notion.pages.create(**new_page)
            return response
        except Exception as e:
            print(f"Error creating page: {e}")
            return None

if __name__ == "__main__":
    name = "Bot"
    origine = random.choice(list_origine)  # Origine aléatoire
    nombre_produits = random.randint(nombre_prod_reg[origine][0], nombre_prod_reg[origine][1])  # Nombre de produits aléatoire
    estimation_prix = 1000  # Valeur du prix du produit (estimation)

    notion_api = NotionAPI()
    response = notion_api.add_row(DATABASE_TOKEN, name, origine, nombre_produits, estimation_prix)
    if response:
        print("Page created successfully")
    else:
        print("Failed to create page")