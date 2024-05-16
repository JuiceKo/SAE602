echo "Arrêt de tous les services Swarm..."
sudo docker service rm $(sudo docker service ls -q)

# Quitter le Swarm
echo "Quitter le Swarm..."
sudo docker swarm leave --force

# Optionnel : Arrêter Docker
echo "Arrêter Docker..."
sudo systemctl stop docker
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)

echo "Docker Swarm est arrêté et Docker est arrêté."
