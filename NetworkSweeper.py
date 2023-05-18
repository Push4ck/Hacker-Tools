import scapy.all as scapy
import argparse
import socket
import json
import csv
from datetime import datetime


# Define the scan function to scan the network using the IP provided
def scan(ip):
    try:
        # Create an ARP request for the provided IP
        arp_request = scapy.ARP(pdst=ip)
        # Create a broadcast Ethernet frame
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        # Combine the ARP request and the broadcast to send as a single packet
        arp_request_broadcast = scapy.srp(arp_request/broadcast, timeout=1, verbose=False)[0]

        # Initialize an empty list to store the results
        clients_list = []
        # Iterate through the received packets
        for sent, received in arp_request_broadcast:
            try:
                # Get the hostname from the received packet's source IP address
                hostname = socket.gethostbyname(received.psrc)
            except (socket.herror, socket.timeout):
                # If hostname cannot be resolved, set hostname to an empty string
                hostname = ""
            # Create a dictionary with the client information
            client_dict = {"ip": received.psrc, "mac": received.hwsrc, "hostname": hostname}
            # Append the client information to the clients_list
            clients_list.append(client_dict)
        # Return the clients_list
        return clients_list
    except Exception as e:
        # Raise an exception with an error message if an error occurs during the scan
        raise Exception("An error occurred while scanning the network: " + str(e))


# Define the print_result function to print the results
def print_result(results_list):
    # Print the header
    print("IP\t\t\t MAC Address \t\t Hostname\n----------------------------------------------")
    # Iterate through the results_list and print each client's information
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"] + "\t\t" + client["hostname"])


def save_to_txt(file_path, data):
    try:
        # Open the file with the specified path in write mode
        with open(file_path, 'x') as f:
            # Loop through each client in the data
            for client in data:
                # Write the IP, MAC, and hostname of the client to the file
                f.write(f"IP: {client['ip']}\tMAC: {client['mac']}\tHostname: {client['hostname']}\n")
    except FileExistsError as e:
        # Raise an exception if the file already exists
        raise Exception(f"File {file_path} already exists") from e

    except Exception as e:
        # Raise an exception if any other error occurs while saving the data to the file
        raise Exception("An error occurred while saving the output to a txt file: " + str(e))


def save_to_xml(file_path, data):
    try:
        # Create a list of scapy packets for each client in the data
        packets = [scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(psrc=client["ip"], hwsrc=client["mac"]) for client in data]
        # Write the packets to a pcap file using scapy's wrpcap method
        scapy.wrpcap(file_path, packets)
    except Exception as e:
        # Raise an exception if any error occurs while saving the data to the xml file
        raise Exception("An error occurred while saving the output to an xml file: " + str(e))


def save_to_json(file_path, data):
    try:
        # Open the file with the specified path in write mode
        with open(file_path, 'w') as f:
            # Write the data to the file in json format using the json.dump method
            json.dump(data, f, indent=4)
    except Exception as e:
        # Raise an exception if any error occurs while saving the data to the json file
        raise Exception("An error occurred while saving the output to a json file: " + str(e))


def save_to_csv(file_path, data):
    try:
        # Open file in write mode
        with open(file_path, 'w') as f:
            # Create a csv writer object with fieldnames
            writer = csv.DictWriter(f, fieldnames=["ip", "mac", "hostname"])
            # Write the header row
            writer.writeheader()
            # Write the data rows
            writer.writerows(data)
    except Exception as e:
        # Raise an error if an exception occurs
        raise Exception("An error occurred while saving the output to a csv file: " + str(e))


def save_to_html(data, file_path):
    try:
        # Open file in write mode
        with open(file_path, 'w') as f:
            # Write the HTML header
            f.write("<html>\n")
            f.write("  <head>\n")
            f.write("    <title>Data</title>\n")
            f.write("  </head>\n")
            f.write("  <body>\n")
            # Write the table header
            f.write("    <table>\n")
            f.write("      <tr>\n")
            f.write("        <th>IP</th>\n")
            f.write("        <th>MAC</th>\n")
            f.write("        <th>Hostname</th>\n")
            f.write("      </tr>\n")
            # Write the data rows
            for client in data:
                f.write("      <tr>\n")
                f.write("        <td>{}</td>\n".format(client['ip']))
                f.write("        <td>{}</td>\n".format(client['mac']))
                f.write("        <td>{}</td>\n".format(client['hostname']))
                f.write("      </tr>\n")
            # Close the table
            f.write("    </table>\n")
            # Close the body
            f.write("  </body>\n")
            # Close the html
            f.write("</html>\n")
    except Exception as e:
        # Raise an error if an exception occurs
        raise Exception("An error occurred while saving the data to HTML: " + str(e))


def main():
    # Initialize the argument parser with a description
    parser = argparse.ArgumentParser(description='Network Scanner')
    # Add a target argument to specify the IP address or range to scan
    parser.add_argument('-t', '--target', dest='ip', help='IP address or range to scan', required=True)
    # Add an output argument to specify the output file path (txt, xml, json)
    parser.add_argument('-o', '--output', dest='output', help='Output file path (txt, xml, json)')
    # Add a verbose argument to enable verbose output
    parser.add_argument('-v', '--verbose', dest='verbose', help='Verbose output', action='store_true')
    # Parse the arguments
    args = parser.parse_args()

    # Store the target IP address
    ip = args.ip
    # Store the output file path
    output = args.output
    # Store the verbose output flag
    verbose = args.verbose

    # Record the start time
    start_time = datetime.now()
    # Try to perform the network scan
    try:
        scan_result = scan(ip)
    except Exception as e:
        print(f"Error: {e}")
        return
    # Record the end time
    end_time = datetime.now()

    # If verbose output is enabled, print the time taken to complete the scan
    if verbose:
        print(f'Scan completed in {(end_time - start_time).seconds} seconds')

    # If an output file path is specified, save the scan results in the specified format(s)
    if output:
        formats = output.split(",")
        for f in formats:
            format = f.strip().split(".")[-1]
            try:
                if format == "txt":
                    save_to_txt(f, scan_result)
                elif format == "xml":
                    save_to_xml(f, scan_result)
                elif format == "json":
                    save_to_json(f, scan_result)
                elif format == "csv":
                    save_to_csv(f, scan_result)
                elif format == "html":
                    save_to_html(scan_result, f)
                # Raise an exception for unsupported output formats
                else:
                    raise Exception(f"Error: Unsupported output file format: {format}. Supported formats: txt, xml, json, csv, html")
            except Exception as e:
                print(f"Error saving to file format {format}: {e}")


if __name__ == "__main__":
    main()
