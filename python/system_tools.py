
def GetDNSServersFromToken(token="testing1234") -> dict:

    import re

    try:
        # Override if this is test token
        if token == "testing1234":
            dns_resolvers = [ "192.0.2.53", "198.51.100.53", "203.0.113.53" ]
        else:
            # Open the BIND log file for A record queries
            dns_resolvers = []
            dns_resolvers_hash = dict()
            bind_log_file = LogFile("/var/log/named/query.log", " IN A ")
            for line in bind_log_file.contents:
                if token in line[7]:
                    source_ip, source_port = line[6].split("#")
                    if not re.match("10.|192.168.", source_ip) and source_ip not in dns_resolvers_hash:
                        dns_resolvers_hash[source_ip] = True
                        dns_resolvers.append(source_ip)

        return dict(dns_resolvers=dns_resolvers)

    except Exception as e:
        raise Exception(e)


def GetConfig(type, key = None):

    import configparser

    # Read config file
    config = configparser.ConfigParser()
    config.read('/web/private/cfg/{}.cfg'.format(type))

    if key:
        return config[key]
    return config

def ReadFromHTTPS(hostname, path):

    import http.client
    import ssl

    lines = []

    try: 
        ssl_context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(hostname, port = 443, timeout = 3, context = ssl_context)
        #conn = http.client.HTTPConnection(hostname, port = 80, timeout = 3)
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

    from time import time
    from math import floor

    #now = math.floor(time.time())
    now = 1614968742
    threshold = now - 7200 

    entries = []
    for l in range(len(lines)-1, 0, -1):
        line = lines[l]
        parts = line.split()
        if int(parts[0].split('.')[0]) > threshold:
            entry = {'reporter': source_name, 'data': parts}
            #for i in range(0,len(fields)):
            #    if i == 0:
            #        datetimestr = datetime.fromtimestamp(int(parts[0].split(".")[0]), tz=None)
            #        entry['timestamp'] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
            #    else:
            #        entry[fields[i]] = parts[i]
            entries.append(entry)
        else:
            break

    return entries

def ReadFromFile(file_name):

    #import mmap

    lines = []
    f = open(file_name)
    return f.readlines()

    #with open(file_name, 'r+') as f:
    #    for line in f:
    #        lines.append(line)
    #return lines

    #with open(file_name, 'r') as f:
    #    for piece in read_in_chunks(f):
    #        lines.append(piece)

    #for line in open(file_name):
    #    lines.append(line)
    #return lines

    #with open(file_name, "r+") as f:
    #    map = mmap.mmap(f.fileno(), 0)
    #    map.close()

    #return lines

def ReadInput(file_name: str) -> (list, str):

    lines = []
    f = open(file_name)
    lines = f.readlines()

    file_ext = file_name.split(".")[-1]

    return (lines, file_ext)

def ConvertToDict(contents: list, file_type: str) -> list:

    data = []
    if file_type == "csv":
        for line in contents:
            line = line.rstrip()
            print(line)
            parts = line.split(",")
            obj = {}
            for i in range(0,len(parts)):
                obj[i] = parts[i]
            data.append(obj)

    return data

class LogFile():

    def __init__(self, filename, filter = None):

        self.filename = filename
        self.contents = []
        self.num_lines = 0
        self.ReadFile(filter)

    def ReadFile(self, filter = None):

        try:
            fh = open(self.filename,"r")
        except:
            raise Exception("ERROR: could not read log file '" + self.filename + "'")

        for line in fh:
            if filter:    
                if filter in line:
                    parts = line.split(" ")
                    self.contents.append(parts)
            else:
                parts = line.split(" ")
                self.contents.append(parts)
            self.num_lines += 1

        fh.close()

