import os
import subprocess
from database import get_connection
from user import User
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Storage:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()


    def save(self, users):
        query = """
        INSERT INTO users (user_id, pin, balance)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
        pin = EXCLUDED.pin,
        balance = EXCLUDED.balance;
        """

        for user in users.values():
            self.cursor.execute(query,
                                (user.user_id, user.pin, user.balance)
            )
            self.conn.commit()


    def load(self):
        self.cursor.execute("""
        SELECT user_id, pin, balance
        FROM users
        """)

        users = {}

        for user_id, pin, balance in self.cursor.fetchall():
            users[user_id] = User(user_id = user_id, pin = pin, balance = float(balance))

        return users


    def save_transaction(self, user_id, transaction_type, amount = None,
                          sender_id = None, receiver_id = None):
        query = """
        INSERT INTO transactions
        (
            user_id,
            transaction_type,
            amount,
            sender_id,
            receiver_id
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(
            query,
            (
                user_id,
                transaction_type,
                amount,
                sender_id,
                receiver_id
            )
        )
        self.conn.commit()

    def get_transactions(self, user_id):
        self.cursor.execute("""
        SELECT
            transaction_type,
            amount,
            sender_id,
            receiver_id,
            transaction_date
        FROM transactions
        WHERE user_id = %s
        ORDER BY transaction_date DESC
        """,(user_id,))

        return self.cursor.fetchall()

    def delete_user(self, user_id):
        self.cursor.execute(
            "DELETE FROM users WHERE user_id = %s",
            (user_id,)
        )

        self.conn.commit()

    def update_pin(self, user_id, pin):
        self.cursor.execute(
            """
            UPDATE users
            SET pin = %s
            WHERE user_id = %s
            """,
            (pin, user_id)
        )

        self.conn.commit()

    def get_transaction_count(self, user_id):
        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE user_id = %s
            """,
            (user_id,)
        )

        return self.cursor.fetchone()[0]


    def get_system_statistics(self):
        self.cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM users),
            (SELECT COALESCE(SUM(balance), 0) FROM users),
            (SELECT COUNT(*) FROM transactions)
        """)

        return self.cursor.fetchone()


    @staticmethod
    def backup_database():
        backup_folder = "backups"
        os.makedirs(backup_folder, exist_ok = True)

        file_name = datetime.now().strftime(
            "backup_%Y-%m-%d_%H-%M-%S.backup")

        backup_path = os.path.join(backup_folder, file_name)

        os.environ["PGPASSWORD"] = os.getenv("DB_PASSWORD", "")

        command = [
            r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe",
            "-U", "postgres",
            "-F", "c",
            "-d", "atm_db",
            "-f", backup_path
        ]

        try:
            subprocess.run(command, check = True)
            print("\nBackup Created Successfully.")
            print(f"Location: {backup_path}")

        except Exception as e:
            print("\nBackup Failed.")
            print(e)



    @staticmethod
    def get_backup_files():
        backup_folder = "backups"

        if not os.path.exists(backup_folder):
            return []

        files = [file for file in os.listdir(backup_folder)
                 if file.endswith(".backup")
        ]

        files.sort(reverse = True)

        return files


    def restore_database(self, file_name):

        backup_path = os.path.join("backups",file_name)

        os.environ["PGPASSWORD"] = os.getenv("DB_PASSWORD", "")

        # Close current connection
        self.cursor.close()
        self.conn.close()

        command = [
            r"C:\Program Files\PostgreSQL\17\bin\pg_restore.exe",
            "-h", "localhost",
            "-U", "postgres",
            "-d", "atm_db",
            "--clean",
            "--if-exists",
            backup_path
        ]

        try:
            subprocess.run(command, check = True)

            self.conn = get_connection()
            self.cursor = self.conn.cursor()
            print("\nDatabase Restored Successfully.")

        except Exception as e:
            print("\nRestore Failed.")
            print(e)

