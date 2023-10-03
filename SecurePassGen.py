import random
import string

# Define the generate_password function
def generate_password(length):
    # Check if the length is less than 8 characters
    if length < 8:
        raise ValueError("Password length should be at least 8 characters")

    # Define character sets
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digits_chars = string.digits
    special_chars = "!@#$%^&*"

    # Create a password by selecting one character from each character set
    password = (
        random.choice(lowercase_chars)
        + random.choice(uppercase_chars)
        + random.choice(digits_chars)
        + random.choice(special_chars)
    )

    # Combine the character sets
    password_chars = lowercase_chars + uppercase_chars + digits_chars + special_chars

    # Choose random characters to complete the password
    password += ''.join(random.choice(password_chars) for i in range(length - 4))

    return password

# Define a function to check password strength
def check_password_strength(password):
    length = len(password)
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*" for char in password)

    # Assess password strength based on length and character set criteria
    if length >= 16 and (has_lowercase and has_uppercase) and (has_digit and has_special):
        return "Super Strong"
    elif length >= 12 and (has_lowercase and has_uppercase) and (has_digit and has_special):
        return "Strong"
    elif length >= 8 and (has_lowercase or has_uppercase) and (has_digit or has_special):
        return "Moderate"
    else:
        return "Weak"

while True:
    try:
        # Ask the user for the length of the password
        length = int(input("Enter the length of the password (at least 8): "))

        # Generate a password
        password = generate_password(length)
        
        # Print the generated password
        print("Generated Password:", password)

        # Check and print the password strength
        strength = check_password_strength(password)
        print("Password Strength:", strength)
        
        # Exit the loop if password generation is successful
        break
    except ValueError as e:
        # Handle invalid input with an error message
        print(f"Error: {e}. Please enter a valid password length.")
