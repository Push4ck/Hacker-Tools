import os
import getpass
import hashlib
import secrets


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return dk.hex(), salt.hex()


def lock_folder():
    while True:
        # Prompt user for folder name and password
        folder_name = input("Enter a name for the folder to lock: ")
        if os.path.exists(folder_name):
            print(f"{folder_name} already exists. Please choose a different name.")
        else:
            password = getpass.getpass("Enter a password to lock the folder: ")
            hashed_password, salt = hash_password(password)
            try:
                # Create the folder and lock it
                os.mkdir(folder_name)
                os.system(f'chmod 700 "{folder_name}"')
                with open(f'{folder_name}/.password', 'w') as f:
                    f.write(hashed_password)
                with open(f'{folder_name}/.salt', 'w') as f:
                    f.write(salt)
                print(f"{folder_name} locked successfully.")
                break
            except Exception as e:
                print(f"Error creating the folder: {str(e)}")
                break


def unlock_folder():
    # Prompt user for folder name
    folder_name = input("Enter the name of the folder to unlock: ")
    if not os.path.exists(folder_name):
        print(f"{folder_name} does not exist.")
        return

    # Prompt user for password
    with open(f'{folder_name}/.password', 'r') as f:
        hashed_password = f.read().strip()
    with open(f'{folder_name}/.salt', 'r') as f:
        salt = bytes.fromhex(f.read().strip())

    input_password = getpass.getpass("Enter the password to unlock the folder: ")
    hashed_input_password, _ = hash_password(input_password, salt)
    if hashed_password != hashed_input_password:
        print("Incorrect password.")
        return

    # Unlock the folder
    os.system(f'chmod 755 "{folder_name}"')
    print(f"{folder_name} unlocked successfully.")


if __name__ == "__main__":
    choice = input("Enter 'lock' or 'unlock' to choose an option: ")

    if choice == "lock":
        lock_folder()
    elif choice == "unlock":
        unlock_folder()
    else:
        print("Invalid choice.")
