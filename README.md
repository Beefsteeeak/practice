# practice

To run in a production mode run:
./manage.py runserver --settings=practice.settings.production

Database population:
1) Use management command: ./manage.py load_data
2) Fixture: ./manage.py loaddata db.json

To run celery worker run:
celery -A practice worker -l INFO