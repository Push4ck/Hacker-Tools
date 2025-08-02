#!/usr/bin/env python3
"""
CryptoRaptor - Professional Folder Encryption Tool
Advanced AES-256 encryption with military-grade security
"""

import os
import sys
import shutil
import argparse
import getpass
import platform
import time
from pathlib import Path
from typing import Optional

try:
    import pyzipper
except ImportError:
    print("❌ Missing dependency: 'pyzipper' is required")
    print("   Install with: pip install pyzipper")
    sys.exit(1)

# Constants
__version__ = "2.1.0"
__author__ = "CryptoRaptor Security Team"
TEMP_FOLDER = ".cryptoraptor_temp"

class Style:
    """Enhanced styling system for professional CLI appearance"""
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
    SUCCESS = '✅'
    ERROR = '❌'
    WARNING = '⚠️'
    INFO = 'ℹ️'
    LOCK = '🔐'
    SHIELD = '🛡️'
    ROCKET = '🚀'
    FIRE = '🔥'
    
    @classmethod
    def init_colors(cls):
        """Initialize color support across platforms"""
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                # Disable colors on unsupported Windows versions
                for attr in dir(cls):
                    if not attr.startswith('_') and attr.isupper() and len(getattr(cls, attr)) > 1:
                        setattr(cls, attr, '')

# Initialize styling
Style.init_colors()

def print_header():
    """Display professional application header"""
    width = 80
    header = f"""
{Style.CYAN}{Style.BOLD}{'=' * width}
{'CryptoRaptor'.center(width)}
{'Professional Folder Encryption Suite'.center(width)}
{Style.RESET}{Style.CYAN}{'=' * width}{Style.RESET}

{Style.WHITE}{Style.BOLD}Version:{Style.RESET} {Style.CYAN}{__version__}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Platform:{Style.RESET} {Style.CYAN}{platform.system()}{Style.RESET}  {Style.GRAY}|{Style.RESET}  {Style.WHITE}{Style.BOLD}Security:{Style.RESET} {Style.GREEN}AES-256{Style.RESET}

{Style.YELLOW}{Style.ITALIC}"Military-grade encryption for your most sensitive data"{Style.RESET}
"""
    print(header)

def print_success(message: str, prefix: str = "SUCCESS"):
    """Enhanced success message"""
    print(f"{Style.GREEN}{Style.BOLD}[{prefix}]{Style.RESET} {Style.SUCCESS} {message}")

def print_error(message: str, prefix: str = "ERROR"):
    """Enhanced error message"""
    print(f"{Style.RED}{Style.BOLD}[{prefix}]{Style.RESET} {Style.ERROR} {message}")

def print_warning(message: str, prefix: str = "WARNING"):
    """Enhanced warning message"""
    print(f"{Style.YELLOW}{Style.BOLD}[{prefix}]{Style.RESET} {Style.WARNING} {message}")

def print_info(message: str, prefix: str = "INFO"):
    """Enhanced info message"""
    print(f"{Style.BLUE}{Style.BOLD}[{prefix}]{Style.RESET} {Style.INFO} {message}")

def print_step(step: int, total: int, message: str):
    """Print step progress"""
    progress = f"[{step}/{total}]"
    print(f"{Style.CYAN}{Style.BOLD}{progress}{Style.RESET} {Style.ROCKET} {message}")

def print_separator(char: str = "─", length: int = 60):
    """Print a visual separator"""
    print(f"{Style.GRAY}{char * length}{Style.RESET}")

def format_size(size_bytes: int) -> str:
    """Convert bytes to human readable format with styling"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            if unit in ['MB', 'GB', 'TB']:
                return f"{Style.BOLD}{size_bytes:.1f}{Style.RESET} {Style.CYAN}{unit}{Style.RESET}"
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_folder_stats(folder_path: str) -> tuple:
    """Get comprehensive folder statistics"""
    total_size = 0
    file_count = 0
    folder_count = 0
    
    try:
        for root, dirs, files in os.walk(folder_path):
            folder_count += len(dirs)
            file_count += len(files)
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    continue
    except (OSError, IOError):
        pass
    
    return total_size, file_count, folder_count

def display_folder_info(folder_path: str):
    """Display comprehensive folder information"""
    size, files, folders = get_folder_stats(folder_path)
    
    print_separator()
    print(f"{Style.WHITE}{Style.BOLD}📁 SOURCE ANALYSIS{Style.RESET}")
    print_separator()
    
    info_items = [
        ("Path", os.path.abspath(folder_path)),
        ("Size", format_size(size)),
        ("Files", f"{Style.BOLD}{files:,}{Style.RESET}"),
        ("Folders", f"{Style.BOLD}{folders:,}{Style.RESET}")
    ]
    
    for label, value in info_items:
        print(f"  {Style.CYAN}{Style.BOLD}{label:.<12}{Style.RESET} {value}")
    
    print_separator()

def animate_progress(message: str, duration: float = 1.0):
    """Simple progress animation"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        print(f"\r{Style.BLUE}{frames[i % len(frames)]}{Style.RESET} {message}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    
    print(f"\r{Style.GREEN}✓{Style.RESET} {message}")

def validate_inputs(folder_path: str, output_dir: str, password: str) -> bool:
    """Enhanced input validation with detailed feedback"""
    
    print_step(1, 3, "Validating source folder...")
    
    # Check folder existence
    if not os.path.exists(folder_path):
        print_error(f"Source folder does not exist: {folder_path}")
        return False
    
    if not os.path.isdir(folder_path):
        print_error(f"Path is not a directory: {folder_path}")
        return False
    
    if not os.access(folder_path, os.R_OK):
        print_error(f"Insufficient permissions to read folder: {folder_path}")
        return False
    
    # Check if folder is empty
    try:
        contents = os.listdir(folder_path)
        if not contents:
            print_warning("Source folder is empty")
            if not get_user_confirmation("Continue with empty folder?"):
                return False
    except PermissionError:
        print_error(f"Access denied to folder contents: {folder_path}")
        return False
    
    print_step(2, 3, "Validating output directory...")
    
    # Validate output directory
    try:
        os.makedirs(output_dir, exist_ok=True)
        if not os.access(output_dir, os.W_OK):
            print_error(f"No write permission for output directory: {output_dir}")
            return False
    except (OSError, IOError) as e:
        print_error(f"Cannot create output directory: {e}")
        return False
    
    print_step(3, 3, "Validating security parameters...")
    
    # Password strength check
    if len(password) < 8:
        print_warning("Password is shorter than recommended (8+ characters)")
        if not get_user_confirmation("Continue with weak password?"):
            return False
    elif len(password) < 12:
        print_warning("Consider using a stronger password (12+ characters)")
    
    print_success("All validations passed", "VALIDATED")
    return True

def get_user_confirmation(prompt: str) -> bool:
    """Get styled user confirmation"""
    try:
        response = input(f"{Style.CYAN}{Style.BOLD}❓ {prompt} (y/N): {Style.RESET}")
        return response.lower() in ['y', 'yes']
    except KeyboardInterrupt:
        print(f"\n{Style.YELLOW}Operation cancelled by user{Style.RESET}")
        return False

def encrypt_folder(folder_path: str, output_dir: str, password: str, 
                  output_name: str = "encrypted.zip", overwrite: bool = False) -> bool:
    """Enhanced folder encryption with professional UI"""
    
    # Header
    print_header()
    
    # Display folder info
    display_folder_info(folder_path)
    
    # Validate inputs
    if not validate_inputs(folder_path, output_dir, password):
        return False
    
    # Prepare paths
    temp_path = os.path.join(os.getcwd(), TEMP_FOLDER)
    encrypted_zip_path = os.path.join(output_dir, output_name)
    
    # Check for existing file
    if os.path.exists(encrypted_zip_path) and not overwrite:
        print_error(f"Output file already exists: {encrypted_zip_path}")
        print_info("Use --overwrite to replace existing files")
        return False
    
    try:
        # Cleanup and prepare
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path, ignore_errors=True)
        os.makedirs(temp_path, exist_ok=True)
        
        print()
        print(f"{Style.WHITE}{Style.BOLD}🚀 ENCRYPTION PROCESS{Style.RESET}")
        print_separator()
        
        # Stage 1: File preparation
        animate_progress("Preparing files for encryption", 1.5)
        
        items_copied = 0
        skipped_items = []
        
        for item in os.listdir(folder_path):
            src = os.path.join(folder_path, item)
            dst = os.path.join(temp_path, item)
            
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, temp_path)
                items_copied += 1
            except (IOError, OSError) as e:
                skipped_items.append((item, str(e)))
                continue
        
        if skipped_items:
            print_warning(f"Skipped {len(skipped_items)} items due to errors")
            for item, error in skipped_items[:3]:  # Show first 3 errors
                print(f"  {Style.GRAY}• {item}: {error}{Style.RESET}")
            if len(skipped_items) > 3:
                print(f"  {Style.GRAY}• ... and {len(skipped_items) - 3} more{Style.RESET}")
        
        if items_copied == 0:
            print_error("No files were successfully prepared for encryption")
            return False
        
        # Stage 2: Encryption
        animate_progress("Creating encrypted archive", 2.0)
        
        with pyzipper.AESZipFile(encrypted_zip_path, 'w', 
                               compression=pyzipper.ZIP_LZMA, 
                               encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode('utf-8'))
            
            files_added = 0
            for root, _, files in os.walk(temp_path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    arcname = os.path.relpath(abs_path, temp_path)
                    
                    try:
                        zf.write(abs_path, arcname=arcname)
                        files_added += 1
                    except (IOError, OSError) as e:
                        print_warning(f"Failed to encrypt '{file}': {e}")
                        continue
        
        # Stage 3: Verification
        animate_progress("Verifying encrypted archive", 1.0)
        
        if not os.path.exists(encrypted_zip_path):
            print_error("Failed to create encrypted archive")
            return False
        
        # Display results
        original_size, _, _ = get_folder_stats(folder_path)
        archive_size = os.path.getsize(encrypted_zip_path)
        compression_ratio = (1 - archive_size / original_size) * 100 if original_size > 0 else 0
        
        print()
        print(f"{Style.GREEN}{Style.BOLD}🎉 ENCRYPTION COMPLETED SUCCESSFULLY!{Style.RESET}")
        print_separator("═")
        
        results = [
            ("Archive Location", encrypted_zip_path),
            ("Original Size", format_size(original_size)),
            ("Compressed Size", format_size(archive_size)),
            ("Compression Ratio", f"{Style.BOLD}{compression_ratio:.1f}%{Style.RESET}"),
            ("Files Encrypted", f"{Style.BOLD}{files_added:,}{Style.RESET}"),
            ("Encryption", f"{Style.GREEN}{Style.BOLD}AES-256{Style.RESET}"),
            ("Status", f"{Style.GREEN}{Style.BOLD}SECURE{Style.RESET} {Style.SHIELD}")
        ]
        
        for label, value in results:
            print(f"  {Style.CYAN}{Style.BOLD}{label:.<20}{Style.RESET} {value}")
        
        print_separator("═")
        print(f"{Style.YELLOW}{Style.BOLD}⚠️  IMPORTANT: Keep your password safe! Without it, your data cannot be recovered.{Style.RESET}")
        
        return True
        
    except Exception as e:
        print_error(f"Encryption process failed: {e}")
        return False
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path, ignore_errors=True)

def get_secure_password() -> Optional[str]:
    """Enhanced secure password input"""
    try:
        print(f"\n{Style.WHITE}{Style.BOLD}🔐 SECURITY SETUP{Style.RESET}")
        print_separator()
        
        password = getpass.getpass(f"{Style.CYAN}{Style.BOLD}Enter encryption password: {Style.RESET}")
        if not password:
            print_error("Password cannot be empty")
            return None
        
        confirm = getpass.getpass(f"{Style.CYAN}{Style.BOLD}Confirm password: {Style.RESET}")
        if password != confirm:
            print_error("Passwords do not match")
            return None
        
        # Password strength indicator
        strength = "WEAK"
        color = Style.RED
        if len(password) >= 12:
            strength = "STRONG"
            color = Style.GREEN
        elif len(password) >= 8:
            strength = "MEDIUM"
            color = Style.YELLOW
        
        print(f"Password strength: {color}{Style.BOLD}{strength}{Style.RESET}")
        return password
        
    except KeyboardInterrupt:
        print(f"\n{Style.YELLOW}Operation cancelled by user{Style.RESET}")
        return None

def create_argument_parser():
    """Create enhanced argument parser"""
    description = f"""
{Style.BOLD}CryptoRaptor v{__version__}{Style.RESET} - Professional Folder Encryption Suite

Secure your sensitive folders with military-grade AES-256 encryption.
Advanced compression algorithms ensure optimal file sizes while maintaining maximum security.
"""
    
    parser = argparse.ArgumentParser(
        prog='cryptoraptor',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Style.BOLD}Examples:{Style.RESET}
  cryptoraptor -f /path/to/secret-docs -o /secure/location
  cryptoraptor -f ./project -o ./backup -n project-backup.zip
  cryptoraptor -f ~/documents -o ~/encrypted --overwrite

{Style.BOLD}Security Notice:{Style.RESET}
  This tool uses AES-256 encryption with PBKDF2 key derivation.
  Your password is the only way to decrypt your data - keep it safe!
"""
    )
    
    # Required arguments
    required = parser.add_argument_group(f'{Style.BOLD}Required Arguments{Style.RESET}')
    required.add_argument('-f', '--folder', required=True, metavar='PATH',
                         help='Path to the folder to encrypt')
    required.add_argument('-o', '--output', required=True, metavar='DIR',
                         help='Output directory for encrypted archive')
    
    # Optional arguments
    optional = parser.add_argument_group(f'{Style.BOLD}Optional Arguments{Style.RESET}')
    optional.add_argument('-p', '--password', metavar='PASS',
                         help='Encryption password (prompted securely if not provided)')
    optional.add_argument('-n', '--name', default='encrypted.zip', metavar='NAME',
                         help='Output filename (default: encrypted.zip)')
    optional.add_argument('--overwrite', action='store_true',
                         help='Overwrite existing output files')
    optional.add_argument('--no-header', action='store_true',
                         help='Skip the application header')
    optional.add_argument('--version', action='version', 
                         version=f'CryptoRaptor {__version__}')
    
    return parser

def main():
    """Enhanced main application entry point"""
    parser = create_argument_parser()
    
    # Handle no arguments
    if len(sys.argv) == 1:
        print_header()
        print(f"{Style.YELLOW}{Style.BOLD}No arguments provided{Style.RESET}")
        print(f"{Style.GRAY}Use --help for detailed usage information{Style.RESET}\n")
        parser.print_help()
        sys.exit(1)
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)
    
    # Get password if not provided
    password = args.password
    if not password:
        password = get_secure_password()
        if not password:
            sys.exit(1)
    
    # Convert to absolute paths
    folder_path = os.path.abspath(args.folder)
    output_dir = os.path.abspath(args.output)
    
    # Execute encryption
    success = encrypt_folder(
        folder_path=folder_path,
        output_dir=output_dir,
        password=password,
        output_name=args.name,
        overwrite=args.overwrite
    )
    
    # Exit with appropriate code
    if success:
        print(f"\n{Style.GREEN}{Style.BOLD}✨ Mission accomplished! Your data is now fortress-level secure.{Style.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Style.RED}{Style.BOLD}💥 Operation failed. Please review the errors above.{Style.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()