from behave import *
import requests

URL = "http://127.0.0.1:5000"


@step(
    'I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"'
)
def create_account(context, name, last_name, pesel):
    json_body = {"name": f"{name}", "surname": f"{last_name}", "pesel": pesel}
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201


@step("Account registry is empty")
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert f'{response.json()["count"]}' == count


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = {f"{field}": f"{value}"}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    if field not in ["name", "surname", "balance"]:
        raise ValueError(
            f"Invalid field: {field}. Must be 'name', 'surname' or 'balance'."
        )
    response = requests.get(URL + f"/api/accounts/{pesel}")
    data = response.json()
    assert f"{data[field]}" == f"{value}"


# TRANSFERS-------------------------
@step('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    if field not in ["name", "surname", "balance"]:
        raise ValueError(
            f"Invalid field: {field}. Must be 'name', 'surname' or 'balance'."
        )
    response = requests.get(URL + f"/api/accounts/{pesel}")
    data = response.json()
    assert f"{data[field]}" == f"{value}"


@step(
    'User with pesel "{pesel}" makes "{transfer_type}" transfer with value "{amount}"'
)
def incoming_transfer(context, pesel, transfer_type, amount):
    value = int(amount)
    payload = {"amount": value, "type": transfer_type}
    requests.post(URL + f"/api/accounts/{pesel}/transfer", json=payload)