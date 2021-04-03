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
    
    lines = []
    for line in all_lines:
        timestamp = int(line[:10])
        if timestamp <  time_range[0]:
            continue
        elif timestamp > time_range[1]:
            break
        else:
            if filter:    
                if filter in line:
                   lines.append(line)
            else:
                lines.append(line)

    return lines

def ReadLocalFile(filename, time_range, filter = None):
    
    lines = []

    try:
        fh = open(filename, "r")
    except:
        raise Exception("ERROR: could not read log file '" + filename + "'")
    
    for line in fh:
        timestamp = int(line[:10])
        if timestamp <  time_range[0]:
            continue
        elif timestamp > time_range[1]:
            break
        else:
            if filter:    
                if filter in line:
                   #lines.append(line.split())
                   lines.append(line)
            else:
                #lines.append(line.split())
                lines.append(line)
    
    return lines

def GetData():

    from datetime import datetime

    #now = math.floor(time.time())
    now = 1617379601
    time_range = (now - 7200, now)

    hostnames = []
    for _ in range(1,5):
        hostnames.append('gcp-prox01-p00{}'.format(_))

    fields = ['reporter','timestamp','elapsed','client_ip','code','bytes','method','url','rfc931','peer_status','type']

    data = []
    client_ips = {}
    reporters = {}
    for hostname in hostnames:
        #lines = ReadLocalFile("/mnt/web/buckets/j5-org/temp/" + hostname + ".log", time_range)
        lines = ReadWebFile("http://j5-org.storage.googleapis.com/temp/" + hostname + ".log", time_range)
        #print("lines read from {}: {}".format(file, len(lines)))
        reporters[hostname] = len(lines)
        #for line in lines:
        for i in range(len(lines)-1, 0, -1):
            #_ = lines[i]
            _ = lines[i].split()
            #lines.append(parts)
            
            
            client_ip = _[2]
            if client_ip in client_ips:
                client_ips[client_ip] += 1
            else:
                client_ips[client_ip] = 1
            #entry = {'reporter': file, 'data': line}
            _.insert(0, hostname)
            #data.append(_)
            datetimestr = datetime.fromtimestamp(int(_[1].split('.')[0]), tz=None)
            _[1] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
            data.append(dict(zip(fields, _)))

    return data, reporters
    newest_first = sorted(data, key=lambda x: x[0], reverse=True)
    

    new = []
    for _ in newest_first:
        datetimestr = datetime.fromtimestamp(int(_[1].split('.')[0]), tz=None)
        _[1] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        new.append(dict(zip(fields, _)))

    return new, reporters

