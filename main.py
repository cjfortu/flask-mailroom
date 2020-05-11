import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donor, Donation

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()
# app.secret_key = base64.b32encode(os.urandom(8)).decode().strip("=")


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create a new donation based on the session user.
    """
    if request.method == 'GET':
        return render_template('create.jinja2', donor=session['donorname'])

    if request.method == 'POST':
        donor = Donor.get(Donor.name == session['donorname'])
        donation = Donation(value=request.form['donation'], donor=donor)
        donation.save()
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login for an existing donor, then redirect to creating a new donation.
    """
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        try:
            donor = Donor.get(Donor.name == name)
            # user = User.select().where(User.name == name).get()
        except Donor.DoesNotExist:
            return render_template('login.jinja2', error='Donorname or Password incorrect.')
        else:
            if pbkdf2_sha256.verify(password, donor.password):
                session['donorname'] = donor.name
                return redirect(url_for('create'))
            else:
                return render_template('login.jinja2', error='Donorname or Password incorrect.')

    else:
        return render_template('login.jinja2')


@app.route('/new_donor', methods=['GET', 'POST'])
def new_donor():
    """
    Add a new donor with password, then redirect to creating a new donation.
    """
    names = [donor.name for donor in Donor.select()]

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name in names:
            return render_template('new_donor.jinja2', error='Donor already exists.')
        else:
            donor = Donor(name=name, password=pbkdf2_sha256.hash(password))
            donor.save()
            session['donorname'] = donor.name
            return redirect(url_for('create'))

    else:
        return render_template('new_donor.jinja2')


@app.route('/donor_all', methods=['GET', 'POST'])
def donor_alls():
    """
    Search a donor and display all their donations.
    """
    if request.method == 'GET':
        return render_template('donor_all.jinja2')

    if request.method == 'POST':
        try:
            donor = Donor.get(Donor.name == request.form['name'])
        except Donor.DoesNotExist:
            return render_template('donor_all.jinja2', error='Donor does not exist.')
        else:
            query = Donation.select().where(Donation.donor == donor)
            print('ok heres the query', query)
            donations = [donation.value for donation in query]
            print('ok heres the donations', donations)
            return render_template('donor_all.jinja2', donor=donor.name, donations=donations)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
