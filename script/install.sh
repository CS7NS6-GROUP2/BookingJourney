sudo apt update
sudo apt install openjdk-8-jdk -y
sudo apt install apt-transport-https -y
sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 311x main" > /etc/apt/sources.list.d/cassandra.list'
wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo apt update
sudo apt install ntp -y
sudo apt install cassandra -y
sudo systemctl stop cassandra
