class User:
    def __init__(self, user_id, pin, balance, history = None):
        self.user_id = user_id
        self.__pin = pin
        self.__balance = balance
        self.history = history or []

        if history is None:
            self.history = []
        else:
            self.history = history

    @classmethod
    def from_dict(cls, user_id, data):

        return cls(
            user_id,
            data["pin"],
            data["balance"],
            data["history"]
        )

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, new_pin):
        self.__pin = new_pin

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        self.__balance = amount