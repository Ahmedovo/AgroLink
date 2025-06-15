# Utiliser une image Python officielle comme base
FROM python:3.12-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du projet dans le conteneur
COPY . .

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Exécuter les migrations et lancer le serveur après avoir attendu la base de données
CMD ["sh", "-c", "wait-for-it db:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]