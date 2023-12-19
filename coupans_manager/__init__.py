from flask import Flask

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "575a581e34d929fc5215c09a934d9a32"  # For dev it can be hardcoded # for prod get it from env variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


from coupans_manager import routes