import random
import string
import argparse


def generate_password(length):
    if length < 8:
        raise ValueError("Password length must be at least 8.")

    # Guarantee at least one of each type
    chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]

    # Fill the rest
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    chars += [random.choice(all_chars) for _ in range(length - 4)]

    # Shuffle to avoid predictable placement
    random.shuffle(chars)
    return ''.join(chars)


def check_password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)

    if length >= 16 and all([has_lower, has_upper, has_digit, has_special]):
        return "Super Strong"
    elif length >= 12 and all([has_lower, has_upper, has_digit, has_special]):
        return "Strong"
    elif length >= 8 and any([has_lower, has_upper]) and any([has_digit, has_special]):
        return "Moderate"
    else:
        return "Weak"


def main():
    parser = argparse.ArgumentParser(description="Password Generator & Strength Checker")
    parser.add_argument('--length', type=int, required=True, help='Length of the password (min: 8)')
    args = parser.parse_args()

    try:
        pwd = generate_password(args.length)
        print("Generated Password:", pwd)
        print("Password Strength:", check_password_strength(pwd))
    except ValueError as e:
        print("Error:", e)


if __name__ == '__main__':
    main()