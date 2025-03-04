# Molybot - Bot Discord Dockerisé

Molybot est un bot Discord développé en Python, conçu pour enrichir l'expérience utilisateur avec des commandes interactives, une gestion avancée et une intégration avec Notion. Ce projet est conçu pour être déployé facilement via Docker, que ce soit sur un serveur TrueNAS, un NAS Synology ou toute autre infrastructure compatible Docker.

## Fonctionnalités

- 📌 Commandes interactives (/help, /say, /check, etc.)
- 📝 Intégration avec Notion pour gérer les commandes
- 🗑️ Commandes de modération (/sup, /sanction, /unsanction)
- 📊 Formulaire interactif pour collecter des retours
- 🔄 Déploiement simplifié avec Docker Compose

## Déploiement avec Docker Compose

### 1. Prérequis

- Un serveur avec **Docker** et **Docker Compose** installé
- Un fichier `.env` contenant votre **DISCORD_TOKEN** et **DATABASE_ID**
- Un NAS **TrueNAS** ou **Synology** (optionnel, pour auto-hébergement)

### 2. Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/Kazuryy/molybot
cd molybot
```

2. **Créer un fichier `.env`**
```ini
DISCORD_TOKEN=your_discord_token
DATABASE_ID=your_notion_database_id
```

3. **Configurer `docker-compose.yml`**
```yaml
version: '3.8'
services:
  molybot:
    image: finnick5/molybot:latest
    container_name: molybot
    restart: always
    env_file: .env
    volumes:
      - ./data:/app/data
```

4. **Lancer le bot**
```bash
docker-compose up -d
```

## Déploiement sur TrueNAS

1. Installer une **application custom** sur TrueNAS SCALE
2. Sélectionner l'image `finnick5/molybot`
3. Ajouter les variables d'environnement (`DISCORD_TOKEN`, `DATABASE_ID`)
4. Lancer l'application 🚀

## Déploiement sur Synology

1. Ouvrir **Container Manager** et importer l'image Docker
2. Ajouter les variables d’environnement et les volumes
3. Lancer et tester le bot sur Discord ✅

## Licence

Ce projet est sous licence MIT.

