import argparse
import itertools
import random
import string
import sys


def generate_keyword_passwords(keywords, min_length, max_length):
    """Generate base passwords using keyword combinations."""
    for keyword in keywords:
        for n in range(min_length, max_length + 1):
            if len(keyword) >= n:
                yield keyword[:n]
            else:
                for combo in itertools.product(keyword, repeat=n):
                    yield ''.join(combo)


def mutate_passwords(passwords, use_special_chars, use_numbers):
    """Mutate passwords with special characters and/or numbers."""
    for pwd in passwords:
        yield pwd  # base password
        for i in range(1, len(pwd)):
            if use_special_chars:
                for c in string.punctuation:
                    yield pwd[:i] + c + pwd[i:]
            if use_numbers:
                for d in string.digits:
                    yield pwd[:i] + d + pwd[i:]


def generate_random_password(length, use_special_chars=False, use_numbers=False):
    """Generate one random password of specified length."""
    chars = string.ascii_letters
    if use_special_chars:
        chars += string.punctuation
    if use_numbers:
        chars += string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def parse_args():
    parser = argparse.ArgumentParser(description='Password Generator Tool')
    parser.add_argument('--keywords', nargs='+', help='Keywords to use for password generation')
    parser.add_argument('--min-length', type=int, default=4, help='Minimum password length')
    parser.add_argument('--max-length', type=int, default=8, help='Maximum password length')
    parser.add_argument('--special-chars', action='store_true', help='Include special characters')
    parser.add_argument('--numbers', action='store_true', help='Include numbers')
    parser.add_argument('--random', action='store_true', help='Generate a random password instead')
    parser.add_argument('--length', type=int, help='Length of random password (required if --random)')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    return parser.parse_args()


def main():
    opts = parse_args()

    with open(opts.output, 'w') as f:
        if opts.random:
            if not opts.length:
                print("Error: --length is required when using --random")
                sys.exit(1)
            password = generate_random_password(opts.length, opts.special_chars, opts.numbers)
            f.write(password + '\n')
        else:
            if not opts.keywords:
                print("Error: --keywords is required unless --random is specified")
                sys.exit(1)
            base_passwords = generate_keyword_passwords(opts.keywords, opts.min_length, opts.max_length)
            final_passwords = mutate_passwords(base_passwords, opts.special_chars, opts.numbers)
            for pwd in final_passwords:
                f.write(pwd + '\n')


if __name__ == '__main__':
    main()