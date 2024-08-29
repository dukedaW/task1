from app import db, app
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, jsonify, Blueprint, redirect, url_for, request
from factory import Factory


class Sector(db.Model):
    __tablename__ = 'sectors'

    sector_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    factory = db.Column(db.Integer, db.ForeignKey(Factory.factory_id), nullable=False)

    def __init__(self, name, factory):
        self.name = name
        self.factory = factory

    def __repr__(self):
        return f'{self.sector_id}, {self.name}'


class SectorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    factory = IntegerField('factory', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/sectors_page', methods=['GET', 'POST'])
def sectors_page():
    form = SectorForm()
    if form.validate_on_submit():
        sector = Sector(name=form.name.data, factory=form.factory.data)
        db.session.add(sector)
        db.session.commit()
        return redirect(url_for('sectors_page'))
    sectors = Sector.query.all()
    return render_template('sectors_page.html', form=form, sectors=sectors)


@app.route('/delete_sector/<int:sector_id>', methods=['POST'])
def delete_sector(sector_id):
    factory = Sector.query.get_or_404(sector_id)
    db.session.delete(factory)
    db.session.commit()
    return redirect(url_for('sectors_page'))
