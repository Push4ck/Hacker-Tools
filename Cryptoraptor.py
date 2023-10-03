import os
import pyzipper
import shutil

# Function to encrypt a folder using a password
def encrypt_folder(folder_path, output_folder, password):
    try:
        # Create a temporary folder to store the encrypted archive
        temp_folder = 'temp_encrypted_folder'
        os.makedirs(temp_folder, exist_ok=True)

        # Copy the contents of the original folder to the temporary folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(temp_folder, item))
            else:
                shutil.copy2(item_path, temp_folder)

        # Create a password-protected encrypted ZIP archive of the temporary folder
        encrypted_filename = "encrypted.zip"
        output_path = os.path.join(output_folder, encrypted_filename)
        with pyzipper.AESZipFile(output_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())
            for root, dirs, files in os.walk(temp_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_folder)
                    zf.write(file_path, arcname=arcname)

        # Remove the temporary folder
        shutil.rmtree(temp_folder)

        print("Folder encrypted successfully.")
        print(f"Encrypted file saved to: {output_path}")

    except Exception as e:
        print("Encryption failed:", str(e))

# Prompt the user to enter the folder path, password, and destination folder
while True:
    try:
        folder_path = input("Enter the folder path: ")
        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path. Please enter a valid path.")
        password = input("Enter the encryption password: ")
        output_folder = input("Enter the destination folder where the encrypted file should be saved: ")
        os.makedirs(output_folder, exist_ok=True)

        encrypt_folder(folder_path, output_folder, password)
        break
    except ValueError as e:
        print("Error:", str(e))
