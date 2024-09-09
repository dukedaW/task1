from app import app, db
from flask import render_template
import factory
import index
import sector
import equipment
import details


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', debug=True)
