web: gunicorn main.wsgi 
release: python manage.py makemigrations --noinput 
release: python manage.py collectatic --noinput
release: python manage.py migrate --noinput
