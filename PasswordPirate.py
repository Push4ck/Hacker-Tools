import argparse
import itertools
import random
import string
import sys


def generate_passwords(keywords, min_length, max_length,
                       use_special_chars=False, use_numbers=False):
    """Generate unique passwords from the given keywords and options."""
    for n in range(min_length, max_length + 1):
        for keyword in keywords:
            if len(keyword) >= n:
                yield keyword[:n]
            else:
                for combination in itertools.product(keyword, repeat=n):
                    yield ''.join(combination)
    if use_special_chars or use_numbers:
        for password in generate_passwords(keywords, min_length, max_length):
            for n in range(1, len(password)):
                if use_special_chars:
                    for special_char in string.punctuation:
                        yield f"{password[:n]}{special_char}{password[n:]}"
                if use_numbers:
                    for number in string.digits:
                        yield password[:n] + number + password[n:]


def generate_password(length, use_special_chars=False, use_numbers=False):
    """Generate a random password of the given length."""
    chars = string.ascii_letters
    if use_special_chars:
        chars += string.punctuation
    if use_numbers:
        chars += string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def parse_args(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser('Generate passwords from keywords.')
    parser.add_argument('--keywords', metavar='KEYWORD', nargs='+',
                        help='keywords to use in password generation')
    parser.add_argument('--min-length', metavar='MIN LENGTH', type=int,
                        default=1,
                        help='minimum length of the password (default: 1)')
    parser.add_argument('--max-length', metavar='MAX LENGTH', type=int,
                        default=10,
                        help='maximum length of the password (default: 10)')
    parser.add_argument('--special-chars', action='store_true', default=False,
                        help='use special characters in the password')
    parser.add_argument('--numbers', action='store_true', default=False,
                        help='use numbers in the password')
    return parser.parse_args(args)


def main(args):
    """Generate passwords from command line arguments and print them to stdout."""
    opts = parse_args(args)

    # Ask user for the file path to write the passwords to
    output_file = input("Enter the file path to write the passwords to: ")

    # Write passwords to the output file
    with open(output_file, 'w') as f:
        for password in generate_passwords(opts.keywords, opts.min_length,
                                           opts.max_length,
                                           use_special_chars=opts.special_chars,
                                           use_numbers=opts.numbers):
            f.write(password + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
