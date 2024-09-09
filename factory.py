from app import db, app
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, jsonify, Blueprint, redirect, url_for, request


class Factory(db.Model):
    __tablename__ = 'factory'

    factory_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'({self.factory_id}, {self.name})'


class FactoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/factories_page', methods=['GET', 'POST'])
def factories_page():
    form = FactoryForm()
    if form.validate_on_submit():
        factory = Factory(name=form.name.data)
        db.session.add(factory)
        db.session.commit()
        return redirect(url_for('factories_page'))
    factories = Factory.query.all()
    return render_template('factories_page.html', form=form, factories=factories)


@app.route('/delete_factory/<int:factory_id>', methods=['POST'])
def delete_factory(factory_id):
    factory = Factory.query.get_or_404(factory_id)
    db.session.delete(factory)
    db.session.commit()
    return redirect(url_for('factories_page'))


