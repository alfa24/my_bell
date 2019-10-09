SERVER=62.109.12.113
STAGING_SERVER=$SERVER:83
cd deploy_tools
fab deploy:host=root@$SERVER
cd ..
STAGING_SERVER=$STAGING_SERVER venv/bin/python manage.py test functional_tests