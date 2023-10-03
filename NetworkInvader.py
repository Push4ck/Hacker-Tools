import sys
import re
import wmi

def change_ip(interface="", new_ip="", subnet_mask="", gateway="", check=False):
    # Prompt for missing input parameters
    if not interface:
        interface = input("Enter the interface name: ")
    if not new_ip:
        new_ip = input("Enter the new IP address: ")
    if not subnet_mask:
        subnet_mask = input("Enter the subnet mask: ")
    if not gateway:
        gateway = input("Enter the default gateway: ")

    # Check if any of the required parameters are missing
    if not interface or not new_ip or not subnet_mask or not gateway:
        print("Error: interface, new_ip, subnet_mask, and gateway are all required parameters")
        return 1

    # Validate input types and formats
    if not isinstance(new_ip, str) or not isinstance(subnet_mask, str) or not isinstance(gateway, str):
        print("Error: Invalid input type. All inputs must be strings.")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", new_ip):
        print("Error: Invalid IP address format")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", subnet_mask):
        print("Error: Invalid subnet mask format")
        return 1

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", gateway):
        print("Error: Invalid gateway format")
        return 1

    try:
        # Connect to the Windows Management Instrumentation (WMI) service
        wmiService = wmi.WMI()
        
        # Get network adapter configurations for IP-enabled adapters
        networkConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)

        # Iterate through network adapter configurations
        for config in networkConfigs:
            if config.Description == interface:
                # Set the IP address and subnet mask
                result = config.EnableStatic(IPAddress=[new_ip], SubnetMask=[subnet_mask])
                if result[0] == 0:
                    print("IP address set successfully.")
                else:
                    print(f"Error setting IP address. Error code: {result[0]}")
                    return result[0]

                # Set the default gateway
                result = config.SetGateways(DefaultIPGateway=[gateway])
                if result[0] == 0:
                    print("Default gateway set successfully.")
                else:
                    print(f"Error setting default gateway. Error code: {result[0]}")
                    return result[0]

    except Exception as e:
        # Handle exceptions, if any
        print(f"Error: {str(e)}")
        return 1

    if check:
        try:
            # Retrieve and print the current IP configuration
            wmiService = wmi.WMI()
            networkConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)

            for config in networkConfigs:
                if config.Description == interface:
                    print("Current IP Configuration:")
                    print(f"IP Address: {config.IPAddress[0]}")
                    print(f"Subnet Mask: {config.IPSubnet[0]}")
                    print(f"Default Gateway: {config.DefaultIPGateway[0]}")

        except Exception as e:
            # Handle exceptions, if any
            print(f"Error: {str(e)}")
            return 1

if __name__ == '__main__':
    # Execute the change_ip function and exit the script
    sys.exit(change_ip())
