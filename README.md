Create venv and install all dependencies:
python -m venv venv
pip install -r requirements.txt

To start DB enter:
sudo -u postgres ./init_db.sh.

To run the server enter:
uvicorn app.main:app --reload

Then open
http://127.0.0.1:8000

To fill base DB enter:
python populate.py

To try out queries, regex and pagination read requests.txt

To run migrations enter:
alembic upgrade head

To fill extra JSON field (only after all migrations) enter:
python fill_JSON_field.py