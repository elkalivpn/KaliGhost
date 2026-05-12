#!/usr/bin/env python3
"""Convierte salida XML de nmap a CSV para análisis"""

import xml.etree.ElementTree as ET
import csv
import sys

def nmap_xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    hosts = []
    for host in root.findall('host'):
        addr = host.find('address').get('addr')
        hostname_elem = host.find('hostnames/hostname')
        hostname = hostname_elem.get('name') if hostname_elem is not None else ''
        
        for port in host.findall('ports/port'):
            portid = port.get('portid')
            protocol = port.get('protocol')
            state = port.find('state').get('state')
            service = port.find('service')
            service_name = service.get('name') if service is not None else ''
            product = service.get('product') if service is not None else ''
            version = service.get('version') if service is not None else ''
            
            hosts.append({
                'ip': addr,
                'hostname': hostname,
                'port': portid,
                'protocol': protocol,
                'state': state,
                'service': service_name,
                'product': product,
                'version': version
            })
    
    # Write CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ip', 'hostname', 'port', 'protocol', 'state', 'service', 'product', 'version'])
        writer.writeheader()
        writer.writerows(hosts)
    
    print(f"✅ {len(hosts)} ports written to {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: nmap_to_csv.py <nmap.xml> <output.csv>")
        sys.exit(1)
    nmap_xml_to_csv(sys.argv[1], sys.argv[2])