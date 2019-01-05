Provisioning a new sites
========================

## Required packages:


* nginx
* Python 3.6
* virtualenv + pip
* Git

e.g., on Ubuntu:

        sudo add-apt-repository ppa:deadsnake/ppa
        sudo apt update
        sudo apt install nginx git python36 python3.6-venv


## Nginx Virtual Host Configuration

* see nginx.template.conf
* replace DOMAIN with, e.g. staging.my-domain.com


## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g. staging.my-domain.com

## Folder structure:

Assume we have a user at /home/username


    /home/username
    |___sites
        |--- DOMAIN1
        |     |____ .env
        |     |____ db.sqlite3
        |     |____ manage.py etc
        |     |____ static
        |     |____ virtualenv
        |
        |___ DOMAIN2
              |_____ .env
              |_____ db.sqlite3
              |_____ etc

