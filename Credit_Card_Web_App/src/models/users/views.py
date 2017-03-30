from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
from datetime import datetime
from src.common.utils import Utils, Date
from src.models.data.data import Data
from src.models.user_settings.user_settings import Settings

from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST']) # GET simply gets something from the server. POST = The website sending us data
def login_user():
    if request.method == 'POST':
        # Check Login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email # stores a unique ID for user
                return redirect('/')

        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Check Login is valid
        email = request.form['email']
        password = request.form['password']


        try:
            if User.register_user(email, password):
                session['email'] = email # stores a unique ID for user
                return redirect('/')

        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")

@user_blueprint.route('/data')
def user_data():
    settings_start_date = Settings.from_mongo(session['email'])
    if settings_start_date.billing_start_date == '' or settings_start_date.billing_start_date == None:
        date_now_future = Date.future_week()
        current_date = Date.view_page_date()
        data = Data.from_email(session['email'])
        z = Data.prices_amount(session['email'])
        return render_template('test.jinja2', date_now_future=date_now_future, current_date=current_date, data=data, z=z)

    #user = User.find_by_email(session['email'])
    else:
        #data = Data.from_mongo(session['email'])
        date_now_future = Data.test(session['email'])#Date.current_week()
        #data_date = data.date
        #data_description = data.description
        #data_price = data.price
        current_date = Date.view_page_date()
        data = Data.from_email(session['email'])
        z = Data.prices_amount(session['email'])
        return render_template('test.jinja2', date_now_future=date_now_future, current_date=current_date, data=data, z=z)

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/settings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'POST':
        credit_date = request.form['credit_date']
        name = request.form['name']
        monthly_budget_amount = request.form['monthly_budget_amount']
        settings = Settings(session['email'], credit_date, monthly_budget_amount, name)
        settings.save_to_mongo()
        return redirect(url_for('users.user_settings'))

    settings_name = Settings.from_mongo(session['email'])
    if settings_name.name == "" or settings_name.name == None:
        email = session['email']
        credit_date = 'No date selected'
        budget_amount = '$00.00'
        return render_template("users/settings.jinja2", email=email, credit_date=credit_date, budget_amount=budget_amount)

    else:
        email = settings_name.name
        credit_date = Date.user_date_selected(session['email'])
        budget_amount = settings_name.budget_amount
        return render_template("users/settings.jinja2", email=email, credit_date=credit_date, budget_amount=budget_amount)


        #Settings.from_mongo(session['email'])
    #credit_date = '03/10/2016'
    #return render_template("users/settings.jinja2", email=email, credit_date=credit_date)

@user_blueprint.route('/add', methods=['GET', 'Post'])
def add_item():
    current_date = Date.add_page_date()
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = int(request.form['amount'])
        category = request.form['category']
        data = Data(session['email'], amount, date, description, category)
        data.save_to_mongo()
        return redirect(url_for('users.user_data'))
    return render_template("users/add.jinja2", current_date=current_date)