#!/bin/bash

#Let's store the current user for permission settings later
ME=$(whoami)
sudo apt-get update

##########################
# PART 1: API Setup
##########################

#Check to see if dev.db exists
if [ ! -f dev.db ]; then
  #If it does not exist, let's create it
  touch dev.db
fi

#Setup python virtual environment
sudo apt-get install python-virtualenv python-dev build-essential
python virtualenv.py flask
flask/bin/pip install setuptools --no-use-wheel --upgrade

#Install python dependencies from require.txt
filename="require.txt"
while read -r line
do
  echo "Installing python module $line"
  flask/bin/pip install $line
  #Check to make sure each dependency works properly...
  if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install python module $line -- EXITING"
    exit 1
  fi
done < $filename

source flask/bin/activate
#Setup the database
python run.py setup

##########################
# Part2: UWSGI setup
##########################
sudo apt-get install uwsgi
#The unix socket will be located here
mkdir sock
#Logs (for uwsgi) will be stored here
mkdir -p logs/uwsgi
#Apply some sed magic to include the base directory for uwsgi configs
sed -i.bak "s@sed_magic_1@$PWD@" app_uwsgi.ini

#And now we initialize our uwsgi configurations to start the app
uwsgi --ini app_uwsgi.ini


##########################
# PART 3: NGINX Setup
##########################

#Let's install this as a deb package
sudo apt-get install nginx

#Apply some sed magic to include our static directory
sed -i.bak "s@sed_magic_1@$PWD/static@" app_nginx.conf

#Apply some sed magic to include our sock directory
sed -i.bak "s@sed_magic_2@$PWD/sock"

#Remove the default nginx configuration!
sudo rm /etc/nginx/sites-enabled/default

#Add symlink to nginx's config file directory
sudo ln -s $PWD/app_nginx.conf /etc/nginx/conf.d/

#Restart nginx!
sudo service nginx restart

echo "DONE";
