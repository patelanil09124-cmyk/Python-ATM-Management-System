from user import User
from storage import Storage
from transaction import Transaction
from admin import Admin
from validator import Validator
import time
import sys


class ATM:

    # 1. Constructor / Start
    def __init__(self):
        self.__users = {}
        self.__current_user = None
        self.__storage = Storage()
        self.load_data()
        self.admin = Admin(self.__users)

    def start(self):
        self.main_menu()


    # 2. Main Menus
    def main_menu(self):
        atm_name = "SBI"
        while True:
            print(f"""
                      ==============={atm_name} ATM===============
                      1. Create User ID
                      2. User Login
                      3. Admin Login
                      =====================================
            """)

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.create_user()

                elif choice == 2:
                    if self.user_login():
                        self.atm_menu()

                elif choice == 3:
                    if self.admin.login():
                        self.admin_menu()

                else:
                    print("\nPlease enter a valid choice.")

            except ValueError:
                print("\nPlease enter a valid input.")


    def admin_menu(self):
        while True:
            print("""
            =================Admin Menu==================
            1. Show All Users
            2. Total Users
            3. Total Balance
            4. Search User
            5. Delete User
            6. Reset User PIN
            7. Backup Database
            8. Restore Database
            9. System Shutdown
            0. Logout
            =============================================
            """)

            try:
                choice = int(input("Enter Choice: "))

                if choice == 1:
                    self.admin.show_all_users()

                elif choice == 2:
                    self.admin.total_users()

                elif choice == 3:
                    self.admin.total_balance()

                elif choice == 4:
                    self.admin.search_user()

                elif choice == 5:
                    self.admin.delete_user()
                    self.save_data()

                elif choice == 6:
                    self.admin.reset_user_pin()

                elif choice == 7:
                    self.admin.backup_database()

                elif choice == 8:
                    self.admin.restore_database()

                elif choice == 9:
                    if self.admin.system_shutdown():
                        sys.exit()

                elif choice == 0:
                    print("\nAdmin Logout.")
                    break

                else:
                    print("Invalid Choice.")

            except ValueError:
                print("Please enter a valid input.")


    def atm_menu(self):
        while True:
            start_time = time.time()
            print(f"""
                        ==========Welcome {self.__current_user.user_id}==========
                        1. Check Balance 
                        2. Withdraw Money
                        3. Deposit Money
                        4. Transfer Money
                        5. Change PIN
                        6. Transaction History 
                        0.Logout
                        =====================================
            """)

            try:
                user_input = int(input("Enter your choice: "))
                if user_input == 1:
                    if self.check_session(start_time):
                        break
                    self.check_balance()

                elif user_input == 2:
                    if self.check_session(start_time):
                        break
                    self.withdraw_money()

                elif user_input == 3:
                    if self.check_session(start_time):
                        break
                    self.deposit_money()

                elif user_input == 4:
                    if self.check_session(start_time):
                        break
                    self.transfer_money()

                elif user_input == 5:
                    if self.check_session(start_time):
                        break
                    self.change_pin()

                elif user_input == 6:
                    if self.check_session(start_time):
                        break
                    self.show_transaction_history()

                elif user_input == 0:
                    self.logout()
                    break

                else:
                    print("\nPlease enter a valid input.")

            except ValueError:
                print("\nPlease enter a valid input.")


    # 3. User Creation & Authentication
    def create_user(self):
        while True:

            user_id = input("\nCreate User ID(0 to cancel): ").strip().lower()
            if user_id == "0":
                return

            valid, message = Validator.is_valid_user_id(user_id)

            if not valid:
                print(message)
                continue

            if user_id in self.__users:
                print("\nUser ID already exists.")
                continue

            self.create_pin(user_id)
            print("\nAccount Created Successfully.")
            print(f"User ID: {user_id}")
            return


    def create_pin(self, user_id):
        while True:
            pin = self.get_new_pin()

            user = User(user_id, pin, 0)
            self.__users[user_id] = user
            self.save_data()
            return


    @staticmethod
    def get_new_pin():
        while True:
            new_pin = input("\nCreate 4-digit PIN: ")
            confirm_pin = input("Confirm 4-digit PIN: ")

            valid, message = Validator.is_valid_pin(new_pin, confirm_pin)

            if not valid:
                print(message)
                continue

            return new_pin


    def user_login(self):
        user_id = input("\nEnter User ID:").strip().lower()

        if user_id not in self.__users:
            print("\nUser Not Found.")
            return False

        user = self.__users[user_id]

        max_attempts = 3
        for attempts_left in range(max_attempts, 0, -1):
            pin = input("\nEnter Pin: ")

            if pin == user.pin:
                self.__current_user = user
                print("\nLogin Successful.")
                return True

            elif attempts_left > 1:
                print(f"\nIncorrect Pin."
                      f" {attempts_left - 1} attempts remaining.")
            else:
                print("\nMaximum Attempts Exceeded.")

        return False


    def check_pin(self):
        user = self.__current_user

        max_attempts = 3
        for attempts_left in range(max_attempts, 0, -1):

            if input("\nEnter PIN: ") == user.pin:
                return True

            elif attempts_left > 1:
                print(f"\nIncorrect Pin. {attempts_left - 1} attempts remaining.")

            else:
                print("\nMaximum Attempts Exceeded.")

        return False


    # 4. Session Management
    def check_session(self, start_time):
        if (time.time() - start_time) > 60:
            self.__current_user = None
            print("\nSession Expired."
                  "\nPlease try again.")
            return True

        else:
            return False


    def logout(self):
        self.__current_user = None
        print("\nLogout Successfully.")
        print("Thank you for using ATM.")


    # 5. Account Operations
    def check_balance(self):
        print(f"\nCurrent Balance: ₹ {self.__current_user.balance}")


    def deposit_money(self):
        user = self.__current_user
        while True:
            try:
                amount = int(input("\nEnter Deposit Amount(0 to cancel): "))

                if amount == 0:
                    print("\nDeposit Cancelled.")
                    return

                valid, message = Validator.is_valid_amount(amount)

                if not valid:
                    print(message)
                    continue

                if amount < 100 or amount > 10000:
                    print("\nDeposit amount must be between 100 and 50000.")
                    continue

                user.balance += amount
                transaction = Transaction("Deposit", amount)
                user.history.append(transaction.to_dict())
                self.save_data()

                print("\nAmount Deposited Successfully.")
                print(f"\nCurrent Balance: ₹ {user.balance}")
                return

            except ValueError:
                print("\nPlease enter a valid amount.")


    def withdraw_money(self):
        user = self.__current_user

        if user.balance < 100:
            self.check_balance()
            print("\nInsufficient Balance.")
            return

        while True:
            try:
                amount = int(input("\nEnter Withdraw Amount(0 to cancel): "))

                if amount == 0:
                    print("\nWithdraw Cancelled.")
                    return

                valid, message = Validator.is_valid_amount(amount)
                if not valid:
                    print(message)
                    continue

                if amount < 100 or amount > 20000:
                    print("\nWithdraw amount must be between 100 and 20000.")
                    continue

                if amount > user.balance:
                    self.check_balance()
                    print("\nInsuficient Balance.")
                    continue

                user.balance -= amount

                transaction = Transaction("Withdraw", amount)
                user.history.append(transaction.to_dict())

                self.save_data()
                print("\nWithdraw Successfully.")
                self.check_balance()
                return

            except ValueError:
                print("\nPlease enter a valid amount.")


    def transfer_money(self):
        while True:
            receiver_id = input("\nEnter Receiver User ID(0 to cancel): ").strip().lower()

            if receiver_id == "0":
                print("\nTransfer Cancelled.")
                return

            if receiver_id not in self.__users:
                print("\nUser Not Found.")
                continue

            if receiver_id == self.__current_user.user_id:
                print("You cannot transfer money to yourself.")
                continue

            sender = self.__current_user
            receiver = self.__users[receiver_id]

            try:
                amount = int(input("\nEnter Transfer Amount(0 to cancel): "))

                if amount == 0:
                    print("\nTransfer Cancelled.")
                    return

                valid, message = Validator.is_valid_transfer_amount(amount)
                if not valid:
                    print(message)
                    continue

                if amount > sender.balance:
                    print("\nInsufficient Balance.")
                    continue

                sender.balance -= amount
                receiver.balance += amount

                sender_transaction = Transaction("Transfer", amount)
                data = sender_transaction.to_dict()
                data["To"] = receiver_id
                sender.history.append(data)

                receiver_transaction = Transaction("Receive", amount)
                data = receiver_transaction.to_dict()
                data["From"] = sender.user_id
                receiver.history.append(data)

                self.save_data()

                print("Money Transfered Successfully.")
                return

            except ValueError:
                print("\nPlease enter a valid amount.")


    def change_pin(self):
        user = self.__current_user
        if self.check_pin():

            while True:
                new_pin = self.get_new_pin()

                if new_pin == user.pin:
                    print("\nNew PIN cannot be same as old PIN.")
                    continue

                user.pin = new_pin

                transaction = Transaction("Change Pin")
                user.history.append(transaction.to_dict())

                self.save_data()
                print("\nPIN Changed Successfully.")
                return


    # 6. Transaction History
    def show_transaction_history(self):
        user = self.__current_user

        if not user.history:
            print("\nNo Transactions Found.")
            return

        for transaction in user.history:

            for key, value in transaction.items():
                print(f"{key}: {value}")
            print("------------------------")


    # 7. Data Storage
    def save_data(self):
        self.__storage.save(self.__users)


    def load_data(self):
        data = self.__storage.load()

        for user_id, user_data in data.items():
            self.__users[user_id] = User.from_dict(
                user_id,
                user_data
            )

