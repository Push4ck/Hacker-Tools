import scapy.all as scapy
import argparse
import socket
import json
import csv
from datetime import datetime

def scan(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = scapy.srp(arp_request/broadcast, timeout=1, verbose=False)[0]

        clients_list = []
        for sent, received in arp_request_broadcast:
            try:
                hostname = socket.gethostbyname(received.psrc)
            except (socket.herror, socket.timeout):
                hostname = ""
            client_dict = {"ip": received.psrc, "mac": received.hwsrc, "hostname": hostname}
            clients_list.append(client_dict)
        return clients_list
    except Exception as e:
        raise Exception("An error occurred while scanning the network: " + str(e))

def print_result(results_list):
    print("IP\t\t\t MAC Address \t\t Hostname\n----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"] + "\t\t" + client["hostname"])

def save_to_txt(file_path, data):
    try:
        with open(file_path, 'x') as f:
            for client in data:
                f.write(f"IP: {client['ip']}\tMAC: {client['mac']}\tHostname: {client['hostname']}\n")
    except FileExistsError as e:
        raise Exception(f"File {file_path} already exists")
    except Exception as e:
        raise Exception("An error occurred while saving the output to a txt file: " + str(e))

def save_to_xml(file_path, data):
    try:
        packets = [scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(psrc=client["ip"], hwsrc=client["mac"]) for client in data]
        scapy.wrpcap(file_path, packets)
    except Exception as e:
        raise Exception("An error occurred while saving the output to an xml file: " + str(e))

def save_to_json(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception("An error occurred while saving the output to a json file: " + str(e))

def save_to_csv(file_path, data):
    try:
        with open(file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["ip", "mac", "hostname"])
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        raise Exception("An error occurred while saving the output to a csv file: " + str(e))

def save_to_html(data, file_path):
    try:
        with open(file_path, 'w') as f:
            f.write("<html>\n")
            f.write("  <head>\n")
            f.write("    <title>Data</title>\n")
            f.write("  </head>\n")
            f.write("  <body>\n")
            f.write("    <table>\n")
            f.write("      <tr>\n")
            f.write("        <th>IP</th>\n")
            f.write("        <th>MAC</th>\n")
            f.write("        <th>Hostname</th>\n")
            f.write("      </tr>\n")
            for client in data:
                f.write("      <tr>\n")
                f.write("        <td>{}</td>\n".format(client['ip']))
                f.write("        <td>{}</td>\n".format(client['mac']))
                f.write("        <td>{}</td>\n".format(client['hostname']))
                f.write("      </tr>\n")
            f.write("    </table>\n")
            f.write("  </body>\n")
            f.write("</html>\n")
    except Exception as e:
        raise Exception("An error occurred while saving the data to HTML: " + str(e))

def main():
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('-t', '--target', dest='ip', help='IP address or range to scan', required=True)
    parser.add_argument('-o', '--output', dest='output', help='Output file path (txt, xml, json)')
    parser.add_argument('-v', '--verbose', dest='verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    ip = args.ip
    output = args.output
    verbose = args.verbose

    start_time = datetime.now()
    try:
        scan_result = scan(ip)
    except Exception as e:
        print(f"Error: {e}")
        return
    end_time = datetime.now()

    if verbose:
        print(f'Scan completed in {(end_time - start_time).seconds} seconds')

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
                    save_to_html(f, scan_result)
                else:
                    raise Exception(f"Error: Unsupported output file format: {format}. Supported formats: txt, xml, json, csv, html")
            except Exception as e:
                print(f"Error saving to file format {format}: {e}")
