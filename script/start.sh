sudo rm -rf /var/lib/cassandra/data/system/*
sudo /lib/systemd/systemd-sysv-install enable cassandra
sudo systemctl start cassandra
