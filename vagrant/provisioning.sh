#!/usr/bin/env bash

packages="
curl
git
postgresql-9.4
libpq-dev
python3
python3-dev
vim
zsh
"

# DB operations courtesy of Davis Ford: https://gist.github.com/davisford/8000332

echo "-------------------- updating package lists"
sudo apt-get update
echo "-------------------- installing packages"
sudo apt-get install -y ${packages}
echo "-------------------- installing pip"
sudo wget --quiet https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo rm get-pip.py
echo "-------------------- installing Python dependencies"
sudo pip3 install -U -r pwp/server/requirements.txt
echo "-------------------- creating postgres vagrant role with password vagrant"
sudo su postgres -c "psql -c \"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant'\" "
sudo su postgres -c "createdb vagrant"
sudo su postgres -c "createdb pwp"
echo "-------------------- creating test database"
cd pwp; sudo su vagrant -c "python3 -m server.init_db"; cd -
echo "-------------------- upgrading packages to latest"
sudo apt-get upgrade -y
echo "-------------------- installing Oh-My-Zsh"
sudo su vagrant -c 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"'
sudo chsh -s /usr/bin/zsh vagrant
