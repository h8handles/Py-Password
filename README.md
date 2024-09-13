## About
This is a simple python script that stores passwords in a sqlite3 database encrypted and retrieves the decrypted values

## To do
add functionality to generation function in main.py to randomly generate password
- right now it only allows for user to add password manually

### Usage

python3 main.py GEN <username> <password> <site>
- this will add an encrypted password to the database

python3 main.py RET
- this will return all the passwords stored in the database unencrypted

![image](https://github.com/user-attachments/assets/dec66c14-fae7-46e8-8aad-3da64e91a73f)

Encrypted value stored in DB

![image](https://github.com/user-attachments/assets/3155f668-e850-479a-9bcd-6750194b9b15)
