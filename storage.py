import json

class Storage:
    FILE_NAME = "atm_data.json"

    @staticmethod
    def save(users):
        data = {}
        for user_id, user in users.items():
            data[user_id] = {
                "pin": user.pin,
                "balance": user.balance,
                "history": user.history
            }
        with open(Storage.FILE_NAME, "w") as file:
            json.dump(data, file, indent = 4)

    @staticmethod
    def load():
        try:
            with open(Storage.FILE_NAME, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            return {}