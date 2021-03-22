#!/usr/bin/env python3

def ReadFromHTTPS(hostname, path):

    import http.client
    #import ssl

    lines = []

    try: 
        #ssl_context = ssl._create_unverified_context()
        #conn = http.client.HTTPSConnection(hostname, port = 443, timeout = 3, context = ssl_context)
        conn = http.client.HTTPConnection(hostname, port = 80, timeout = 3)
        conn.request(method = "GET", url = path)
        resp = conn.getresponse()
        lines = resp.read().decode("utf-8").rstrip().splitlines()
    except Exception as e:
        return e        
    conn.close()
    return lines

def ReadFromGoogleCloudStorage(bucket_name, file_name):

    from google.cloud import storage

    lines = []

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        return blob.download_as_string().decode("utf-8").rstrip().splitlines()
        #out_file = "/var/tmp/" + file_name.split("/")[-1]
        #blob.download_to_filename(out_file)
        #print(out_file)
    except Exception as e:
        raise(e)

    return lines

def ReadFromS3(bucket_name, file_name):

    import boto3
    return None

def ProcessBlob(source_name = None, lines = []):

    from datetime import datetime
    from time import time
    from math import floor

    #now = math.floor(time.time())
    now = 1614968742
    threshold = now - 60 * 30

    fields = ['timestamp', 'elapsed', 'client_ip', 'code', 'bytes', 'method', 'url', 'rfc931', 'peer_status', 'type']
    entries = []
    for l in range(len(lines)-1, 0, -1):
        line = lines[l]
        parts = line.split()
        if int(parts[0].split('.')[0]) > threshold:
            entry = {}
            entry['reporter'] = source_name
            for i in range(0,len(fields)):
                if i == 0:
                    datetimestr = datetime.fromtimestamp(int(parts[0].split(".")[0]), tz=None)
                    entry['timestamp'] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
                else:
                    entry[fields[i]] = parts[i]
            entries.append(entry)
        else:
            break

    return entries

def ReadFromFile(file_name):

    f = open(file_name)
    return f.readlines()

if __name__ == '__main__':

    import sys, os, json, traceback, time

    sys.stderr = sys.stdout

    start_time = time.time()

    try:
        data = []; total_lines = 0
        for host in ["gcp-prox01-p001", "gcp-prox01-p003"]:
            lines = ReadFromFile("/var/log/" + host + ".log")
            #lines = ReadFromHTTPS("j5-org.storage.googleapis.com", "/temp/" + host + ".log")
            #lines = ReadFromGoogleCloudStorage("j5-org", "temp/" + host + ".log")
            #lines = ReadFromGoogleCloudStorage("otc-core-network-prod", "squid/logs/" + host + ".log")
            total_lines += len(lines)
            data.extend(ProcessBlob(host, lines))
        
        if 'REQUEST_METHOD' in os.environ:
            print("Content-Type: text/json; charset=UTF-8\n")
            print(json.dumps(data, indent=3))
        else:
            print("lines read:", total_lines)
            print("entries processed:", len(data))
            print("seconds_to_execute:", round((time.time() - start_time), 3))

    except Exception as e:
        if 'REQUEST_METHOD' in os.environ:
            print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit = 3)


