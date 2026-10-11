from validator import Validator
import shutil

class Admin:
    def __init__(self, users):
        self.users = users
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
        if not self.users:
            print("\nNo Users Found.")
            return

        print("\n==============All Users=============")

        for user_id, user in self.users.items():
            print(f"""
            User ID: {user_id}
            Balance: ₹{user.balance}
            ------------------------------
            """)


    def delete_user(self):
        user_id = input("\nEnter User ID to delete: ").strip().lower()

        if user_id not in self.users:
            print("\nUser Not Found.")
            return

        user = self.users[user_id]

        print(f"""
        User Found:
        
        User ID: {user.user_id}
        Balance: {user.balance}
        """)

        confirm = input("Are you sure you want to delete? (y/n): ").lower()
        if confirm == "y":
            del self.users[user_id]
            print("\nUser Deleted Seccessfully.")

        else:
            print("\nDelete Cancelled.")

    def reset_user_pin(self):
        user_id = input("\nEnter User ID: ").strip().lower()

        if user_id not in self.users:
            print("\nUser Not Found.")

        user = self.users[user_id]
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

        user.pin = new_pin

        print("\nPIN Reset Successfully.")


    def search_user(self):
        user_id = input("\nEnter User ID to search: ").strip().lower()

        if user_id not in self.users:
            print("\nUser Not Found.")
            return

        user = self.users[user_id]

        print("""\n
        ==================User Details=====================
        """)

        print(f"User ID: {user.user_id}")
        print(f"Balance: ₹ {user.balance}")
        print(f"Total Transactions: {len(user.history)}")

    def total_balance(self):
        total_amount = 0
        for user in self.users.values():
            total_amount += user.balance

        print(f"\nTotal ATM Balance: ₹{total_amount}")

    def total_users(self):
        total = len(self.users)
        print(f"\nTotal Users: {total}")

    @staticmethod
    def backup_database():
        try:

            shutil.copy(
                "atm_data.json",
                "backup_database.json"
            )

            print("\nDatabase Backup Created Successfully.")

        except FileNotFoundError:
            print("\nDatabase file nor found.")

    @staticmethod
    def restore_database():
        try:

            shutil.copy(
                "atm_backup.json",
                "atm_data.json"
            )

            print("\nDatabase Restored Successfully.")

        except FileNotFoundError:
            print("\nBackup file not found.")