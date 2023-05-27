from app import app
from utils.db import db
from flask_cors import CORS

with app.app_context():
    db.create_all()

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
