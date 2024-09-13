from cryptography.fernet import Fernet

def generate_key():
    """Generate a key for encryption and decryption."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
        '''
        This will generate a key and save it to a file named 'secret.key'. Eventually we 
        need to make this an ENV variable or some other secure storage.

        '''

def load_key():
    """Load the previously generated key."""
    key = open("secret.key", "rb").read()
    #close the file after read
    return key

def Encrypt(secret):
    """Encrypt the given secret."""
    key = load_key()
    encodeSecret = secret.encode()
    fer = Fernet(key)
    return fer.encrypt(encodeSecret)

def Decrypt(encrypted_secret):
    """Decrypt the given secret."""
    key = load_key()
    fer = Fernet(key)
    decryptSecret = fer.decrypt(encrypted_secret)
    return decryptSecret.decode()

# Example usage
if __name__ == "__main__":
    generate_key()  # Generate a key (only need to do this once)
    '''secret = "my super secret password"
    encrypted = Encrypt(secret)
    print(f"Encrypted: {encrypted}")
    decrypted = Decrypt(encrypted)
    print(f"Decrypted: {decrypted}")  # Should print "my super secret password" if everything works correctly.'''
    