from app import app
from mysql_db.seed import seed_testing
from config import config

if __name__ == "__main__":

    if config.MODE == "aa":
        seed_testing()

    app.run()
