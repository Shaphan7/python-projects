import os
import hmac
import hashlib
from cryptography.fernet import Fernet

# Project: data-encrypter

Access = True

files = []
#b_#as#cat
real_password_hash = "6860ad0464fdd5a74c590165d56d908210cef83eb5dcf008c69e198b1b9ab2c4"
excluded_files = ["dataEncrypter.py", "key.key"]
def loadKey():
    global Access
    password = input("Password: ")
    is_match = hmac.compare_digest(hashlib.sha3_256(password.encode('utf-8')).hexdigest(), real_password_hash)
    if is_match:
        print("Access granted!")
        with open("key.key", "rb") as file:
            return file.read()
    else:
        Access = False
        return "Restricted!"
def saveNewKey():
    with open("key.key", "wb") as file:
        key = Fernet.generate_key()
        file.write(key)
try:
    fernet = Fernet(loadKey())
except ValueError:
    pass
def encrypt():
    for file_path in files:
        with open(file_path, "rb") as file:
            original_data = file.read()
        encrypted_data = fernet.encrypt(original_data)

        with open(file_path, "wb") as file:
            file.write(encrypted_data)
    print("Data has successfully been encrypted!")     
def decrypt():
    for file_path in files:
        with open(file_path, "rb") as file:
            original_data = file.read()
        decrypted_data = fernet.decrypt(original_data)

        with open(file_path, "wb") as file:
            file.write(decrypted_data)
    print("Data has successfully been decrypted!")
commands = {
    "encrypt": lambda: encrypt(),
    "decrypt": lambda: decrypt()
}

for file in os.listdir():
    if file in excluded_files:
        continue
    if os.path.isfile(file):
        files.append(file)
def main():
    if Access:
        print("|----------Encrypter----------|")
        while True:
            command = input("Command: ")
            if command in commands:
                commands[command]()
            elif command == "exit": 
                print("|---------App-Closed----------|")
                break
            else:
                print("The syntax of the command is incorrect! (use 'exit' or 'help')")
    else: 
        print("Access denied!")
main()
