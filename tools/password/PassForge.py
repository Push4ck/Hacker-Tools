#!/usr/bin/env python3
"""
PassForge - Professional Password Generator
A secure and reliable password generation tool with strength analysis.
"""

import random
import string
import argparse
import sys
import os


# Color codes for cross-platform terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable_on_windows(cls):
        """Disable colors on Windows if not supported"""
        if os.name == 'nt':
            try:
                # Enable ANSI colors on Windows 10+
                os.system('color')
            except:
                # Fallback: disable colors
                for attr in dir(cls):
                    if not attr.startswith('_') and attr != 'disable_on_windows':
                        setattr(cls, attr, '')


def print_banner():
    """Display the application banner"""
    Colors.disable_on_windows()
    
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                         PassForge v1.0                       ║
║                  Professional Password Generator             ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BLUE}🔐 Generate secure passwords with customizable length and complexity
📊 Real-time password strength analysis and security recommendations{Colors.END}
"""
    print(banner)


def generate_password(length, include_symbols=True, exclude_ambiguous=False):
    """Generate a secure password of specified length with required complexity."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?" if include_symbols else ""
    
    # Remove ambiguous characters if requested
    if exclude_ambiguous:
        ambiguous = "0O1lI"
        lowercase = ''.join(c for c in lowercase if c not in ambiguous)
        uppercase = ''.join(c for c in uppercase if c not in ambiguous)
        digits = ''.join(c for c in digits if c not in ambiguous)

    # Ensure at least one character from each required type
    required_chars = []
    if length >= 8:  # Only enforce complexity for longer passwords
        required_chars = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits)
        ]
        if include_symbols and symbols:
            required_chars.append(random.choice(symbols))

    # Build character pool
    all_chars = lowercase + uppercase + digits + symbols
    if not all_chars:
        raise ValueError("No valid characters available for password generation")

    # Generate remaining characters
    remaining_length = max(0, length - len(required_chars))
    additional_chars = [random.choice(all_chars) for _ in range(remaining_length)]

    # Combine and shuffle
    password_chars = required_chars + additional_chars
    random.shuffle(password_chars)
    
    return ''.join(password_chars)


def check_password_strength(password):
    """Assess the strength of a given password with detailed analysis."""
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)
    
    # Calculate score
    score = 0
    criteria = []
    
    if length >= 12:
        score += 2
        criteria.append("✓ Good length")
    elif length >= 8:
        score += 1
        criteria.append("○ Adequate length")
    else:
        criteria.append("✗ Too short")
    
    if has_lower:
        score += 1
        criteria.append("✓ Lowercase letters")
    else:
        criteria.append("✗ Missing lowercase")
        
    if has_upper:
        score += 1
        criteria.append("✓ Uppercase letters")
    else:
        criteria.append("✗ Missing uppercase")
        
    if has_digit:
        score += 1
        criteria.append("✓ Numbers")
    else:
        criteria.append("✗ Missing numbers")
        
    if has_special:
        score += 1
        criteria.append("✓ Special characters")
    else:
        criteria.append("✗ Missing symbols")

    # Determine strength level
    if score >= 6:
        strength = f"{Colors.GREEN}🔒 Excellent{Colors.END}"
        color = Colors.GREEN
    elif score >= 4:
        strength = f"{Colors.CYAN}🛡️ Strong{Colors.END}"
        color = Colors.CYAN
    elif score >= 3:
        strength = f"{Colors.YELLOW}🧩 Moderate{Colors.END}"
        color = Colors.YELLOW
    else:
        strength = f"{Colors.RED}⚠️ Weak{Colors.END}"
        color = Colors.RED

    return strength, criteria, color


def display_results(password, length, include_symbols, exclude_ambiguous):
    """Display the generated password and analysis in a formatted way."""
    print(f"\n{Colors.BOLD}📋 Password Generation Results{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 50}{Colors.END}")
    
    # Password display
    print(f"\n{Colors.BOLD}Generated Password:{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{password}{Colors.END}")
    
    # Password analysis
    strength, criteria, strength_color = check_password_strength(password)
    print(f"\n{Colors.BOLD}Security Analysis:{Colors.END}")
    print(f"Strength Level: {strength}")
    print(f"Character Count: {Colors.BOLD}{len(password)}{Colors.END}")
    
    # Configuration used
    print(f"\n{Colors.BOLD}Generation Settings:{Colors.END}")
    print(f"• Length: {length}")
    print(f"• Symbols: {'Included' if include_symbols else 'Excluded'}")
    print(f"• Ambiguous chars: {'Excluded' if exclude_ambiguous else 'Included'}")
    
    # Security criteria
    print(f"\n{Colors.BOLD}Security Criteria:{Colors.END}")
    for criterion in criteria:
        if "✓" in criterion:
            print(f"{Colors.GREEN}{criterion}{Colors.END}")
        elif "○" in criterion:
            print(f"{Colors.YELLOW}{criterion}{Colors.END}")
        else:
            print(f"{Colors.RED}{criterion}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{'─' * 50}{Colors.END}")


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='passforge',
        description='🔐 PassForge - Professional Password Generator',
        epilog=f"""
Examples:
  {Colors.CYAN}passforge --length 16{Colors.END}                    Generate a 16-character password
  {Colors.CYAN}passforge -l 12 --no-symbols{Colors.END}            Generate without special characters
  {Colors.CYAN}passforge -l 20 --exclude-ambiguous{Colors.END}     Exclude confusing characters (0, O, 1, l, I)
  {Colors.CYAN}passforge -l 14 --batch 5{Colors.END}               Generate 5 passwords at once

{Colors.YELLOW}💡 Tip: For maximum security, use passwords with 16+ characters including symbols.{Colors.END}
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '-l', '--length',
        type=int,
        required=True,
        metavar='N',
        help='Password length (minimum: 4, recommended: 16+)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Exclude special characters from password'
    )
    
    parser.add_argument(
        '--exclude-ambiguous',
        action='store_true',
        help='Exclude ambiguous characters (0, O, 1, l, I)'
    )
    
    parser.add_argument(
        '--batch',
        type=int,
        default=1,
        metavar='N',
        help='Generate multiple passwords (default: 1)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Output only the password(s) without formatting'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'{Colors.CYAN}PassForge v1.0{Colors.END} - Professional Password Generator'
    )
    
    return parser


def main():
    """Main application entry point."""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Validate arguments
        if args.length < 4:
            print(f"{Colors.RED}❌ Error: Password length must be at least 4 characters{Colors.END}")
            sys.exit(1)
            
        if args.batch < 1 or args.batch > 100:
            print(f"{Colors.RED}❌ Error: Batch count must be between 1 and 100{Colors.END}")
            sys.exit(1)
        
        # Display banner unless in quiet mode
        if not args.quiet:
            print_banner()
        
        # Generate password(s)
        include_symbols = not args.no_symbols
        
        if args.batch == 1:
            # Single password generation
            password = generate_password(
                args.length, 
                include_symbols=include_symbols,
                exclude_ambiguous=args.exclude_ambiguous
            )
            
            if args.quiet:
                print(password)
            else:
                display_results(password, args.length, include_symbols, args.exclude_ambiguous)
        else:
            # Batch password generation
            if args.quiet:
                for _ in range(args.batch):
                    password = generate_password(
                        args.length,
                        include_symbols=include_symbols,
                        exclude_ambiguous=args.exclude_ambiguous
                    )
                    print(password)
            else:
                print(f"\n{Colors.BOLD}🔄 Generating {args.batch} passwords...{Colors.END}\n")
                for i in range(args.batch):
                    password = generate_password(
                        args.length,
                        include_symbols=include_symbols,
                        exclude_ambiguous=args.exclude_ambiguous
                    )
                    strength, _, color = check_password_strength(password)
                    print(f"{Colors.BOLD}{i+1:2d}.{Colors.END} {Colors.CYAN}{password}{Colors.END} [{strength}]")
                print(f"\n{Colors.GREEN}✅ Successfully generated {args.batch} secure passwords{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()