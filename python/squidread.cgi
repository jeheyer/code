#!/usr/bin/python3 

import time

def ReadWebFile(url, threshold):

    import http.client
    import ssl

    timeout = 5
    
    try:
        [proto, _] = url.split("://")
        hostname = _.split("/")[0]
        path = _[len(hostname):]
        if proto == "https":
            ssl_context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(hostname, port = 443, timeout = timeout, context = ssl_context)
        else:
            conn = http.client.HTTPConnection(hostname, port = 80, timeout = timeout)
        
        conn.request(method = "GET", url = path)  
        resp = conn.getresponse()
        all_lines = resp.read().decode("utf-8").rstrip().splitlines()
            
    except Exception as e:
        return e      

    conn.close()
    
    lines = []
    for _ in all_lines:
        if float(_.split(" ")[0]) > threshold:
            lines.append(_.split())
    
    return lines

def ReadLocalFile(filename, threshold, filter = None):
    
    lines = []
    
    try:
        fh = open(filename, "r")
    except:
        raise Exception("ERROR: could not read log file '" + filename + "'")
    
    for line in fh:
        if float(line.split(" ")[0]) > threshold:
            if filter:    
                if filter in line:
                   lines.append(line.split())
            else:
                lines.append(line.split())
    
    return lines

fields = ['timestamp', 'elapsed', 'client_ip', 'code', 'bytes', 'method', 'url', 'rfc931', 'peer_status', 'type']

#now = math.floor(time.time())
now = 1616878438
threshold = now - 3600 * 4

from datetime import datetime

print("Content-Type: text/plain\n")

start_time = time.time()
data = []
files = ['gcp-prox01-p001.log','gcp-prox01-p002.log', 'gcp-prox01-p003.log', 'gcp-prox01-p004.log', 'gcp-prox01-p005.log']
client_ips = {}
for file in files:
    lines = ReadLocalFile("/web/" + file, threshold)
    #lines = ReadWebFile("http://j5-org.storage.googleapis.com/temp/" + file, threshold)
    print("lines read from {}: {}".format(file, len(lines)))
    for _ in range(len(lines)-1, 0, -1):
        parts = lines[_]
        if int(parts[0].split('.')[0]) > threshold:
            client_ip = parts[2]
            if client_ip in client_ips:
                client_ips[client_ip] += 1
            else:
                client_ips[client_ip] = 1
            #entry = {'reporter': file, 'data': line}
            datetimestr = datetime.fromtimestamp(int(parts[0].split(".")[0]), tz=None)
            parts[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
            data.append(dict(zip(fields, parts)))
        else:
            break

print("Total lines read:", len(data))
print("seconds_to_execute:", round((time.time() - start_time), 3))

print("Unique client IPs:", len(client_ips), "\nTop 10 client IPs and hit count:")
sorted_client_ips = sorted(client_ips.items(), key=lambda item: item[1], reverse = True)
for i in range(0,5):
    client_ip = sorted_client_ips[i]
    print(client_ip[0] ,":", client_ip[1])

import random
print(random.choice(data))
