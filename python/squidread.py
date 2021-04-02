#!/usr/bin/env python

def ReadWebFile(url, time_range):

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

def ReadLocalFile(filename, time_range, filter = None):
    
    lines = []
    
    try:
        fh = open(filename, "r")
    except:
        raise Exception("ERROR: could not read log file '" + filename + "'")
    
    for line in fh:
        parts = line.split()
        timestamp = float(parts[0])
        if timestamp >= time_range[0] and timestamp <= time_range[1]:
            if filter:    
                if filter in line:
                   lines.append(parts)
            else:
                lines.append(parts)
    
    return lines

def GetData():

    from datetime import datetime

    #now = math.floor(time.time())
    now = 1617379777
    time_range = (now - 120, now)

    data = []
    client_ips = {}
    reporters = {}
    files = ['gcp-prox01-p001.log','gcp-prox01-p002.log', 'gcp-prox01-p003.log', 'gcp-prox01-p004.log', 'gcp-prox01-p005.log']
    for file in files:
        lines = ReadLocalFile("/mnt/web/buckets/j5-org/temp/" + file, time_range)
        #lines = ReadWebFile("http://j5-org.storage.googleapis.com/temp/" + file, threshold)
        #print("lines read from {}: {}".format(file, len(lines)))
        reporters[file] = len(lines)
        for i in range(len(lines)-1, 0, -1):
            _ = lines[i]
        #for _ in lines:
            #print(_[0])
            #parts = lines[_]
          #  if int(parts[0].split('.')[0]) > threshold:
            client_ip = _[2]
            if client_ip in client_ips:
                client_ips[client_ip] += 1
            else:
                client_ips[client_ip] = 1
            #entry = {'reporter': file, 'data': line}
            _.insert(0, file)
            data.append(_)

    newest_first = sorted(data, key=lambda x: x[0], reverse=True)
    fields = ['reporter','timestamp','elapsed','client_ip','code','bytes','method','url','rfc931','peer_status','type']

    new = []
    for _ in newest_first:
        datetimestr = datetime.fromtimestamp(int(_[1].split('.')[0]), tz=None)
        _[1] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        new.append(dict(zip(fields, _)))

    return new, reporters

