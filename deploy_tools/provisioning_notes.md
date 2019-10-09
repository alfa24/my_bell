Обеспечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.6
* virtualenv + pip
* Git
например, в Ubuntu:
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-venv
## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на my_bell
## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на название приложения, например "my_bell"
## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/user
* ** /home/
* **** SITENAME
* ******* virtualenv
* ******* SITENAME
* ********** SITENAME
* ********** static

