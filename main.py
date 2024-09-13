import sys
import sqlite3
import encryptor
import os



# Constants
DB_FILE = "Sqlite3.db"
e = encryptor

# Connect to the database
def connect_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        print("Database initialized")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
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
        for row in rows:
            # need to implement a master password to access the passwords
            
            # Print user, decrypted password, and site
            print(row[0], decrypted_passwords[rows.index(row)], row[2])
    else:
        print("No data found.")
    
    conn.commit()





# ADD and store a new password entry
def add_passwd(conn):
    cursor = conn.cursor()

    # Ensure proper argument length
    if len(sys.argv) < 5:

        print("Usage: python script.py ADD <USER> <PASSWORD> <SITE>")

        sys.exit(1)

    user_value = sys.argv[2]

    pw_value = sys.argv[3]

    site_value = sys.argv[4]

    pw_value = e.Encrypt(pw_value)

    cursor.execute("SELECT * FROM PASSWORDS WHERE USER=? AND SITE=?", (user_value, site_value))

    if cursor.fetchone():

        print("Error: Duplicate entry detected.")

    else:

        cursor.execute("INSERT INTO PASSWORDS (USER, VALUE, SITE) VALUES (?, ?, ?)",
                        
                       (user_value, pw_value, site_value))
        
        print(f"Password for {site_value} added.")
    
    conn.commit()


def generate_password():
    import random
    import string

    global conn  # Ensure conn is treated as a global variable
    cursor = conn.cursor()
    
    try:
        length = int(input("Enter the desired password length: "))
        user_value = input("Enter the username for the generated password: ")
        site_value = input("Enter the site for the generated password: ")
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        
        # Encrypt the password before storing
        encrypted_password = e.Encrypt(password)
        
        cursor.execute('''INSERT INTO PASSWORDS (USER, VALUE, SITE) VALUES (?, ?, ?)''',
                       (user_value, encrypted_password, site_value))
        
        # Commit the transaction to save the changes
        conn.commit()
        
        print("Generated password:", password)
        
    except Exception as ex:
        print(f"An error occurred: {ex}")
        conn.rollback()  # Rollback in case of error

if __name__ == '__main__':

    # Ensure method is provided
    if len(sys.argv) < 2 or sys.argv[1].upper() not in ["ADD", "RET", "GEN"]:

        print("Usage: python script.py <GEN|RET>")

        sys.exit(1)

    method = sys.argv[1].upper()

    conn = connect_db()

    #if the key is not generated yet, generate it

    if os.path.exists("secret.key") == False:
        e.generate_key()
    else:
        print("Key already exists.")

    build_db(conn)
    if method == "GEN":
        generate_password()
        # add the generated password to the database
        
    if method == "ADD":
        add_passwd(conn)
    elif method == "RET":
        print("Retrieving stored passwords:")
        ret_passwd(conn)
 
        

    # Close the connection at the end
    conn.close()
