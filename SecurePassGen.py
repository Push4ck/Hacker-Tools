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

# Call the function to generate a password with length 16
password = generate_password(16)

# Print the generated password
print(password)
