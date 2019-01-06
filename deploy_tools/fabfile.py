import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/ciphernix/python-tdd-book.git'

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    currrent_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in currrent_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}') 


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')



def _update_and_reload_gunicorn():
    run('cat deploy_tools/gunicorn-systemd.template.service | '\
        f'sed "s/DOMAIN/{env.host}/g" | '\
        f'sed "s/USERNAME/{env.user}/g"  |'\
        f'sudo tee /etc/systemd/system/gunicorn-{env.host}.service'
    )
    run('sudo systemctl daemon-reload')
    run(f'sudo systemctl restart gunicorn-{env.host}.service')


def _update_and_reload_nginx():
    run('cat deploy_tools/nginx.template.conf |'\
        f'sed "s/DOMAIN/{env.host}/g" |'\
        f' sed "s/USERNAME/{env.user}/g" |'\
        f'sudo tee /etc/nginx/sites-available/{env.host}'
    )
    run(f'sudo ln -sf /etc/nginx/sites-available/{env.host} '\
        f'/etc/nginx/sites-enabled/{env.host}'
    )
    run(f'sudo systemctl reload nginx')


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _update_and_reload_nginx()
        _update_and_reload_gunicorn()
