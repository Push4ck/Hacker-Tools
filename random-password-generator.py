import random
import string

def generate_password(length):
    password_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password = ''.join(random.choice(password_chars) for i in range(length))
    return password

password = generate_password(16)
print(password)