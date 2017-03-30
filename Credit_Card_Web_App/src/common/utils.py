import datetime
from passlib.hash import pbkdf2_sha512
import re

from src.models.user_settings.user_settings import Settings


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)



class Date():

    @staticmethod
    def current_date():
        time_now = datetime.datetime.now()
        return time_now.strftime('%B %d, %Y')

    @staticmethod
    def current_week():
        global date_1
        time_now = datetime.datetime.now()
        week1 = time_now.strftime('%m/%d/%y')
        #print(week1)
        date_1 = datetime.datetime.strptime(week1, "%m/%d/%y")


        # print(plus_seven)
        #print(z)

        return week1

    @staticmethod
    def add_page_date():
        time_now = datetime.datetime.now()
        return time_now.strftime('%A')

    @staticmethod
    def view_page_date():
        time_now = datetime.datetime.now()
        return time_now.strftime('%A, %B %d %Y')


    @staticmethod
    def future_week():
        date_1 = datetime.datetime.utcnow()
        plus_seven = date_1 + datetime.timedelta(days=7)
        z = plus_seven.strftime('%b %d')
        current_date = date_1.strftime('%b %d')
        return current_date + ' - ' + z

    @staticmethod
    def user_date_selected(user_email):
        date = Settings.from_mongo(user_email)
        user_date = date.billing_start_date
        year = user_date[0:4]
        month = user_date[5:7]
        day = user_date[8:10]
        year_int = int(year)
        month_int = int(month)
        day_int = int(day)
        my_time = datetime.date(year_int, month_int, day_int)
        modified_date = my_time.strftime('%B, %d %Y')
        return modified_date




        #time_now = datetime.datetime.now()
        #week = time_now.strftime('%b 1 - %b 7')
        #week = time_now.strftime('%m/%d/%y')
        #date_1 = datetime.datetime.strptime(week, "%m/%d/%y")
        #zy = date_1.strftime('%m/%d/%y')

        #d = datetime.timedelta(days=7)
        #z = date_1 + datetime.timedelta(days=7)
        #xx = z.strftime('%b %d')
        #return week


