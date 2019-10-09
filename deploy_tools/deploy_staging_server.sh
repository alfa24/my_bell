SERVER=62.109.12.113
cd deploy_tools
fab deploy:host=root@$SERVER
cd ..
#STAGING_SERVER=$SERVER ../venv/bin/python manage.py test functional_tests