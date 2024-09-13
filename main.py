import sys
import sqlite3
import encryptor
import os
import random
import string

# Constants
DB_FILE = "Sqlite3.db"
e = encryptor

# Connect to the database
def connect_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        print("Database initialized")
        return conn
    except sqlite3.Error as error:
        print(f"Database connection failed: {error}")
        sys.exit(1)

# Build the database and create the table if it doesn't exist
def build_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PASSWORDS(
            USER TEXT, 
            VALUE TEXT, 
            SITE TEXT
        );
    """)
    print("Table initialized.")
    conn.commit()

# Retrieve and print all passwords
def ret_passwd(conn):
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM PASSWORDS;")
    rows = data.fetchall()

    if rows:
        encrypted_passwords = [row[1] for row in rows]
        decrypted_passwords = [e.Decrypt(pw) for pw in encrypted_passwords]
        for row, decrypted_password in zip(rows, decrypted_passwords):
            print(row[0], decrypted_password, row[2])
    else:
        print("No data found.")
    
    conn.commit()

# Add and store a new password entry
def add_passwd(conn):
    if len(sys.argv) < 5:
        print("Usage: python script.py ADD <USER> <PASSWORD> <SITE>")
        sys.exit(1)

    cursor = conn.cursor()
    user_value, pw_value, site_value = sys.argv[2], e.Encrypt(sys.argv[3]), sys.argv[4]

    cursor.execute("SELECT * FROM PASSWORDS WHERE USER=? AND SITE=?", (user_value, site_value))

    if cursor.fetchone():
        print("Error: Duplicate entry detected.")
    else:
        cursor.execute("INSERT INTO PASSWORDS (USER, VALUE, SITE) VALUES (?, ?, ?)",
                       (user_value, pw_value, site_value))
        print(f"Password for {site_value} added.")
    
    conn.commit()

# Generate a random password and store it
def generate_password(conn):
    cursor = conn.cursor()

    try:
        length = int(input("Enter the desired password length: "))
        user_value = input("Enter the username for the generated password: ")
        site_value = input("Enter the site for the generated password: ")

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))

        encrypted_password = e.Encrypt(password)
        
        cursor.execute("INSERT INTO PASSWORDS (USER, VALUE, SITE) VALUES (?, ?, ?)",
                       (user_value, encrypted_password, site_value))
        conn.commit()

        print("Generated password:", password)

    except Exception as ex:
        print(f"An error occurred: {ex}")
        conn.rollback()

# Main function
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1].upper() not in ["ADD", "RET", "GEN"]:
        print("Usage: python script.py <GEN|RET|ADD>")
        sys.exit(1)

    conn = connect_db()

    # Check and generate the encryption key if not already present
    if not os.path.exists("secret.key"):
        e.generate_key()
    else:
        print("Key already exists.")

    build_db(conn)

    method = sys.argv[1].upper()
    
    if method == "GEN":
        generate_password(conn)
    elif method == "ADD":
        add_passwd(conn)
    elif method == "RET":
        print("Retrieving stored passwords:")
        ret_passwd(conn)

    conn.close()
