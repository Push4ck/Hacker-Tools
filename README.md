# Hacker-Tools

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/hacker-tools/toolkit)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/hacker-tools/toolkit)

A comprehensive collection of professional cybersecurity tools designed for ethical hacking, penetration testing, network analysis, and authorized security research. Perfect for cybersecurity professionals, ethical hackers, CTF players, and security enthusiasts.

## 🛡️ Tool Overview

| Tool              | Category          | Description                                          | Platform       |
| ----------------- | ----------------- | ---------------------------------------------------- | -------------- |
| **InfoScope**     | Surveillance      | Professional network scanner with device enumeration | Cross-platform |
| **ShadowTracer**  | Surveillance      | Tor-enabled web request interceptor and analyzer     | Cross-platform |
| **NetSweepX**     | Network Security  | Advanced network discovery and ARP scanning          | Cross-platform |
| **NetBreach**     | Network Security  | Professional network penetration testing tool        | Cross-platform |
| **PhantomMAC**    | Network Security  | Advanced MAC address spoofing and management         | Cross-platform |
| **BrutePilot**    | Password Security | Professional wordlist generator with mutations       | Cross-platform |
| **PassForge**     | Password Security | Secure password generator with strength analysis     | Cross-platform |
| **SpamStrike**    | Spam Testing      | HTTP request testing framework with proxy support    | Cross-platform |
| **GateKeeper**    | Access Control    | Professional authentication and access management    | Cross-platform |
| **StealthLocker** | Access Control    | Advanced file encryption and secure storage          | Cross-platform |
| **CryptoRaptor**  | Cryptography      | Multi-algorithm encryption and cryptographic toolkit | Cross-platform |
| **EnigmaVault**   | Cryptography      | Secure data vault with advanced encryption           | Cross-platform |
| **Sentinex**      | Malware Detection | Professional malware analysis and detection engine   | Cross-platform |

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Administrator/root privileges (for some network tools)
- Internet connection (for some security testing tools)
- Tor (for ShadowTracer)
- Firefox and geckodriver (for web tools)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/hacker-tools.git
   cd hacker-tools
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python tools/surveillance/InfoScope.py --version
   python tools/password/PassForge.py --version
   ```

### Basic Usage Examples

**Network Discovery with InfoScope:**

```bash
# Scan local network
python tools/surveillance/InfoScope.py -n 192.168.1.0/24 -v

# Save results to multiple formats
python tools/surveillance/InfoScope.py -n 192.168.1.1-50 -o network_scan.json
```

**Web Request Interception with ShadowTracer:**

```bash
# Basic request interception with Tor
python tools/surveillance/ShadowTracer.py https://example.com api --verbose

# Click element and capture requests
python tools/surveillance/ShadowTracer.py https://site.com login --click "#login-btn"
```

**Password Generation with PassForge:**

```bash
# Generate secure 16-character password
python tools/password/PassForge.py -l 16

# Generate multiple passwords without symbols
python tools/password/PassForge.py -l 12 --no-symbols --batch 5
```

**Wordlist Generation with BrutePilot:**

```bash
# Generate wordlist from keywords
python tools/password/BrutePilot.py --keywords admin password --mutations all --output wordlist.txt

# Generate random passwords
python tools/password/BrutePilot.py --random --count 5000 --length 10 --output random_passwords.txt
```

## 📁 Project Structure

```
Hacker-Tools/
├── tools/
│   ├── access/
│   │   ├── GateKeeper.py              # Authentication and access management
│   │   └── StealthLocker.py           # File encryption and secure storage
│   ├── crypto/
│   │   ├── CryptoRaptor.py            # Multi-algorithm encryption toolkit
│   │   └── EnigmaVault.py             # Secure data vault with encryption
│   ├── malware_detection/
│   │   └── Sentinex.py                # Malware analysis and detection
│   ├── networking/
│   │   ├── NetBreach.py               # Network penetration testing
│   │   ├── NetSweepX.py               # Network discovery and scanning
│   │   └── PhantomMAC.py              # MAC address spoofing
│   ├── password/
│   │   ├── BrutePilot.py              # Professional wordlist generator
│   │   └── PassForge.py               # Secure password generator
│   ├── spam/
│   │   ├── payloads.txt               # Sample test payloads
│   │   ├── proxies.txt                # Sample proxy list
│   │   └── SpamStrike.py              # HTTP testing framework
│   └── surveillance/
│       ├── InfoScope.py               # Network scanner and device enumeration
│       └── ShadowTracer.py            # Tor-enabled request interceptor
├── LICENSE                            # MIT License with security terms
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
└── tools.md                          # Detailed tool documentation
```

## 🔧 Tool Categories

### 🕵️ Surveillance Tools

**InfoScope** - Professional network discovery scanner featuring:

- Cross-platform ping-based host discovery
- Comprehensive hostname resolution and device type detection
- Multiple output formats (TXT, JSON, CSV, HTML)
- Threaded scanning for improved performance
- Real-time progress tracking and detailed statistics

**ShadowTracer** - Tor-enabled web request interceptor featuring:

- Tor proxy integration for anonymous browsing
- Selenium-based browser automation with stealth settings
- HTTP request/response interception and analysis
- Element interaction capabilities for dynamic content
- JSON output format for detailed analysis

### 🌐 Network Security Tools

**NetSweepX** - Advanced network discovery featuring:

- ARP-based device discovery with layer 2/3 fallback
- MAC address detection and vendor identification
- Comprehensive network mapping and topology analysis
- Performance-optimized scanning algorithms

**NetBreach** - Network penetration testing featuring:

- Port scanning and service enumeration
- Vulnerability assessment and exploit testing
- Network protocol analysis and testing
- Advanced stealth and evasion techniques

**PhantomMAC** - MAC address management featuring:

- Cross-platform MAC address modification
- Vendor-specific MAC generation
- Original MAC address restoration
- Change history tracking and validation

### 🔐 Password Security Tools

**PassForge** - Professional password generator featuring:

- Cryptographically secure random password generation
- Real-time password strength analysis with detailed criteria
- Customizable character sets and complexity requirements
- Batch generation capabilities for multiple passwords
- Ambiguous character exclusion for improved usability

**BrutePilot** - Advanced wordlist generator featuring:

- Keyword-based password generation with intelligent mutations
- Advanced mutation algorithms (case variations, leet speak, patterns)
- Random password generation with customizable character sets
- Comprehensive filtering options for targeted wordlists
- Progress tracking and detailed statistics reporting

### 🎯 Spam Testing Tools

**SpamStrike** - HTTP testing framework featuring:

- Multi-proxy HTTP request testing with rotation support
- Payload injection testing for authorized security assessments
- Response analysis with pattern detection
- Rate limiting and concurrent request management
- Comprehensive JSON reporting with performance metrics

### 🔒 Access Control Tools

**GateKeeper** - Authentication and access management featuring:

- Multi-factor authentication implementation
- Role-based access control (RBAC)
- Session management and token validation
- Audit logging and security monitoring

**StealthLocker** - File encryption and secure storage featuring:

- Military-grade encryption algorithms
- Secure key derivation and management
- Hidden volume creation and steganography
- Cross-platform compatibility and portability

### 🛡️ Cryptography Tools

**CryptoRaptor** - Multi-algorithm encryption toolkit featuring:

- Support for multiple encryption algorithms (AES, RSA, ChaCha20)
- Digital signature creation and verification
- Cryptographic hash functions and key derivation
- Secure random number generation

**EnigmaVault** - Secure data vault featuring:

- Advanced encryption with perfect forward secrecy
- Secure password management and storage
- Encrypted database with integrity verification
- Multi-layer security architecture

### 🔍 Malware Detection Tools

**Sentinex** - Malware analysis and detection featuring:

- Static and dynamic malware analysis
- Signature-based and heuristic detection
- Behavioral analysis and anomaly detection
- Threat intelligence integration

## 🛠️ Advanced Usage

### Environment Setup

**For Development:**

```bash
# Create virtual environment
python -m venv hacker-tools-env
source hacker-tools-env/bin/activate  # Linux/macOS
# hacker-tools-env\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
```

**For Production:**

```bash
# Install system-wide (requires admin privileges)
sudo pip install -r requirements.txt
```

### Configuration Examples

**InfoScope Advanced Scanning:**

```bash
# Comprehensive network scan with verbose output
python tools/surveillance/InfoScope.py -n 192.168.1.0/24 --threads 200 --timeout 2 -v

# Quick scan of specific range with HTML report
python tools/surveillance/InfoScope.py -n 10.10.10.1-100 -o detailed_scan.html
```

**ShadowTracer Advanced Interception:**

```bash
# Comprehensive request analysis with Tor
python tools/surveillance/ShadowTracer.py https://target.com api \
    --click "#submit-btn" --timeout 60 --wait 10 --output analysis.json --verbose

# Visible browser mode for debugging
python tools/surveillance/ShadowTracer.py https://site.com login \
    --visible --verbose --port 9050
```

**BrutePilot Advanced Wordlist Generation:**

```bash
# Generate comprehensive wordlist with all mutations
python tools/password/BrutePilot.py --keywords company admin login \
    --min-length 6 --max-length 16 --mutations all \
    --filter-min-length 8 --require-mixed-case \
    --output advanced_wordlist.txt --format csv
```

## 📚 Documentation

### Quick Reference

- **[tools.md](tools.md)** - Comprehensive tool documentation with detailed usage examples
- **Individual tool help:** Use `--help` flag with any tool for detailed usage information
- **Configuration examples:** Check tool directories for sample configuration files

### Security Considerations

⚠️ **Important Security Notes:**

1. **Authorization Required:** Always ensure you have explicit permission before testing networks or systems
2. **Administrator Privileges:** Network tools require elevated privileges for full functionality
3. **Responsible Disclosure:** Report security vulnerabilities through proper channels
4. **Rate Limiting:** Use appropriate delays to avoid overwhelming target systems
5. **Legal Compliance:** Ensure all testing complies with applicable laws and regulations

## 🎯 Use Cases

### Penetration Testing

- Network reconnaissance and device discovery
- Web application security testing and analysis
- Password security evaluation and wordlist generation
- Access control testing and authentication bypass

### Cybersecurity Education

- CTF competition tools and techniques
- Hands-on security training and skill development
- Network security fundamentals and practical exercises
- Cryptography and security protocol understanding

### Security Research

- Network protocol analysis and testing
- Malware analysis and reverse engineering
- Cryptographic algorithm implementation and testing
- Security tool development and methodology research

### Network Administration

- Network device discovery and inventory management
- Security configuration testing and validation
- Performance monitoring and troubleshooting
- Access control and authentication management

## 🤝 Contributing

We welcome contributions from the cybersecurity community! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow coding standards** and maintain consistent styling
3. **Add comprehensive tests** for new functionality
4. **Update documentation** for any changes
5. **Submit a pull request** with detailed description

### Development Standards

- Follow PEP 8 Python style guidelines
- Include comprehensive error handling and logging
- Maintain cross-platform compatibility where possible
- Add professional CLI interfaces with help documentation
- Include security considerations and usage warnings

## 📄 License

This project is licensed under the MIT License with additional security terms - see the [LICENSE](LICENSE) file for details.

## ⚡ Support

### Getting Help

- **Documentation:** Check [tools.md](tools.md) for detailed tool documentation
- **Issues:** Report bugs and request features via GitHub Issues
- **Security:** For security-related concerns, please contact maintainers directly

### System Requirements

| Component  | Minimum            | Recommended        |
| ---------- | ------------------ | ------------------ |
| Python     | 3.7+               | 3.9+               |
| RAM        | 4GB                | 8GB+               |
| Storage    | 500MB              | 2GB+               |
| Network    | Basic connectivity | Stable broadband   |
| Privileges | Standard user      | Administrator/root |

## 🔮 Roadmap

### Upcoming Features

- **Web interface** for remote tool management and monitoring
- **Plugin system** for custom security modules and extensions
- **Database integration** for result storage and historical analysis
- **REST API** for tool automation and CI/CD integration
- **Advanced reporting** with visual analytics and trend analysis

### Version History

- **v2.0.0** - Complete toolkit with 13 professional security tools
- **v1.5.0** - Added surveillance and cryptography tools
- **v1.0.0** - Initial release with core security tools

---

## 🏆 Acknowledgments

Special thanks to the cybersecurity community for inspiration and the open-source projects that make this toolkit possible.

**Educational Disclaimer:** This toolkit is intended for educational purposes, authorized security testing, and cybersecurity research only. Users are responsible for ensuring compliance with applicable laws and regulations.

---

_Built with ❤️ by security professionals, for security professionals._
