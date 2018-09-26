sudo apt-get install git
git add git
mkdir /srv/git/myapp.git
chown -R /srv/git
cd /srv/git/myapp.git && git init --bare
