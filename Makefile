manage=./manage.py
python=python3

runserver:
	$(python) $(manage) runserver 8000

collectstaic:
	$(python) $(manage) collectstatic

check:
	$(python) $(manage) check

install:
	pip install -r requirements.txt

migrate:
	$(python) $(manage) makemigrations  && $(python) $(manage) migrate

freeze:
	pip freeze > requirements.txt

shell:
	$(python) $(manage) shell_plus

reset-db:
	$(python) $(manage) reset_db
	make migrate

superuser:
	$(python) $(manage) createsuperuser

create-user:
	$(python) $(manage) user


show:
	$(python) $(manage) showmigrations

git_command=git pull origin stable

restart:
	sudo systemctl restart nginx && sudo service supervisor start 

dev:
	ssh -i tradebattle.pem ubuntu@43.204.50.66

