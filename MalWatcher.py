import os
import hashlib
import logging

# Set up logging configuration to log messages to a file 'scanner.log'
# with log level set to DEBUG and log format as asctime:levelname:message
logging.basicConfig(filename='scanner.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# List of known malware hashes
_malware_hashes = ['ef3cb3f3d3c5d3e3f3g3h3i3j3k3l3m3n3o3p3q', 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0']

# Dictionary of supported hash algorithms with sha256 as the only supported algorithm for now
supported_hash_algorithms = {
    "sha256": hashlib.sha256
}

def update_malware_hashes(new_hashes: list) -> None:
    """
    Add new hashes to the list of known malware hashes.

    :param new_hashes: A list of new hashes to be added.
    :type new_hashes: list
    :return: None
    :rtype: None
    """
    # Extend the list of known malware hashes with the new hashes
    _malware_hashes.extend(new_hashes)

def check_file_hash(file_path: str, algorithm: str) -> None:
    """
    Check if the file's hash is in the list of known malware hashes and log the result.

    :param file_path: Path to the file.
    :type file_path: str
    :param algorithm: The hash algorithm to be used.
    :type algorithm: str
    :return: None
    :rtype: None
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if the path is a file
        if not os.path.isfile(file_path):
            raise TypeError(f"{file_path} is not a file")
        
        # Check if the algorithm is supported
        if algorithm not in supported_hash_algorithms:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        # Open the file in binary mode and calculate the hash
        with open(os.path.abspath(file_path), 'rb') as f:
            file_hash = supported_hash_algorithms[algorithm](f.read()).hexdigest()
            
            # Check if the hash is in the list of known malware hashes
            if file_hash in _malware_hashes:
                logging.error(f'Found malware: {file_path}')
            else:
                logging.info(f'Scan complete: {file_path}')
    except FileNotFoundError as e:
        # Log error if the file is not found
        logging.error(f"File not found: {file_path}")
    except TypeError as e:
        # Log error if the path is not a file
        logging.error(f"{file_path} is not a file")
    except ValueError as e:
        # Log error if the algorithm is unsupported
        logging.error(f"{e}")
    except Exception as e:
        # Log error if an unexpected exception occurs
        logging.error(f"An error occurred while reading file {file_path}: {e}")

def scan_directory(directory: str, algorithm: str) -> None:
    """
    Scan all the files in the given directory and log the results

    Parameters:
    directory (str): path to the directory to scan
    algorithm (str): name of the hash algorithm to use

    Returns:
    None
    """
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        # Check if the path is a directory
        if not os.path.isdir(directory):
            raise TypeError(f"{directory} is not a directory")
        # Loop through all the files and directories within the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Call the check_file_hash function to log the results
                check_file_hash(file_path, algorithm)
    except FileNotFoundError as e:
        # Log error if directory is not found
        logging.error(f"Directory not found: {directory}")
    except TypeError as e:
        # Log error if the path is not a directory
        logging.error(f"{directory} is not a directory")
    except Exception as e:
        # Log any other errors that occur while scanning the directory
        logging.error(f"An error occurred while scanning directory {directory}: {e}")
