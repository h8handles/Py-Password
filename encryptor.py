from cryptography.fernet import Fernet
import os

# Constants
KEY_FILE = "secret.key"

def generate_key():
    """Generate a key for encryption and decryption and save it securely."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    # This will generate a key and save it to 'secret.key'.
    # Consider storing this key securely, such as in an environment variable or key vault.

def load_key():
    """Load the previously generated key from a file."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError(f"Key file '{KEY_FILE}' not found. Please generate the key first.")
    
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def Encrypt(secret: str) -> bytes:
    """Encrypt the given secret using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(secret.encode())

def Decrypt(encrypted_secret: bytes) -> str:
    """Decrypt the given encrypted secret using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_secret).decode()

# Example usage (commented out for production use)
if __name__ == "__main__":
    if not os.path.exists(KEY_FILE):
        generate_key()  # Generate a key if one doesn't exist
    '''
    secret = "my super secret password"
    encrypted = Encrypt(secret)
    print(f"Encrypted: {encrypted}")
    decrypted = Decrypt(encrypted)
    print(f"Decrypted: {decrypted}")  # Should print "my super secret password" if successful
    '''
