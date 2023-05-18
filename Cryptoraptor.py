import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Function to generate an RSA key pair of the given key size
def generate_rsa_key(key_size):
    """Generate an RSA key pair of the given key size."""
    key = RSA.generate(key_size)
    return key

# Function to encrypt a file using the given RSA public key
def encrypt_file(file_path, key):
    """Encrypt a file using the given RSA public key."""
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plaintext)
    with open(file_path + '.enc', 'wb') as f:
        f.write(ciphertext)

# Function to decrypt a file using the given RSA private key
def decrypt_file(file_path, key):
    """Decrypt a file using the given RSA private key."""
    with open(file_path, 'rb') as f:
        ciphertext = f.read()
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    with open(file_path[:-4], 'wb') as f:
        f.write(plaintext)

# Function to encrypt all files in a folder using the given RSA public key
def encrypt_folder(folder_path, key):
    """Encrypt all files in a folder using the given RSA public key."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            cipher = PKCS1_OAEP.new(key)
            ciphertext = cipher.encrypt(plaintext)
            with open(file_path + '.enc', 'wb') as f:
                f.write(ciphertext)
            os.remove(file_path)

# Function to decrypt all files in a folder using the given RSA private key
def decrypt_folder(folder_path, key):
    """Decrypt all files in a folder using the given RSA private key."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.enc'):
            decrypt_file(file_path, key)

# Prompt the user to enter the folder path and key size
while True:
    try:
        folder_path = input("Enter the folder path: ")
        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path. Please enter a valid path.")
        key_size = int(input("Enter the RSA key size (in bits): "))
        if key_size <= 0:
            raise ValueError("Invalid key size.")
        break
    except ValueError as e:
        print(str(e))

# Generate an RSA key pair
key = generate_rsa_key(key_size)

# Encrypt or decrypt the folder
while True:
    try:
        action = input("Do you want to encrypt or decrypt the folder? (E/D): ")
        if action.upper() == 'E':
            encrypt_folder(folder_path, key.publickey())
            print("Folder encrypted successfully.")
            break
        elif action.upper() == 'D':
            decrypt_folder(folder_path, key)
            print("Folder decrypted successfully.")
            break
        else:
            raise ValueError("Invalid action.")
    except ValueError as e:
        print(str(e))
