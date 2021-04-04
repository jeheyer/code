#!/usr/bin/env python

def ReadWebFile(url, time_range, filter = None):

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
    
    matches = []

    for line in all_lines:
        timestamp = int(line[:10])
        if timestamp <  time_range[0]:
            continue
        if timestamp >  time_range[1]:
            break
        if AnalyzeLine(line, filter):
            matches.append(line)

    return matches

def ReadLocalFile(filename, time_range, filter = None):
    
    matches = []

    try:
        fh = open(filename, "r")
    except:
        raise Exception("ERROR: could not read log file '" + filename + "'")
    
    for line in fh:
        timestamp = int(line[:10])
        if timestamp <  time_range[0]:
            continue
        if timestamp >  time_range[1]:
            break
        if AnalyzeLine(line, filter):
            matches.append(line)
    
    return matches

def AnalyzeLine(line,filter = None):

    if filter:    
        if filter in line:
            #lines.append(line.split())
             return line
    else:
        #lines.append(line.split())
        return line
    return 
  
def GetData():

    from datetime import datetime

    #now = math.floor(time.time())
    now = 1617379601
    time_range = (now - 3600, now)

    hostnames = []
    for _ in range(1,5):
        hostnames.append('gcp-prox01-p00{}'.format(_))

    fields = ['timestamp','elapsed','client_ip','code','bytes','method','url','rfc931','peer_status','type']

    entries = []
    reporters = {}; client_ips = {}; usernames = {}; codes = {}
    for hostname in hostnames:
        filter = None
        _ = ReadLocalFile("/mnt/web/buckets/j5-org/temp/" + hostname + ".log", time_range, filter)
        #lines = ReadWebFile("http://j5-org.storage.googleapis.com/temp/" + hostname + ".log", time_range)
        reporters[hostname] = len(_)
        #print(reporters[hostname])
        entries.extend(_)
        #for line in lines:
        #for i in range(len(lines)-1, 0, -1):
            #_ = lines[i]
            #_ = lines[i].split()
            #lines.append(parts)
    #return data[0:3], reporters
    #newest_first = sorted(data, key=lambda x: x[0], reverse=True)
    #return newest_first[0:3], reporters
    #data = []
    #return entries, reporters
    
    newest_first = sorted(entries, key=lambda x: x[0:10], reverse=True)
    #return newest_first, reporters
    data = []
    #for i in range(len(entries)-1, 0, -1):
    for line in newest_first:
        _ = line.split()
        #print(entries[i])
        #_ = entries[i]
        #print(_[0])
        client_ip = _[2]
        client_ips[client_ip] = client_ips[client_ip]+1 if client_ip in client_ips else 1
        
        code = _[3]
        codes[code] = codes[code]+1 if code in codes else 1

        #if client_ip in client_ips:
        #    client_ips[client_ip] += 1
        #else:
        #    client_ips[client_ip] = 1
        #entry = {'reporter': file, 'data': line}
        #_.insert(0, hostname)
        #data.append(_)
        datetimestr = datetime.fromtimestamp(int(_[0][0:10]), tz=None)
        _[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        data.append(dict(zip(fields, _)))

    return data, reporters, client_ips, codes


