import datetime
from datetime import timedelta, date
from core.clients.api_client import APIClient
import pytest
from faker import Faker


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = date.today()
    checking_date = today + timedelta(days=10)
    checkout_date = checking_date + timedelta(days=5)

    return {
        "checkin": checking_date.strftime('%Y-%m-%d'),
        "checkout": checkout_date.strftime('%Y-%m-%d')
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }

    return data
