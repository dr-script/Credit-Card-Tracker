from flask import Flask, render_template

from flask import session
from src.common.database import Database
from datetime import datetime
from src.common.utils import Utils, Date
from src.models.user_settings.user_settings import Settings
from src.models.data.data import Data

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "12352365214"

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    #session['email'] = None
    if 'email' not in session.keys() or session['email'] == None:
        email = None
        return render_template('home.jinja2', email=email)

    else:
        settings_name = Settings.from_mongo(session['email'])
        if settings_name.name == "" or settings_name.name == None:
            email = session['email']
            credit_date = '03/10/2016'
            return render_template('home.jinja2', email=email)

        else:
            email = settings_name.name
            credit_date = '03/10/2016'
            return render_template('home.jinja2', email=email)


from src.models.users.views import user_blueprint

from src.models.users.views import user_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")


@app.route('/test')
def test_page():
    date_now = Date.current_week()
    future = Date.future_week()
    return render_template('test.jinja2', date_now=date_now, future=future)

@app.context_processor
def weekly_amount():
    if 'email' not in session.keys() or session['email'] == None:
        return {'weekly_amount': None}

    else:
        user_weekly_amount = Settings.from_mongo(session['email'])
        if user_weekly_amount.budget_amount == '' or user_weekly_amount.budget_amount == None:
            weekly_amount = 0.00
            return {'weekly_amount': weekly_amount}
        else:
            weekly_amount = Data.user_amount_weekly(session['email'])
            data_amount = Data.prices_amount(session['email'])
            weekly_amount_subtracted = weekly_amount - data_amount
            return {'weekly_amount': weekly_amount_subtracted}

@app.context_processor
def current_date():
    date_1 = datetime.utcnow()
    date_now = date_1.strftime(' %A, %B %d, %Y')
    return {'date_now': date_now}

@app.context_processor
def monthtly_amount():
    if 'email' not in session.keys() or session['email'] == None:
        return {'monthly_amount': None}

    else:
        user_monthly_amount = Settings.from_mongo(session['email'])
        if user_monthly_amount.budget_amount == '' or user_monthly_amount.budget_amount == None:
            monthly_amount = 0.00
            return {'monthly_amount': monthly_amount}
        else:
            monthtly_amount = Data.user_amount_monthly(session['email'])
            data_amount = Data.prices_amount(session['email'])
            monthly_amount_subtracted = monthtly_amount - data_amount
            return {'monthly_amount': monthly_amount_subtracted}