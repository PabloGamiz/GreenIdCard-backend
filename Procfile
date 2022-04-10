web: python GreenIdCard/GreenIdCard/manage.py runserver 0.0.0.0:8000
web: gunicorn GreenIdCard.GreenIdCard.wsgi --log-file -
heroku ps:scale web=1