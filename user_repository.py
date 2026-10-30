from database import get_connection
from user import User

class UserRepository:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def save_user(self, user):
        query = """
        INSERT INTO users(user_id, pin, balance)
        VALUES (%s, %s, %s)
        
        ON CONFLICT(user_id)
        DO UPDATE SET
            pin = EXCLUDED.pin,
            balance = EXCLUDED.balance
        """

        self.cursor.execute(
            query,
            (
                user.user_id,
                user.pin,
                user.balance
            )
        )
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute(
            """
            SELECT user_id, pin, balance
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return User(
            user_id = row[0],
            pin = row[1],
            balance = float(row[2])
        )

