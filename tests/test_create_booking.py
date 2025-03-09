import allure
from pydantic import ValidationError
from conftest import generate_random_booking_data
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }

    response = api_client.create_booking(booking_data)
    response_json = response.json()

    with allure.step('Checking status code'):
        response.raise_for_status()
        assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

    with allure.step('Validating response structure'):
        try:
            BookingResponse(**response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation failed: {e}')

        assert response_json['booking']['firstname'] == booking_data['firstname']
        assert response_json['booking']['lastname'] == booking_data['lastname']
        assert response_json['booking']['totalprice'] == booking_data['totalprice']
        assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
        assert response_json['booking']['bookingdates'] == booking_data['bookingdates']
        assert response_json['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_random_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    response = api_client.create_booking(booking_data)
    response_json = response.json()

    with allure.step('Checking status code'):
        response.raise_for_status()
        assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

    with allure.step('Validating response structure'):
        try:
            BookingResponse(**response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation failed: {e}')

        assert response_json['booking']['firstname'] == booking_data['firstname']
        assert response_json['booking']['lastname'] == booking_data['lastname']
        assert response_json['booking']['totalprice'] == booking_data['totalprice']
        assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
        assert response_json['booking']['bookingdates'] == booking_data['bookingdates']
        assert response_json['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with empty body')
def test_create_booking_with_empty_body(api_client):
    booking_data = {}

    response = api_client.create_booking(booking_data)

    with allure.step('Checking status code'):
        assert response.status_code == 500, f'Expected status 500 but got {response.status_code}'


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking without required fields')
def test_create_booking_without_required_fields(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    if "firstname" in booking_data and "lastname" in booking_data:
        del booking_data["firstname"]
        del booking_data["lastname"]

    response = api_client.create_booking(booking_data)

    with allure.step('Checking status code'):
        assert response.status_code == 500, f'Expected status 500 but got {response.status_code}'


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with incorrect data type')
def test_create_booking_with_incorrect_data_type(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    if "totalprice" in booking_data:
        booking_data["totalprice"] = True

    response = api_client.create_booking(booking_data)

    with allure.step('Checking status code'):
        response.raise_for_status()
        assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with unexpected fields')
def test_create_booking_with_unexpected_fields(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    booking_data["unexpected_field"] = "some_value"  # Поле, которого нет в API

    response = api_client.create_booking(booking_data)

    with allure.step('Checking status code'):
        response.raise_for_status()
        assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'