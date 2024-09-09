from app import app
from equipment import Equipment, SecToEq
from sector import Sector
from factory import Factory
from flask import render_template, jsonify, Blueprint, redirect, url_for, request


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
