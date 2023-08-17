# Budget Manager

Useful commands:
* Create a new alembic migration. Run in backend folder.  
  `PYTHONPATH=. poetry run dotenv -f .env run alembic revision -m "initial migration" --autogenerate`
* Run migration in alembic:  
  `PYTHONPATH=. poetry run dotenv -f .env run alembic upgrade head`
* Run uvicorn on dev:  
  `poetry run dotenv -f .env run uvicorn app.main:app --reload`

## FE Pages:
* ~~Home/Dashboard~~
* Expenses
  * Add expenses
    * ~~Non recurring expenses~~
    * **Recurring expenses**
  * Expense table based on filters
* Category
  * Create category
  * Edit category
* Budgets
  * View all budgets
  * Create budget
  * Edit budget
  * Delete/archive budget

## TODO:
* Add savings as a feature, saving goals to keep track of and adding money to savings.