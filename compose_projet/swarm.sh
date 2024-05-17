echo "Mise à jour du système..."
sudo apt-get update && sudo apt-get upgrade -y

# Installer les dépendances nécessaires
echo "Installation des dépendances..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Ajouter la clé GPG de Docker
echo "Ajout de la clé GPG de Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Ajouter le dépôt Docker
echo "Ajout du dépôt Docker..."
echo | sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Mettre à jour les informations sur les paquets
echo "Mise à jour des informations sur les paquets..."
sudo apt-get update

# Installer Docker
echo "Installation de Docker..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Vérifier que Docker est installé
echo "Vérification de l'installation de Docker..."
sudo docker --version

# Activer et démarrer Docker
echo "Activation et démarrage de Docker..."
sudo systemctl enable docker
sudo systemctl start docker

# Initialiser Docker Swarm
echo "Initialisation de Docker Swarm..."
sudo docker swarm init

# Afficher le statut du cluster Swarm
echo "Statut du cluster Swarm :"
sudo docker info | grep Swarm


docker stack deploy -c docker-compose.yml test
