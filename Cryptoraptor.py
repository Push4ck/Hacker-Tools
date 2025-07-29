import os
import shutil
import argparse
import pyzipper


def encrypt_folder(folder_path, output_folder, password, overwrite=False):
    temp_folder = 'temp_encrypted_folder'
    os.makedirs(temp_folder, exist_ok=True)

    try:
        # Copy folder content
        for item in os.listdir(folder_path):
            src = os.path.join(folder_path, item)
            dst = os.path.join(temp_folder, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, temp_folder)

        # Define output path
        encrypted_zip = os.path.join(output_folder, "encrypted.zip")

        # Handle overwrite
        if os.path.exists(encrypted_zip) and not overwrite:
            raise FileExistsError(f"{encrypted_zip} already exists. Use --overwrite to force.")

        # Write encrypted zip
        with pyzipper.AESZipFile(encrypted_zip, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())
            for root, _, files in os.walk(temp_folder):
                for file in files:
                    path = os.path.join(root, file)
                    arcname = os.path.relpath(path, temp_folder)
                    zf.write(path, arcname=arcname)

        print(f"✅ Folder encrypted successfully → {encrypted_zip}")

    except Exception as e:
        print(f"❌ Encryption failed: {e}")
    finally:
        shutil.rmtree(temp_folder, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Encrypt a folder into a password-protected zip file.")
    parser.add_argument('--folder', required=True, help='Path of folder to encrypt')
    parser.add_argument('--output', required=True, help='Destination folder to save encrypted ZIP')
    parser.add_argument('--password', required=True, help='Encryption password')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing encrypted.zip if exists')
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print("❌ Error: Input folder does not exist.")
        return

    os.makedirs(args.output, exist_ok=True)
    encrypt_folder(args.folder, args.output, args.password, args.overwrite)


if __name__ == '__main__':
    main()