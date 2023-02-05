import scapy.all as scapy
import argparse
from datetime import datetime
import socket

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = scapy.srp(arp_request/broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in arp_request_broadcast:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "hostname": socket.gethostbyaddr(element[1].psrc)[0]}
        clients_list.append(clients_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\t MAC Address \t\t Hostname\n-----")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"] + "\t\t" + client["hostname"])

def main():
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('-t', '--target', dest='ip', help='IP address or range to scan')
    parser.add_argument('-o', '--output', dest='output', help='Output file name (txt, xml, json)')

    args = parser.parse_args()
    ip = args.ip
    output = args.output

    if not ip:
        print("[-] Error: Please specify an IP address or range to scan")
        return

    start_time = datetime.now()
    scan_result = scan(ip)
    end_time = datetime.now()

    print(f'Scan completed in {(end_time - start_time).seconds} seconds')

    if output:
        if output.endswith('.txt'):
            with open(output, 'w') as f:
                for client in scan_result:
                    f.write(f"IP: {client['ip']}\tMAC: {client['mac']}\tHostname: {client['hostname']}\n")
        elif output.endswith('.xml'):
            scapy.wrpcap(output, scan_result)
        elif output.endswith('.json'):
            import json
            with open(output, 'w') as f:
                json.dump(scan_result, f)
        else:
            print(f"[-] Error: Unsupported output file format: {output}")
    else:
        print_result(scan_result)

if __name__ == "__main__":
    main()