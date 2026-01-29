from flask import Flask, jsonify, request
from src.AccountRegistry import AccountRegistry as ar
from src.PersonalAccount import PersonalAccount as pa
from src.MongoAccountsRepository import MongoAccountRepository

app = Flask(__name__)
registry = ar()

@app.route("/api/accounts", methods=['POST'])
def createAccount():
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400
    data: dict = request.get_json()
    if registry.search(data["pesel"]):
        return jsonify({"error": "Account already exists"}), 409
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

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def handleTransfer(pesel):
    acc: pa = registry.search(pesel)

    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.get_json()

    if "amount" not in data or "type" not in data:
        return jsonify({"error": "Missing data"}), 400

    if data['type'] not in ['express', 'outgoing', 'incoming']:
        return jsonify({"error": "Invalid transfer type"}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400

        r = None

        if data['type'] == 'incoming':
            r = acc.receiveTransfer(amount)
        elif data['type'] == 'outgoing':
            r = acc.normalTransfer(amount)
        elif data['type'] == 'express':
            r = acc.expressTransfer(amount)

    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid amount"}), 400

    if r:
        return jsonify({"message": "Accepted for processing"}), 200

    else:
        return jsonify({"error": "Insufficient funds"}), 422

@app.route("/api/accounts/save", methods=["POST"])
def saveAccounts():
    repo = MongoAccountRepository()
    repo.save_all(registry.getAllAccounts())
    return jsonify({"message": "Accounts saved to MongoDB"}), 200


@app.route("/api/accounts/load", methods=["POST"])
def loadAccounts():
    repo = MongoAccountRepository()
    accounts = repo.load_all()
    registry.accounts = []
    for account in accounts:
        registry.addAccount(account)
    return jsonify({"message": "Accounts loaded from MongoDB"}), 200