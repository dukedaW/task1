from app import db, app
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired
from flask import render_template, jsonify, Blueprint, redirect, url_for, request
from factory import Factory
from sector import Sector, SectorForm


class Equipment(db.Model):
    __tablename__ = 'equipment'
    eq_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.eq_id}, {self.name}'


'''
sectors to equipments table
'''


class SecToEq(db.Model):
    __tablename__ = 'sec_to_eq'
    id = db.Column(db.Integer, primary_key=True)
    sec = db.Column(db.Integer, db.ForeignKey(Sector.sector_id))
    eq = db.Column(db.Integer, db.ForeignKey(Equipment.eq_id))

    def __init__(self, sec, eq):
        self.sec = sec
        self.eq = eq


class EqForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    sec1 = IntegerField('sector1', validators=[DataRequired()])
    sec2 = IntegerField('sector2', validators=[DataRequired()])
    sec3 = IntegerField('sector3', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/eqs_page', methods=['GET', 'POST'])
def eqs_page():
    form = EqForm()
    if form.validate_on_submit():
        eq = Equipment(name=form.name.data)
        db.session.add(eq)
        db.session.commit()

        sectors = [form.sec1.data, form.sec2.data, form.sec3.data]
        for sec in sectors:
            sec_to_eq = SecToEq(sec=sec, eq=eq.eq_id)
            db.session.add(sec_to_eq)
        db.session.commit()
        return redirect(url_for('eqs_page'))
    eqs = Equipment.query.all()
    return render_template('eqs_page.html', form=form, eqs=eqs)


@app.route('/delete_eq/<int:eq_id>', methods=['POST'])
def delete_eq(eq_id):
    eq = Equipment.query.get_or_404(eq_id)
    to_del = SecToEq.query.filter(SecToEq.eq == eq_id).all()
    for elem in to_del:
        db.session.delete(elem)
    db.session.delete(eq)
    db.session.commit()
    return redirect(url_for('eqs_page'))


@app.route('/equipment/<int:eq_id>')
def equipment_detail(eq_id):
    # Fetch equipment details based on eq_id
    # For example, using a database query or a predefined dictionary
    eq = Equipment.query.get_or_404(eq_id)

    if not eq:
        # Handle case where equipment is not found
        return "Equipment not found", 404

    sectors = set()
    factories = set()
    for elem in SecToEq.query.filter(SecToEq.eq == eq.eq_id).all():
        sector = Sector.query.get_or_404(elem.sec)
        sectors.add(sector.name)
        factories.add(sector.factory)

    return render_template('equipment_detail.html', equipment=eq, sectors=sectors, factories=factories)


@app.route('/factory/<int:factory_id>')
def factory_detail(factory_id):
    factory = Factory.query.get_or_404(factory_id)

    if not factory:
        return "Factory not found", 404

    sectors = Sector.query.filter(Sector.factory == factory_id).all()
    sector_names = set([sec.name for sec in sectors])
    equipment = set()

    for sec in sectors:
        sec_to_eqs = SecToEq.query.filter(SecToEq.sec == sec.sector_id).all()
        for elem in sec_to_eqs:
            eq = Equipment.query.get_or_404(elem.eq)
            equipment.add(eq.name)

    return render_template('factory_detail.html', factory=factory, sectors=sector_names, eqs=equipment)


@app.route('/sector/<int:sector_id>')
def sector_detail(sector_id):

    sector = Sector.query.get_or_404(sector_id)

    if not sector:
        return "Sector not found", 404

    factory = Factory.query.get_or_404(sector.factory)
    factory = factory.name

    sec_to_eqs = SecToEq.query.filter(SecToEq.sec == sector_id).all()

    equipment = set()
    for elem in sec_to_eqs:
        eq = Equipment.query.get_or_404(elem.eq)
        equipment.add(eq.name)
    return render_template('sector_detail.html', sector=sector, factory=factory, eqs=equipment)
