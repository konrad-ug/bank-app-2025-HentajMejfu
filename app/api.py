from flask import Flask, jsonify, request
from src.AccountRegistry import AccountRegistry as ar
from src.PersonalAccount import PersonalAccount as pa

app = Flask(__name__)
registry = ar()

@app.route("/api/accounts", methods=['POST'])
def createAccount():
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400
    data: dict = request.get_json()
    print(f"Create account request: {data}")
    account: pa = pa(data["name"], data["surname"], data["pesel"])
    registry.addAccount(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def getAllAccounts():
    print("Get all accounts request received")
    accounts: list[dict] = registry.getAllAccounts()
    accounts_data: list[dict] = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def getAccountCount():
    print("Get account count request received")
    count: int = registry.getNumberOfAccounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def getAccountByPesel(pesel: str):
    print(f"Get account by PESEL request received: {pesel}")
    account: pa = registry.search(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"name": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def updateAccount(pesel: int):
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400

    data: dict = request.get_json()

    print(f"Update account request for PESEL {pesel}: {data}")

    acc: pa = registry.search(pesel)

    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    if "name" not in data and "surname" not in data:
        return jsonify({"error": "No valid fields to update"}), 400

    for key, value in data.items():
        if key == "name":
            acc.first_name = value
        elif key == "surname":
            acc.last_name = value

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def deleteAccount(pesel: int):
    acc: pa = registry.search(pesel)

    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    registry.removeAccount(pesel)
    return jsonify({"message": "Account deleted"}), 200