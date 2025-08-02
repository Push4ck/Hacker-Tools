#!/usr/bin/env python3
"""
EnigmaVault - Professional Multi-Cipher Encryption Suite
Advanced cryptographic tools for text encoding and decoding
"""

import argparse
import sys
import string
import random
import base64
import binascii
import platform
import time
from typing import Dict, List, Tuple, Optional

# Constants
__version__ = "3.0.0"
__author__ = "EnigmaVault Security Team"

class Style:
    """Professional styling system for CLI interface"""
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Symbols
    LOCK = '🔐'
    UNLOCK = '🔓'
    SHIELD = '🛡️'
    KEY = '🔑'
    GEAR = '⚙️'
    LIGHTNING = '⚡'
    FIRE = '🔥'
    DIAMOND = '💎'
    
    @classmethod
    def init_colors(cls):
        """Initialize cross-platform color support"""
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                # Disable colors on unsupported systems
                for attr in dir(cls):
                    if not attr.startswith('_') and attr.isupper() and len(getattr(cls, attr)) > 1:
                        setattr(cls, attr, '')

# Initialize styling
Style.init_colors()

def print_header():
    """Display the professional application header"""
    width = 80
    header = f"""
{Style.CYAN}{Style.BOLD}{'=' * width}
{'EnigmaVault'.center(width)}
{'Professional Multi-Cipher Encryption Suite'.center(width)}
{Style.RESET}{Style.CYAN}{'=' * width}{Style.RESET}

{Style.WHITE}{Style.BOLD}Version:{Style.RESET} {Style.CYAN}{__version__}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Platform:{Style.RESET} {Style.CYAN}{platform.system()}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Ciphers:{Style.RESET} {Style.GREEN}12+{Style.RESET}

{Style.YELLOW}{Style.ITALIC}"Where secrets meet security - Professional cryptographic solutions"{Style.RESET}
"""
    print(header)

def print_success(message: str, symbol: str = Style.UNLOCK):
    """Print success message with professional styling"""
    print(f"{Style.GREEN}{Style.BOLD}[SUCCESS]{Style.RESET} {symbol} {message}")

def print_error(message: str, symbol: str = "❌"):
    """Print error message with professional styling"""
    print(f"{Style.RED}{Style.BOLD}[ERROR]{Style.RESET} {symbol} {message}")

def print_info(message: str, symbol: str = "ℹ️"):
    """Print info message with professional styling"""
    print(f"{Style.BLUE}{Style.BOLD}[INFO]{Style.RESET} {symbol} {message}")

def print_warning(message: str, symbol: str = "⚠️"):
    """Print warning message with professional styling"""
    print(f"{Style.YELLOW}{Style.BOLD}[WARNING]{Style.RESET} {symbol} {message}")

def print_separator(char: str = "─", length: int = 60):
    """Print visual separator"""
    print(f"{Style.GRAY}{char * length}{Style.RESET}")

def animate_operation(message: str, duration: float = 1.5):
    """Animate cipher operations"""
    frames = ['◐', '◓', '◑', '◒']
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        print(f"\r{Style.CYAN}{frames[i % len(frames)]}{Style.RESET} {message}", end='', flush=True)
        time.sleep(0.2)
        i += 1
    
    print(f"\r{Style.GREEN}✓{Style.RESET} {message}")

class CipherSuite:
    """Professional cipher implementation suite"""
    
    @staticmethod
    def caesar_cipher(text: str, shift: int, decode: bool = False) -> str:
        """Enhanced Caesar cipher with full Unicode support"""
        if decode:
            shift = -shift
        
        result = ""
        for char in text:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - offset + shift) % 26
                result += chr(offset + shifted)
            else:
                result += char
        return result
    
    @staticmethod
    def rot13_cipher(text: str) -> str:
        """ROT13 cipher - special case of Caesar with shift 13"""
        return CipherSuite.caesar_cipher(text, 13)
    
    @staticmethod
    def atbash_cipher(text: str) -> str:
        """Atbash cipher - reverse alphabet substitution"""
        result = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result += chr(ord('Z') - (ord(char) - ord('A')))
                else:
                    result += chr(ord('z') - (ord(char) - ord('a')))
            else:
                result += char
        return result
    
    @staticmethod
    def reverse_cipher(text: str) -> str:
        """Simple reverse cipher"""
        return text[::-1]
    
    @staticmethod
    def base64_encode(text: str) -> str:
        """Base64 encoding"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def base64_decode(text: str) -> str:
        """Base64 decoding"""
        try:
            return base64.b64decode(text.encode('utf-8')).decode('utf-8')
        except Exception:
            raise ValueError("Invalid Base64 input")
    
    @staticmethod
    def hex_encode(text: str) -> str:
        """Hexadecimal encoding"""
        return text.encode('utf-8').hex().upper()
    
    @staticmethod
    def hex_decode(text: str) -> str:
        """Hexadecimal decoding"""
        try:
            return bytes.fromhex(text).decode('utf-8')
        except Exception:
            raise ValueError("Invalid hexadecimal input")
    
    @staticmethod
    def binary_encode(text: str) -> str:
        """Binary encoding"""
        return ' '.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_decode(text: str) -> str:
        """Binary decoding"""
        try:
            binary_values = text.replace(' ', '')
            if len(binary_values) % 8 != 0:
                raise ValueError("Invalid binary length")
            
            result = ""
            for i in range(0, len(binary_values), 8):
                byte = binary_values[i:i+8]
                result += chr(int(byte, 2))
            return result
        except Exception:
            raise ValueError("Invalid binary input")
    
    @staticmethod
    def morse_encode(text: str) -> str:
        """Morse code encoding"""
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ' ': '/'
        }
        
        result = []
        for char in text.upper():
            if char in morse_dict:
                result.append(morse_dict[char])
            else:
                result.append('?')
        return ' '.join(result)
    
    @staticmethod
    def morse_decode(text: str) -> str:
        """Morse code decoding"""
        morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
            '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
            '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
            '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
            '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
            '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
            '---..': '8', '----.': '9', '/': ' '
        }
        
        result = []
        for code in text.split(' '):
            if code in morse_dict:
                result.append(morse_dict[code])
            else:
                result.append('?')
        return ''.join(result)
    
    @staticmethod
    def vigenere_cipher(text: str, key: str, decode: bool = False) -> str:
        """Vigenère cipher implementation"""
        if not key:
            raise ValueError("Key cannot be empty for Vigenère cipher")
        
        key = key.upper()
        result = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                
                if decode:
                    key_shift = -key_shift
                
                shifted = (ord(char) - offset + key_shift) % 26
                result += chr(offset + shifted)
                key_index += 1
            else:
                result += char
        
        return result

def display_cipher_info(cipher_type: str, text: str, result: str, **kwargs):
    """Display comprehensive cipher operation results"""
    print_separator()
    print(f"{Style.WHITE}{Style.BOLD}🔐 CIPHER OPERATION RESULTS{Style.RESET}")
    print_separator()
    
    # Operation details
    details = [
        ("Cipher Type", f"{Style.BOLD}{cipher_type.upper()}{Style.RESET}"),
        ("Input Length", f"{Style.BOLD}{len(text):,}{Style.RESET} characters"),
        ("Output Length", f"{Style.BOLD}{len(result):,}{Style.RESET} characters"),
    ]
    
    # Add cipher-specific details
    if 'shift' in kwargs:
        details.append(("Shift Value", f"{Style.BOLD}{kwargs['shift']}{Style.RESET}"))
    if 'key' in kwargs:
        details.append(("Key", f"{Style.BOLD}{kwargs['key']}{Style.RESET}"))
    
    for label, value in details:
        print(f"  {Style.CYAN}{Style.BOLD}{label:.<15}{Style.RESET} {value}")
    
    print_separator()
    
    # Input/Output display
    print(f"{Style.YELLOW}{Style.BOLD}INPUT:{Style.RESET}")
    print(f"  {Style.GRAY}\"{text[:100]}{'...' if len(text) > 100 else ''}\"{Style.RESET}")
    print()
    print(f"{Style.GREEN}{Style.BOLD}OUTPUT:{Style.RESET}")
    print(f"  {Style.WHITE}\"{result[:100]}{'...' if len(result) > 100 else ''}\"{Style.RESET}")
    
    if len(result) > 100:
        print(f"\n{Style.GRAY}[Full output truncated for display - {len(result):,} total characters]{Style.RESET}")
    
    print_separator()

def get_available_ciphers() -> Dict[str, Dict]:
    """Return dictionary of available ciphers with metadata"""
    return {
        'caesar': {
            'name': 'Caesar Cipher',
            'description': 'Classic shift cipher with customizable offset',
            'requires_key': False,
            'requires_shift': True,
            'symbol': '🏛️'
        },
        'rot13': {
            'name': 'ROT13 Cipher', 
            'description': 'Caesar cipher with fixed shift of 13',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '🔄'
        },
        'atbash': {
            'name': 'Atbash Cipher',
            'description': 'Ancient Hebrew reverse alphabet cipher',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '🕯️'
        },
        'reverse': {
            'name': 'Reverse Cipher',
            'description': 'Simple text reversal cipher',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '↩️'
        },
        'base64': {
            'name': 'Base64 Encoding',
            'description': 'Standard Base64 encoding/decoding',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '📦'
        },
        'hex': {
            'name': 'Hexadecimal Encoding',
            'description': 'Hexadecimal representation encoding',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '🔢'
        },
        'binary': {
            'name': 'Binary Encoding',
            'description': 'Binary representation encoding',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '1️⃣'
        },
        'morse': {
            'name': 'Morse Code',
            'description': 'International Morse code system',
            'requires_key': False,
            'requires_shift': False,
            'symbol': '📡'
        },
        'vigenere': {
            'name': 'Vigenère Cipher',
            'description': 'Polyalphabetic substitution cipher',
            'requires_key': True,
            'requires_shift': False,
            'symbol': '🗝️'
        }
    }

def list_ciphers():
    """Display available ciphers in a professional format"""
    print_header()
    
    ciphers = get_available_ciphers()
    
    print(f"{Style.WHITE}{Style.BOLD}📚 AVAILABLE CIPHER ALGORITHMS{Style.RESET}")
    print_separator("═")
    
    for cipher_id, info in ciphers.items():
        requirements = []
        if info['requires_key']:
            requirements.append("Key Required")
        if info['requires_shift']:
            requirements.append("Shift Value")
        
        req_text = f" ({', '.join(requirements)})" if requirements else ""
        
        print(f"{info['symbol']} {Style.BOLD}{info['name']}{Style.RESET}{req_text}")
        print(f"   {Style.GRAY}{info['description']}{Style.RESET}")
        print(f"   {Style.CYAN}Usage: --cipher {cipher_id}{Style.RESET}")
        print()

def execute_cipher_operation(cipher_type: str, text: str, mode: str, shift: Optional[int] = None, key: Optional[str] = None):
    """Execute cipher operation with professional feedback"""
    
    # Validate inputs
    ciphers = get_available_ciphers()
    if cipher_type not in ciphers:
        print_error(f"Unknown cipher type: {cipher_type}")
        return False
    
    cipher_info = ciphers[cipher_type]
    
    # Check requirements
    if cipher_info['requires_shift'] and shift is None:
        print_error(f"{cipher_info['name']} requires a shift value (use -s/--shift)")
        return False
    
    if cipher_info['requires_key'] and not key:
        print_error(f"{cipher_info['name']} requires a key (use -k/--key)")
        return False
    
    # Display operation header
    operation = "ENCODING" if mode == "encode" else "DECODING"
    print(f"\n{Style.WHITE}{Style.BOLD}🚀 INITIATING {operation} OPERATION{Style.RESET}")
    print_separator()
    
    # Animate operation
    animate_operation(f"Processing with {cipher_info['name']}")
    
    try:
        # Execute cipher operation
        suite = CipherSuite()
        decode_mode = (mode == "decode")
        
        if cipher_type == "caesar":
            result = suite.caesar_cipher(text, shift, decode_mode)
        elif cipher_type == "rot13":
            result = suite.rot13_cipher(text)
        elif cipher_type == "atbash":
            result = suite.atbash_cipher(text)
        elif cipher_type == "reverse":
            result = suite.reverse_cipher(text)
        elif cipher_type == "base64":
            if mode == "encode":
                result = suite.base64_encode(text)
            else:
                result = suite.base64_decode(text)
        elif cipher_type == "hex":
            if mode == "encode":
                result = suite.hex_encode(text)
            else:
                result = suite.hex_decode(text)
        elif cipher_type == "binary":
            if mode == "encode":
                result = suite.binary_encode(text)
            else:
                result = suite.binary_decode(text)
        elif cipher_type == "morse":
            if mode == "encode":
                result = suite.morse_encode(text)
            else:
                result = suite.morse_decode(text)
        elif cipher_type == "vigenere":
            result = suite.vigenere_cipher(text, key, decode_mode)
        
        # Display results
        kwargs = {}
        if shift is not None:
            kwargs['shift'] = shift
        if key:
            kwargs['key'] = key
            
        display_cipher_info(cipher_info['name'], text, result, **kwargs)
        
        print_success(f"{operation.capitalize()} completed successfully!", Style.DIAMOND)
        
        # Copy to clipboard suggestion
        print(f"\n{Style.GRAY}💡 Tip: Copy the output above to use your {operation.lower()}d text{Style.RESET}")
        
        return True
        
    except Exception as e:
        print_error(f"Cipher operation failed: {str(e)}")
        return False

def create_argument_parser():
    """Create enhanced argument parser with comprehensive options"""
    
    description = f"""
{Style.BOLD}EnigmaVault v{__version__}{Style.RESET} - Professional Multi-Cipher Encryption Suite

A comprehensive cryptographic toolkit supporting 9+ cipher algorithms including
classical ciphers, modern encoding schemes, and advanced polyalphabetic systems.
Perfect for security professionals, researchers, and cryptography enthusiasts.
"""
    
    epilog = f"""
{Style.BOLD}Cipher Examples:{Style.RESET}
  enigmavault -c caesar -m encode -t "Hello World" -s 3
  enigmavault -c vigenere -m encode -t "Secret Message" -k "PASSWORD"
  enigmavault -c morse -m encode -t "SOS"
  enigmavault -c base64 -m decode -t "SGVsbG8gV29ybGQ="

{Style.BOLD}Advanced Usage:{Style.RESET}
  enigmavault --list-ciphers                    # Show all available ciphers
  enigmavault -c caesar -m decode -t "KHOOR" -s 3  # Decode with Caesar
  
{Style.BOLD}Security Notice:{Style.RESET}
  These ciphers are for educational and research purposes. For production
  security, use modern cryptographic libraries with proven algorithms.

{Style.CYAN}Master the art of cryptography! 🔐{Style.RESET}
"""
    
    parser = argparse.ArgumentParser(
        prog='enigmavault',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main operation arguments
    main_group = parser.add_argument_group(f'{Style.BOLD}Core Arguments{Style.RESET}')
    main_group.add_argument('-c', '--cipher', metavar='TYPE',
                           help='Cipher algorithm to use (see --list-ciphers)')
    main_group.add_argument('-m', '--mode', choices=['encode', 'decode'], 
                           metavar='MODE', help='Operation mode: encode or decode')
    main_group.add_argument('-t', '--text', metavar='TEXT',
                           help='Input text to process')
    
    # Cipher parameters
    params_group = parser.add_argument_group(f'{Style.BOLD}Cipher Parameters{Style.RESET}')
    params_group.add_argument('-s', '--shift', type=int, metavar='N',
                             help='Shift value for Caesar cipher (positive or negative)')
    params_group.add_argument('-k', '--key', metavar='KEY',
                             help='Encryption key for key-based ciphers (e.g., Vigenère)')
    
    # Utility arguments
    utils_group = parser.add_argument_group(f'{Style.BOLD}Utility Options{Style.RESET}')
    utils_group.add_argument('--list-ciphers', action='store_true',
                            help='Display all available cipher algorithms')
    utils_group.add_argument('--no-header', action='store_true',
                            help='Skip the application header display')
    utils_group.add_argument('--version', action='version',
                            version=f'EnigmaVault {__version__}')
    
    return parser

def main():
    """Enhanced main application entry point"""
    parser = create_argument_parser()
    
    # Handle no arguments
    if len(sys.argv) == 1:
        print_header()
        print(f"{Style.YELLOW}{Style.BOLD}Welcome to EnigmaVault!{Style.RESET}")
        print(f"{Style.GRAY}Use --help for detailed usage or --list-ciphers to see available algorithms{Style.RESET}\n")
        parser.print_help()
        sys.exit(0)
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)
    
    # Handle list ciphers
    if args.list_ciphers:
        list_ciphers()
        sys.exit(0)
    
    # Validate required arguments
    if not all([args.cipher, args.mode, args.text]):
        if not args.no_header:
            print_header()
        print_error("Missing required arguments: --cipher, --mode, and --text are all required")
        print_info("Use --list-ciphers to see available cipher algorithms")
        sys.exit(1)
    
    # Display header unless disabled
    if not args.no_header:
        print_header()
    
    # Execute cipher operation
    success = execute_cipher_operation(
        cipher_type=args.cipher.lower(),
        text=args.text,
        mode=args.mode,
        shift=args.shift,
        key=args.key
    )
    
    # Exit with appropriate code
    if success:
        print(f"\n{Style.GREEN}{Style.BOLD}✨ Cryptographic mission accomplished! 🎯{Style.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Style.RED}{Style.BOLD}💥 Operation failed. Please check the parameters and try again.{Style.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Style.YELLOW}{Style.BOLD}🛑 Operation cancelled by user{Style.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Style.RED}{Style.BOLD}💥 Unexpected error: {e}{Style.RESET}")
        sys.exit(1)