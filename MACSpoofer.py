import subprocess
import optparse
import re


# Define a function to parse command line arguments
def get_arguments():
    # Create an instance of OptionParser class
    parser = optparse.OptionParser()

    # Add options for the interface and new MAC address
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    # Parse the options and arguments
    (options, arguments) = parser.parse_args()

    # Check if the interface and new MAC address are specified
    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC")

    # Return the options
    return options


# Define a function to change the MAC address
def change_mac(interface, new_mac):
    # Print the message that the MAC address is changing
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)

    # Disable the specified interface
    subprocess.call(["ifconfig", interface, "down"])

    # Change the MAC address of the specified interface
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

    # Enable the specified interface
    subprocess.call(["ifconfig", interface, "up"])


# Define a function to get the current MAC address of an interface
def get_current_mac(interface):
    # Get the result of running the ifconfig command on the specified interface
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    # Search for the MAC address in the result
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                                          ifconfig_result.decode('utf-8'))

    # Return the MAC address if found
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        # Print an error message if the MAC address was not changed
        print("[-] MAC Address did not get changed")


# Get the command line arguments
options = get_arguments()

# Get the current MAC address of the specified interface
current_mac = get_current_mac(options.interface)
print("[+] Current MAC Address: " + str(current_mac))

# Change the MAC address of the specified interface
change_mac(options.interface, options.new_mac)

# Get the current MAC address of the specified interface
current_mac = get_current_mac(options.interface)

# Check if the MAC address was successfully changed
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")
