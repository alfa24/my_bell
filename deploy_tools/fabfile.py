import os

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

from fabric.operations import put

REPO_URL = 'https://github.com/alfa24/my_bell.git'
HOST = env.host
USER = env.user
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SITENAME = "my_bell"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def deploy():
    """развернуть"""

    site_folder = f'/home/{SITENAME}'
    source_folder = site_folder
    virtualenv_folder = site_folder + '/venv'

    _get_latest_source(source_folder)
    _create_directory_structure_if_necessary(site_folder)
    _update_settings(source_folder, SITENAME)
    _update_virtualenv(source_folder, virtualenv_folder)
    _update_static_files(source_folder, virtualenv_folder)
    _update_database(source_folder, virtualenv_folder)

    # _configure_gunicorn_service(source_folder)
    _configure_supervisor_service(source_folder, virtualenv_folder)
    _configure_nginx(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """создать структуру каталога, если нужно"""

    for subfolder in ('venv', ):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """получить самый свежий исходный код"""
    run(f'mkdir -p {source_folder}')

    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch && git reset --hard origin/master')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    """обновить настройки"""

    settings_path = f'{source_folder}/{SITENAME}/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        # f'ALLOWED_HOSTS = ["{site_name}"]'
        f'ALLOWED_HOSTS = ["*"]'
        )
    secret_key_file = f'{source_folder}/{SITENAME}/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder, virtualenv_folder):
    """обновить виртуальную среду"""

    if not exists(virtualenv_folder + '/bin/pip'):
        run('apt install python3-venv')
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder, virtualenv_folder):
    """обновить статические файлы"""
    run(f'cd {source_folder} && {virtualenv_folder}/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder, virtualenv_folder):
    """обновить базу данных"""
    run(f'cd {source_folder} && {virtualenv_folder}/bin/python manage.py migrate --noinput')


def _configure_gunicorn_service(source_folder):
    """конфигурируем gunicorn как сервис"""

    gunicorn_conf_template = f'{source_folder}/deploy_tools/gunicorn-systemd.template.service'
    gunicorn_conf_service = f'/etc/systemd/system/{SITENAME}.service'
    run(f'sudo cp {gunicorn_conf_template} {gunicorn_conf_service}')

    sed(gunicorn_conf_service, "SITENAME", SITENAME, use_sudo=True)
    sed(gunicorn_conf_service, "USERNAME", env.user, use_sudo=True)
    # sed(gunicorn_conf_service, "EMAIL_PASSWORD_YANDEX", EMAIL_PASSWORD, use_sudo=True)

    run(f'sudo systemctl daemon-reload && '
        f'sudo systemctl enable {SITENAME} && '
        f'sudo systemctl stop {SITENAME} && '
        f'sudo systemctl start {SITENAME}')


def _configure_supervisor_service(source_folder, venv_folder):
    """конфигурируем supervisor"""

    supervisor_conf_template = f'{source_folder}/deploy_tools/supervisor.template.conf'
    supervisor_conf_service = f'/etc/supervisor/conf.d/{SITENAME}.conf'
    run(f'sudo cp {supervisor_conf_template} {supervisor_conf_service}')

    sed(supervisor_conf_service, "SITENAME", SITENAME, use_sudo=True)
    sed(supervisor_conf_service, "VENV_FOLDER", venv_folder, use_sudo=True)
    sed(supervisor_conf_service, "SOURCE_FOLDER", source_folder, use_sudo=True)

    run(f'sudo supervisorctl update && '
        f'sudo supervisorctl reread && '
        f'sudo supervisorctl restart {SITENAME}:*')


def _configure_nginx(source_folder):
    """конфигурирование nginx"""

    nginx_conf_template = f'{source_folder}/deploy_tools/nginx.template.conf'
    nginx_conf = f'/etc/nginx/sites-available/{SITENAME}'
    nginx_conf_link = f'/etc/nginx/sites-enabled/{SITENAME}'
    if exists(nginx_conf_link):
        run(f'sudo rm {nginx_conf_link}')

    run(f'sudo cp {nginx_conf_template} {nginx_conf}')
    run(f'sudo ln -s {nginx_conf} {nginx_conf_link}')

    sed(nginx_conf, "SITENAME", SITENAME, use_sudo=True)
    sed(nginx_conf, "USERNAME", env.user, use_sudo=True)

    run(f'sudo systemctl reload nginx')
