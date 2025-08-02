#!/usr/bin/env python3
"""
BrutePilot - Professional Wordlist Generator
Advanced password list generation tool for security testing and research.
"""

import argparse
import itertools
import random
import string
import sys
import os
import time
from pathlib import Path


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
                os.system('color')
            except:
                for attr in dir(cls):
                    if not attr.startswith('_') and attr != 'disable_on_windows':
                        setattr(cls, attr, '')


def print_banner():
    """Display the application banner with ethical use notice"""
    Colors.disable_on_windows()
    
    banner = f"""
{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                        BrutePilot v2.0                       ║
║                Professional Wordlist Generator               ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}⚖️  ETHICAL USE ONLY: This tool is designed for authorized security testing,
   penetration testing, and educational purposes. Use responsibly and legally.{Colors.END}

{Colors.BLUE}🎯 Generate targeted wordlists from keywords and patterns
📊 Advanced mutation algorithms for comprehensive coverage
🔧 Customizable output formats and filtering options{Colors.END}
"""
    print(banner)


def print_progress_bar(current, total, width=50):
    """Display a progress bar for long operations"""
    if total == 0:
        return
    
    progress = current / total
    filled = int(width * progress)
    bar = '█' * filled + '░' * (width - filled)
    percent = progress * 100
    
    print(f'\r{Colors.CYAN}Progress: [{bar}] {percent:.1f}% ({current:,}/{total:,}){Colors.END}', end='', flush=True)


def generate_keyword_passwords(keywords, min_length, max_length, progress_callback=None):
    """Generate base passwords using keyword combinations with progress tracking."""
    passwords = []
    total_operations = len(keywords) * (max_length - min_length + 1)
    current_op = 0
    
    for keyword in keywords:
        for n in range(min_length, max_length + 1):
            if len(keyword) >= n:
                passwords.append(keyword[:n])
            else:
                # Limit combinations to prevent exponential explosion
                if n <= 6:  # Reasonable limit for combinations
                    for combo in itertools.product(keyword, repeat=n):
                        passwords.append(''.join(combo))
                        if len(passwords) % 1000 == 0 and progress_callback:
                            progress_callback(len(passwords))
            
            current_op += 1
            if progress_callback:
                progress_callback(current_op, total_operations)
    
    return passwords


def mutate_passwords(passwords, mutations, progress_callback=None):
    """Apply various mutations to base passwords."""
    mutated = set(passwords)  # Use set to avoid duplicates
    total_passwords = len(passwords)
    
    for i, pwd in enumerate(passwords):
        # Basic mutations
        if mutations.get('case_variations', False):
            mutated.add(pwd.upper())
            mutated.add(pwd.lower())
            mutated.add(pwd.capitalize())
            mutated.add(pwd.swapcase())
        
        # Character substitutions
        if mutations.get('leet_speak', False):
            leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
            leet_pwd = pwd.lower()
            for char, replacement in leet_map.items():
                leet_pwd = leet_pwd.replace(char, replacement)
            mutated.add(leet_pwd)
        
        # Number and symbol mutations
        if mutations.get('append_numbers', False):
            for num in ['1', '12', '123', '2023', '2024', '2025']:
                mutated.add(pwd + num)
                mutated.add(num + pwd)
        
        if mutations.get('append_symbols', False):
            for symbol in ['!', '@', '#', '$', '!!', '123']:
                mutated.add(pwd + symbol)
                mutated.add(symbol + pwd)
        
        # Common password patterns
        if mutations.get('common_patterns', False):
            common_endings = ['123', '!', '1!', '@123', '2024', '01']
            for ending in common_endings:
                mutated.add(pwd + ending)
        
        if progress_callback and i % 100 == 0:
            progress_callback(i, total_passwords)
    
    return list(mutated)


def apply_filters(passwords, filters):
    """Apply various filters to the password list."""
    filtered = passwords
    
    if filters.get('min_length'):
        filtered = [p for p in filtered if len(p) >= filters['min_length']]
    
    if filters.get('max_length'):
        filtered = [p for p in filtered if len(p) <= filters['max_length']]
    
    if filters.get('require_numbers', False):
        filtered = [p for p in filtered if any(c.isdigit() for c in p)]
    
    if filters.get('require_symbols', False):
        filtered = [p for p in filtered if any(c in string.punctuation for c in p)]
    
    if filters.get('require_mixed_case', False):
        filtered = [p for p in filtered if any(c.islower() for c in p) and any(c.isupper() for c in p)]
    
    return filtered


def generate_random_passwords(count, length, char_sets):
    """Generate multiple random passwords."""
    chars = ''
    if char_sets.get('lowercase', True):
        chars += string.ascii_lowercase
    if char_sets.get('uppercase', False):
        chars += string.ascii_uppercase
    if char_sets.get('numbers', False):
        chars += string.digits
    if char_sets.get('symbols', False):
        chars += string.punctuation
    
    if not chars:
        chars = string.ascii_lowercase  # Fallback
    
    passwords = []
    for _ in range(count):
        password = ''.join(random.choice(chars) for _ in range(length))
        passwords.append(password)
    
    return passwords


def save_wordlist(passwords, output_file, format_type='txt'):
    """Save the wordlist to file with specified format."""
    output_path = Path(output_file)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if format_type == 'txt':
                for pwd in passwords:
                    f.write(pwd + '\n')
            elif format_type == 'csv':
                f.write('password,length,has_numbers,has_symbols\n')
                for pwd in passwords:
                    has_nums = any(c.isdigit() for c in pwd)
                    has_syms = any(c in string.punctuation for c in pwd)
                    f.write(f'"{pwd}",{len(pwd)},{has_nums},{has_syms}\n')
        
        return True
    except Exception as e:
        print(f"{Colors.RED}❌ Error saving file: {e}{Colors.END}")
        return False


def display_statistics(passwords, generation_time):
    """Display comprehensive statistics about the generated wordlist."""
    if not passwords:
        return
    
    total_count = len(passwords)
    unique_count = len(set(passwords))
    avg_length = sum(len(p) for p in passwords) / total_count
    min_length = min(len(p) for p in passwords)
    max_length = max(len(p) for p in passwords)
    
    has_numbers = sum(1 for p in passwords if any(c.isdigit() for c in p))
    has_symbols = sum(1 for p in passwords if any(c in string.punctuation for c in p))
    has_mixed_case = sum(1 for p in passwords if any(c.islower() for c in p) and any(c.isupper() for c in p))
    
    print(f"\n{Colors.BOLD}📊 Wordlist Statistics{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 40}{Colors.END}")
    print(f"Total passwords:     {Colors.CYAN}{total_count:,}{Colors.END}")
    print(f"Unique passwords:    {Colors.CYAN}{unique_count:,}{Colors.END}")
    print(f"Duplicate rate:      {Colors.YELLOW}{((total_count-unique_count)/total_count*100):.1f}%{Colors.END}")
    print(f"Average length:      {Colors.CYAN}{avg_length:.1f}{Colors.END}")
    print(f"Length range:        {Colors.CYAN}{min_length} - {max_length}{Colors.END}")
    print(f"Generation time:     {Colors.GREEN}{generation_time:.2f}s{Colors.END}")
    
    print(f"\n{Colors.BOLD}🔍 Complexity Analysis{Colors.END}")
    print(f"{Colors.BOLD}{'─' * 40}{Colors.END}")
    print(f"With numbers:        {Colors.CYAN}{has_numbers:,}{Colors.END} ({has_numbers/total_count*100:.1f}%)")
    print(f"With symbols:        {Colors.CYAN}{has_symbols:,}{Colors.END} ({has_symbols/total_count*100:.1f}%)")
    print(f"Mixed case:          {Colors.CYAN}{has_mixed_case:,}{Colors.END} ({has_mixed_case/total_count*100:.1f}%)")


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='brutepilot',
        description='🧨 BrutePilot - Professional Wordlist Generator',
        epilog=f"""
{Colors.BOLD}Generation Modes:{Colors.END}
  {Colors.CYAN}brutepilot --keywords admin user --output wordlist.txt{Colors.END}
  {Colors.CYAN}brutepilot --random --count 1000 --length 8 --output random.txt{Colors.END}
  {Colors.CYAN}brutepilot --keywords company --mutations all --output advanced.txt{Colors.END}

{Colors.BOLD}Advanced Usage:{Colors.END}
  {Colors.CYAN}brutepilot --keywords password admin --min-length 6 --max-length 12 \\{Colors.END}
  {Colors.CYAN}         --mutations case,leet,numbers --filter-min-length 8 \\{Colors.END}
  {Colors.CYAN}         --output secure_wordlist.txt --format csv{Colors.END}

{Colors.YELLOW}⚠️  Remember: Use this tool responsibly and only for authorized testing!{Colors.END}
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Generation modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--keywords', 
        nargs='+', 
        help='Keywords to use for password generation'
    )
    mode_group.add_argument(
        '--random', 
        action='store_true', 
        help='Generate random passwords instead'
    )
    
    # Keyword-based generation options
    parser.add_argument(
        '--min-length', 
        type=int, 
        default=4, 
        help='Minimum password length (default: 4)'
    )
    parser.add_argument(
        '--max-length', 
        type=int, 
        default=8, 
        help='Maximum password length (default: 8)'
    )
    
    # Random generation options
    parser.add_argument(
        '--count', 
        type=int, 
        default=1000, 
        help='Number of random passwords to generate (default: 1000)'
    )
    parser.add_argument(
        '--length', 
        type=int, 
        help='Length of random passwords'
    )
    
    # Mutation options
    parser.add_argument(
        '--mutations', 
        choices=['case', 'leet', 'numbers', 'symbols', 'patterns', 'all'], 
        nargs='+',
        help='Mutation types to apply'
    )
    
    # Filtering options
    parser.add_argument(
        '--filter-min-length', 
        type=int, 
        help='Filter: minimum password length'
    )
    parser.add_argument(
        '--filter-max-length', 
        type=int, 
        help='Filter: maximum password length'
    )
    parser.add_argument(
        '--require-numbers', 
        action='store_true', 
        help='Filter: require passwords to contain numbers'
    )
    parser.add_argument(
        '--require-symbols', 
        action='store_true', 
        help='Filter: require passwords to contain symbols'
    )
    parser.add_argument(
        '--require-mixed-case', 
        action='store_true', 
        help='Filter: require passwords to have mixed case'
    )
    
    # Output options
    parser.add_argument(
        '--output', 
        type=str, 
        required=True, 
        help='Output file path'
    )
    parser.add_argument(
        '--format', 
        choices=['txt', 'csv'], 
        default='txt', 
        help='Output format (default: txt)'
    )
    parser.add_argument(
        '--quiet', 
        action='store_true', 
        help='Suppress progress output'
    )
    parser.add_argument(
        '--max-passwords', 
        type=int, 
        default=1000000, 
        help='Maximum number of passwords to generate (safety limit)'
    )
    
    # Version
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'{Colors.CYAN}BrutePilot v2.0{Colors.END} - Professional Wordlist Generator'
    )
    
    return parser


def main():
    """Main application entry point."""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Display banner unless in quiet mode
        if not args.quiet:
            print_banner()
        
        start_time = time.time()
        passwords = []
        
        # Validate arguments
        if args.random and not args.length:
            print(f"{Colors.RED}❌ Error: --length is required when using --random{Colors.END}")
            sys.exit(1)
        
        if args.min_length > args.max_length:
            print(f"{Colors.RED}❌ Error: min-length cannot be greater than max-length{Colors.END}")
            sys.exit(1)
        
        # Generate passwords
        if args.random:
            if not args.quiet:
                print(f"\n{Colors.BLUE}🎲 Generating {args.count:,} random passwords of length {args.length}...{Colors.END}")
            
            char_sets = {
                'lowercase': True,
                'uppercase': True,
                'numbers': True,
                'symbols': args.mutations and 'symbols' in args.mutations
            }
            passwords = generate_random_passwords(args.count, args.length, char_sets)
        
        else:
            if not args.quiet:
                print(f"\n{Colors.BLUE}🔧 Generating wordlist from keywords: {', '.join(args.keywords)}{Colors.END}")
            
            # Progress callback for keyword generation
            def progress_update(current, total=None):
                if not args.quiet and total:
                    print_progress_bar(current, total)
            
            # Generate base passwords
            passwords = generate_keyword_passwords(
                args.keywords, 
                args.min_length, 
                args.max_length,
                progress_callback=progress_update if not args.quiet else None
            )
            
            if not args.quiet:
                print(f"\n{Colors.GREEN}✅ Generated {len(passwords):,} base passwords{Colors.END}")
            
            # Apply mutations if specified
            if args.mutations:
                if not args.quiet:
                    print(f"{Colors.BLUE}🧬 Applying mutations: {', '.join(args.mutations)}{Colors.END}")
                
                mutation_config = {}
                if 'case' in args.mutations or 'all' in args.mutations:
                    mutation_config['case_variations'] = True
                if 'leet' in args.mutations or 'all' in args.mutations:
                    mutation_config['leet_speak'] = True
                if 'numbers' in args.mutations or 'all' in args.mutations:
                    mutation_config['append_numbers'] = True
                if 'symbols' in args.mutations or 'all' in args.mutations:
                    mutation_config['append_symbols'] = True
                if 'patterns' in args.mutations or 'all' in args.mutations:
                    mutation_config['common_patterns'] = True
                
                passwords = mutate_passwords(
                    passwords, 
                    mutation_config,
                    progress_callback=progress_update if not args.quiet else None
                )
                
                if not args.quiet:
                    print(f"\n{Colors.GREEN}✅ Applied mutations, total: {len(passwords):,} passwords{Colors.END}")
        
        # Apply filters
        filter_config = {}
        if args.filter_min_length:
            filter_config['min_length'] = args.filter_min_length
        if args.filter_max_length:
            filter_config['max_length'] = args.filter_max_length
        if args.require_numbers:
            filter_config['require_numbers'] = True
        if args.require_symbols:
            filter_config['require_symbols'] = True
        if args.require_mixed_case:
            filter_config['require_mixed_case'] = True
        
        if filter_config:
            original_count = len(passwords)
            passwords = apply_filters(passwords, filter_config)
            if not args.quiet:
                print(f"{Colors.YELLOW}🔍 Applied filters: {original_count:,} → {len(passwords):,} passwords{Colors.END}")
        
        # Safety check
        if len(passwords) > args.max_passwords:
            if not args.quiet:
                print(f"{Colors.YELLOW}⚠️ Limiting output to {args.max_passwords:,} passwords for safety{Colors.END}")
            passwords = passwords[:args.max_passwords]
        
        # Save wordlist
        if not args.quiet:
            print(f"{Colors.BLUE}💾 Saving wordlist to {args.output}...{Colors.END}")
        
        success = save_wordlist(passwords, args.output, args.format)
        
        if success:
            generation_time = time.time() - start_time
            
            if not args.quiet:
                print(f"{Colors.GREEN}✅ Successfully saved {len(passwords):,} passwords to {args.output}{Colors.END}")
                display_statistics(passwords, generation_time)
            else:
                print(f"Generated {len(passwords):,} passwords in {generation_time:.2f}s")
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()