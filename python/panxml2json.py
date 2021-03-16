#!/usr/bin/env python3

temp_xml_file = "/tmp/xmlapioutput.xml"

def ReadDevices():

    devices = []

    fh = open("paloaltos.csv", "r")
    while fh:
        line = fh.readline().rstrip()
        if line:
            [hostname, api_key] = line.split(",")
            devices.append({'hostname': hostname, 'api_key': api_key})
        else:
            break
    fh.close()

    return devices

def MakeXMLAPICall(hostname, api_key, cli_command):

    import subprocess

    xml_command = ""
    words = cli_command.split(" ")
    for i in range(len(words)):
        xml_command += "<"+ words[i] +">"
    for i in range(len(words)-1, -1,-1):
        xml_command += "</"+ words[i] +">"

    api_command = "../pan-python-0.16.0/bin/panxapi.py -h {} -K \"{}\" -x -o \"{}\"".format(hostname, api_key, xml_command)
    output = subprocess.check_output(api_command, shell=True)
    lines = output.decode("utf-8").splitlines()

    fh = open(temp_xml_file, "w")
    try:
        for line in lines:
            fh.write(line + "\n")
    finally:
        fh.close()

def ReadXMLFile():

    import xml.etree.ElementTree
    import os

    entries = []
    _ = xml.etree.ElementTree.iterparse(temp_xml_file, events=('end', ))

    for event, elem in _:
        if elem.tag == 'entry':
            entry = {}
            for child in elem.iter():

                try:
                    value = elem.find(child.tag).text
                    if value.isnumeric():
                        value = int(value)
                    else:
                        value = value.rstrip()
                except:
                    value = None

                if child.tag != "entry":
                    key = child.tag.replace("-", "_")
                    entry[key] = value

            entries.append(entry)

     # Cleanup Temp XML file
    os.remove(temp_xml_file)

    return entries

def main(cli_command = None, specific_hostname = None):

    data = []

    try:
        devices = ReadDevices()

        for device in devices:
            if specific_hostname and device['hostname'] != specific_hostname:
               continue
            MakeXMLAPICall(device['hostname'], device['api_key'], cli_command = cli_command)
            data.extend(ReadXMLFile())
        return data
    except Exception as e:
        raise(e)

if __name__ == '__main__':

    import sys, os, traceback, json

    sys.stderr = sys.stdout

    data = []

    try:

        query_fields = {}

        if os.environ.get('REQUEST_METHOD'):

            import cgi

            query_fields_objects = cgi.FieldStorage()
            for key in query_fields_objects:
                value = query_fields_objects[key].value
                query_fields[key] = str(value)

            if 'request_type' in query_fields:

                if query_fields['request_type'] == "get-device-list":
                    devices = ReadDevices()
                    for device in devices:
                        data.append(dict(hostname = device['hostname']))

                command_list = {
                    'show_routing_route': "Route Table",
                    'show_vpn_ike-sa': "IKE SAs",
                    'show_vpn_ipsec-sa': "IPSEC SAs",
                    'show_global-protect-gateway_current-user': "GlobalProtect Sessions",
                    'show_vpn_tunnel': "Configured VPN Tunnels"
                }

                if query_fields['request_type'] == "list-commands":
                    for key, value in command_list.items():
                        data.append({key: value})

            if not 'device_name' in query_fields:
                query_fields['device_name'] = None

        else:
            query_fields['command'] = "show_global-protect-gateway_current-user"
            query_fields['device_name'] = None

        if 'command' in query_fields:
            data = main(query_fields['command'].replace("_", " "), query_fields['device_name'])

        if os.environ.get('REQUEST_METHOD'):
            print("Content-Type: application/json; charset=UTF-8\n")
            print(json.dumps((data), indent=3))
        else:
            print(data)

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit = 3)

    sys.exit()

