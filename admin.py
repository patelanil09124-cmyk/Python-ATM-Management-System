from validator import Validator

class Admin:
    def __init__(self, users, storage):
        self.__users = users
        self.__storage = storage
        self.__admin_id = "admin123"
        self.__password = "Admin123@"


    def login(self):
        max_attempts = 3

        for attempt_left in range(max_attempts, 0, -1):
            admin_id = input("\nAdmin ID(0 to cancel): ")

            if admin_id == "0":
                return False

            if admin_id == self.__admin_id:
                if self.check_password():
                    print("Login Successfully.")
                    return True

            elif max_attempts > 1:
                print(f"\nInvalid Admin ID."
                      f"\n{attempt_left - 1} attempts remaining.")
                continue

            else:
                print("\nMaximum attempts exceeded.")
                return False

        return False


    def check_password(self):
        max_attempts = 3

        for attempt_left in range(max_attempts, 0, -1):

            password = input("\nPassword: ")
            if password == self.__password:
                return True

            elif attempt_left > 1:
                print(f"\nWorng Password."
                      f"\n{attempt_left - 1} attempts remaining.")
                continue

            else:
                print("Maximum attempts exceeded.")
                return False
        return False


    def system_shutdown(self):
        while True:
            print("""
            1. System Shutdown
            0. Cancel
            """)

            try:
                choice = int(input("Enter Choice: "))
                if choice == 0:
                    return False

                elif choice == 1:
                    if self.check_password():
                        print("System Shutdown.")
                        return True

                    return False

                else:
                    print("Please enter a valid choice.")
            except ValueError:
                print("Please enter a valid input.")


    def show_all_users(self):
        if not self.__users:
            print("\nNo Users Found.")
            return

        print("\n==============All Resistered Users=============")

        for user in self.__users.values():
            transaction_count = self.__storage.get_transaction_count(user.user_id)
            print(f"""
            User ID: {user.user_id}
            Balance: ₹{user.balance}
            Total Transactions: {transaction_count}
            ------------------------------""")


    def delete_user(self):
        user_id = input("\nEnter User ID to delete: ").strip().lower()

        if user_id not in self.__users:
            print("\nUser Not Found.")
            return

        user = self.__users[user_id]

        print(f"""
        --------User Found-------
        User ID: {user.user_id}
        Balance: {user.balance}
        -------------------------
        """)

        confirm = input("Are you sure you want to delete? (y/n): ").lower()
        if confirm == "y":
            del self.__users[user_id]
            self.__storage.delete_user(user_id)
            print("\nUser Deleted Seccessfully.")

        else:
            print("\nDelete Cancelled.")

    def reset_user_pin(self):
        user_id = input("\nEnter User ID: ").strip().lower()

        if user_id not in self.__users:
            print("\nUser Not Found.")
            return

        user = self.__users[user_id]
        print(f"\nUser Found: {user.user_id}")

        new_pin = input("Enter New PIN: ")
        confirm_pin = input("Confirm New PIN: ")

        valid, message = Validator.is_valid_pin(new_pin, confirm_pin)
        if not valid:
            print(message)
            return

        if new_pin == user.pin:
            print("\nNew PIN cannot be same as old PIN.")
            return

        self.__storage.update_pin(
            user.user_id,
            new_pin
        )

        print("\nPIN Reset Successfully.")


    def search_user(self):
        user_id = input("\nEnter User ID to search: ").strip().lower()

        if user_id not in self.__users:
            print("\nUser Not Found.")
            return

        user = self.__users[user_id]

        transaction_count = self.__storage.get_transaction_count(user.user_id)

        print("""\n
        ==================User Details=====================
        """)

        print(f"User ID: {user.user_id}")
        print(f"Balance: ₹ {user.balance}")
        print(f"Total Transactions: {transaction_count}")


    def show_system_statistics(self):
        total_users, total_balance, total_transactions = (
            self.__storage.get_system_statistics()
        )

        print("\n=======ATM STSTEM STATISTICS=======")
        print(f"Total Users: {total_users}")
        print(f"Total Balance: {total_balance}")
        print(f"Total Transactions: {total_transactions}")
        print("=====================================")


    def backup_database(self):
        self.__storage.backup_database()


    def restore_database(self):
        files = self.__storage.get_backup_files()

        if not files:
            print("\nNo Backup Files Found.")
            return

        print("\nAvailable Backups...\n")
        for index, file in enumerate(files, start = 1):
            print(f"{index}.{file}")

        choice = int(input("\nSelect Backup: "))
        if choice < 1 or choice > len(files):
            print("\nInvalid Choice.")
            return

        confirmation = input("\nRestore Database? (Y/N): ").strip().upper()

        if confirmation == "Y":
            self.__storage.restore_database(
                files[choice - 1]
            )


