def password_generator():
    # Ask the user for words to use in password generation
    words_input = input("Enter a list of words separated by comma: ")
    if words_input.strip() == "":
        raise Exception("Input cannot be empty")
    words = [word.strip() for word in words_input.split(",")]

    # List of special characters
    special_chars = ["!", "@", "#", "$", "%", "^", "&", "*"]

    # Maximum length of the password
    max_length = input("Enter the maximum length of the password: ")
    try:
        max_length = int(max_length)
    except ValueError:
        raise Exception("Max length should be a positive integer")
    if max_length <= 0:
        raise Exception("Max length should be a positive integer")

    # List to store the generated passwords
    passwords = []

    # Check if the input words contain only alphanumeric characters
    for word in words:
        if not word.isalnum():
            raise Exception("The word should contain only alphanumeric characters")

    # Loop through the words
    for word in words:
        # Append the word as is to the list
        passwords.append(word)

        # Loop through the special characters
        for char in special_chars:
            # Add the special character to the beginning and end of the word
            passwords.append(char + word)
            passwords.append(word + char)

            # Add the special character to the middle of the word
            mid = int(len(word) / 2)
            if len(word) % 2 == 0:
                mid -= 1
            passwords.append(word[:mid] + char + word[mid:])

        # Loop through the length of the password
        for length in range(2, max_length + 1):
            # Repeat the word to create a new password with the given length
            new_password = word * length
            passwords.append(new_password)

    # Remove duplicates from the list of passwords
    passwords = list(set(passwords))

    # Print the generated passwords
    print(passwords)

password_generator()
