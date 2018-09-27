#!/bin/bash

# Install system packages
apt update
apt install -y python3 python3-pip postgresql redis


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

echo -e "\n\n\n\nRun the server now:\nvagrant ssh -c \"sudo python3 /vagrant/cartokuapi/manage.py runserver 0.0.0.0:80\""
echo -e "\n\n\n\nRun the queues now:\nvagrant ssh -c \"sudo python3 celery -A api worker\""
