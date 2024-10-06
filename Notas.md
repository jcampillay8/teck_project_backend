rm -rf env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete


pip install django --upgrade


rm db.sqlite3

python manage.py makemigrations
python manage.py migrate
