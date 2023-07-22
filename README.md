# Budget Manager

Useful commands:
* Create a new alembic migration. Run in backend folder.  
  `PYTHONPATH=. poetry run dotenv -f .env run alembic revision -m "initial migration" --autogenerate`
* Run migration in alembic:  
  `PYTHONPATH=. poetry run dotenv -f .env run alembic upgrade head`
* Run uvicorn on dev:  
  `poetry run dotenv -f .env run uvicorn app.main:app --reload`


## TODO:
* Add savings as a feature, saving goals to keep track of and adding money to savings.