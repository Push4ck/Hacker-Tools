import subprocess
import optparse
import re
import platform


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


def change_mac_linux(interface, new_mac):
    # Print the message that the MAC address is changing
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)

    # Disable the specified interface
    subprocess.call(["ifconfig", interface, "down"])

    # Change the MAC address of the specified interface
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

    # Enable the specified interface
    subprocess.call(["ifconfig", interface, "up"])


def change_mac_windows(interface, new_mac):
    # Print the message that the MAC address is changing
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)

    # Modify the registry to set the new MAC address
    subprocess.call(["reg", "add",
                     "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\{interface}\Ndi\params\NetworkAddress",
                     "/v", "/d", new_mac, "/f"])

    # Disable and enable the specified interface
    subprocess.call(["netsh", "interface", "set", "interface", "name=" + interface, "admin=disable"])
    subprocess.call(["netsh", "interface", "set", "interface", "name=" + interface, "admin=enable"])


def get_current_mac_linux(interface):
    # Get the result of running the ifconfig command on the specified interface
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    # Search for the MAC address in the result
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))

    # Return the MAC address if found
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        # Print an error message if the MAC address was not changed
        print("[-] MAC Address did not get changed")


def get_current_mac_windows(interface):
    # Get the result of querying the registry for the MAC address of the specified interface
    result = subprocess.check_output(["reg", "query",
                                      "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\{interface}\Ndi\params\NetworkAddress"])

    # Search for the MAC address in the result
    mac_address_search_result = re.search(r"NetworkAddress\s+REG_SZ\s+([\w-]+)", result.decode('utf-8'))

    # Return the MAC address if found
    if mac_address_search_result:
        return mac_address_search_result.group(1)
    else:
        # Print an error message if the MAC address was not found
        print("[-] Failed to get current MAC Address")


# Get the command line arguments
options = get_arguments()

# Get the current MAC address of the specified interface based on the platform
current_mac = ""
if platform.system() == "Linux":
    current_mac = get_current_mac_linux(options.interface)
elif platform.system() == "Windows":
    current_mac = get_current_mac_windows(options.interface)

# Print the current MAC address
print("[+] Current MAC Address: " + str(current_mac))

# Change the MAC address of the specified interface based on the platform
if platform.system() == "Linux":
    change_mac_linux(options.interface, options.new_mac)
elif platform.system() == "Windows":
    change_mac_windows(options.interface, options.new_mac)

# Get the current MAC address of the specified interface again
current_mac = ""
if platform.system() == "Linux":
    current_mac = get_current_mac_linux(options.interface)
elif platform.system() == "Windows":
    current_mac = get_current_mac_windows(options.interface)

# Check if the MAC address was successfully changed
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")
