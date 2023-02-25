def caesar_encoder(plain_text, shift):
    encoded_text = ""
    for letter in plain_text:
        if not letter.isalpha():
            # Non-alphabetic characters are included as-is in the encoded text
            encoded_text += letter
            continue

        # Determine the position of the letter in the alphabet (0-25)
        position = ord(letter.lower()) - ord('a')

        # Shift the position by the specified amount
        new_position = (position + shift) % 26

        # Convert the new position back to a letter
        encoded_letter = chr(new_position + ord('a'))

        # Use the original case of the letter
        if letter.isupper():
            encoded_letter = encoded_letter.upper()

        encoded_text += encoded_letter

    return encoded_text


def caesar_decoder(cipher_text, shift):
    decoded_text = ""
    for letter in cipher_text:
        if not letter.isalpha():
            # Non-alphabetic characters are included as-is in the decoded text
            decoded_text += letter
            continue

        # Determine the position of the letter in the alphabet (0-25)
        position = ord(letter.lower()) - ord('a')

        # Shift the position by the specified amount
        new_position = (position - shift) % 26

        # Convert the new position back to a letter
        decoded_letter = chr(new_position + ord('a'))

        # Use the original case of the letter
        if letter.isupper():
            decoded_letter = decoded_letter.upper()

        decoded_text += decoded_letter

    return decoded_text


# Ask the user whether to encode plain text or decode a Caesar cipher
choice = input("Enter 'e' to encode plain text or 'd' to decode a Caesar cipher: ")

if choice == 'e':
    # Ask the user for a message to encode
    plain_text = input("Enter a message to encode: ")

    # Ask the user for a shift value
    shift = int(input("Enter the number of positions to shift the letters: "))

    # Encode the message using the Caesar Cipher
    cipher_text = caesar_encoder(plain_text, shift)
    print("Encoded message:", cipher_text)

elif choice == 'd':
    # Ask the user for a message to decode
    cipher_text = input("Enter a message to decode: ")

    # Ask the user for a shift value
    shift = int(input("Enter the number of positions the letters were shifted: "))

    # Decode the message using the Caesar Cipher
    decoded_text = caesar_decoder(cipher_text, shift)
    print("Decoded message:", decoded_text)

else:
    print("Invalid choice. Please enter 'e' to encode plain text or 'd' to decode a Caesar cipher.")
