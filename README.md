# ships
#for activate without docker
git clone https://github.com/hens2013/ships.git

cd ships

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

navigate to the given url in the log