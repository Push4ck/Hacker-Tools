import random
import string

# Define the generate_password function
def generate_password(length):
    # Check if the length is less than 8 characters
    if length < 8:
        # Raise an exception if length is less than 8 characters
        raise Exception("Password length should be at least 8 characters")

    # Store the lowercase characters
    lowercase_chars = string.ascii_lowercase

    # Store the uppercase characters
    uppercase_chars = string.ascii_uppercase

    # Store the digits
    digits_chars = string.digits

    # Store the special characters
    special_chars = "!@#$%^&*"

    # Choose one random character from each set
    password = random.choice(lowercase_chars) + random.choice(uppercase_chars) + random.choice(digits_chars) + random.choice(special_chars)

    # Combine the sets of characters
    password_chars = lowercase_chars + uppercase_chars + digits_chars + special_chars

    # Choose random characters to complete the password
    password += ''.join(random.choice(password_chars) for i in range(length - 4))

    # Return the password
    return password

# Define a function to check password strength
def check_password_strength(password):
    length = len(password)
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*" for char in password)

    # Assess password strength
    if length >= 16 and (has_lowercase and has_uppercase) and (has_digit and has_special):
        return "Super Strong"
    elif length >= 12 and (has_lowercase and has_uppercase) and (has_digit and has_special):
        return "Strong"
    elif length >= 8 and (has_lowercase or has_uppercase) and (has_digit or has_special):
        return "Moderate"
    else:
        return "Weak"

# Ask the user for the length of the password
length = int(input("Enter the length of the password (at least 8): "))

# Call the generate_password function with the user input length
password = generate_password(length)

# Print the generated password
print("Generated Password:", password)

# Check and print the password strength
strength = check_password_strength(password)
print("Password Strength:", strength)
