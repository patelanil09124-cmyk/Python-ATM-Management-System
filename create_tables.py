from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) UNIQUE NOT NULL,
    pin VARCHAR(4) NOT NULL,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(12, 2),
    receiver_id VARCHAR(25),
    sender_id VARCHAR(25),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id)
     REFERENCES users(user_id)
     ON DELETE CASCADE
    );
""")

conn.commit()

cursor.close()
conn.close()
print("User table created successfully!")


