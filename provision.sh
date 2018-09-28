#!/bin/bash

# Install system packages
apt update
apt install -y python3 python3-pip postgresql redis git nginx

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable edge"

apt install -y docker-ce

# Allow local connections to postgres user without password
sed -i 's#local   all             postgres                                peer#local   all             postgres                                trust#g' /etc/postgresql/10/main/pg_hba.conf
sed -i 's#host    all             all             127.0.0.1/32            md5#host    all             all             127.0.0.1/32            trust#g' /etc/postgresql/10/main/pg_hba.conf
sed -i 's#host    all             all             ::1/128                 md5#host    all             all             ::1/128                 trust#g' /etc/postgresql/10/main/pg_hba.conf

systemctl reload postgresql@10-main.service
systemctl start redis-server

psql -U postgres -c 'CREATE DATABASE cartoku;'

# Setup the app
cd /vagrant/cartokuapi || exit 1

sed -i 's#ALLOWED_HOSTS = \[\]#ALLOWED_HOSTS = \["*"\]#g' cartokuapi/settings.py

pip3 install -r requirements.txt
python3 manage.py migrate

# Setup git server
adduser git --home /srv/git --gecos "" --disabled-password -q
sudo -u git mkdir /srv/git/.ssh && sudo -u git cp /vagrant/authorized_keys /srv/git/.ssh
usermod -aG docker git

# Nginx
chown git:git /etc/nginx/sites-available/
echo "git ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/git

echo -e "\n\n\n\nRun the server now:\nvagrant ssh -c \"cd /vagrant/cartokuapi/; sudo -u git python3 manage.py runserver 0.0.0.0:8000\""
echo -e "\n\n\n\nRun the queues now:\nvagrant ssh -c \"cd /vagrant/cartokuapi/; sudo -u git python3 -m celery -A api worker\""
