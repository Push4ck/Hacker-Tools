words = ["password", "123456", "qwerty", "letmein", "monkey", "dragon", "trustno1"]

special_chars = ["!", "@", "#", "$", "%", "^", "&", "*"]

max_length = 8

passwords = []

for word in words:
    passwords.append(word)

    for char in special_chars:
        passwords.append(char + word)
        passwords.append(word + char)
        passwords.append(word[:int(len(word) / 2)] + char + word[int(len(word) / 2):])

    for length in range(2, max_length + 1):
        new_password = word * length
        passwords.append(new_password)

print(passwords)