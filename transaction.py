from datetime import datetime

class Transaction:
    def __init__(self, transaction_type, amount = None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = datetime.now().strftime("%m/%d/%y")
        self.time = datetime.now().strftime("%H:%M:%S")


    def to_dict(self):
        data = {
            "Type": self.transaction_type,
            "Date": self.date,
            "Time": self.time
        }

        if self.amount is not None:
            data["Amount"] = self.amount
        return data