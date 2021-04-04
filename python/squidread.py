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
    
    fields = ['timestamp','elapsed','client_ip','code','bytes','method','url','rfc931','peer_status','type']
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
        result = AnalyzeLine(line, filter)
        if result:
            matches.append(result)
            #_ = line.split()
            #matches.append(dict(zip(fields, _)))
    
    return matches

def AnalyzeLine(line,filter = None):
    
    from datetime import datetime
    fields = ['timestamp','elapsed','client_ip','code','bytes','method','url','rfc931','peer_status','type']

    if filter:    
        if filter in line:
            #lines.append(line.split())
            _ = line.split()
            #datetimestr = datetime.fromtimestamp(int(_[0][0:10]), tz=None)
            #_[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
            return dict(zip(fields, _))
    else:
        #lines.append(line.split())
        _ = line.split()
        #datetimestr = datetime.fromtimestamp(int(_[0][0:10]), tz=None)
        #_[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        return dict(zip(fields, _))
    return 
  
def GetData():

    from datetime import datetime

    #now = math.floor(time.time())
    now = 1617379601
    time_range = (now - 3600 , now)

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
        
        entries.extend(_)
        
        #for i in range(len(_)-1, 0, -1):
        #for line in _:
        #    _ = line.split()
        #    client_ip = _[2]
        #    client_ips[client_ip] = client_ips[client_ip]+1 if client_ip in client_ips else 1    
        #    code = _[3]
        #    codes[code] = codes[code]+1 if code in codes else 1
        #    datetimestr = datetime.fromtimestamp(int(_[0][0:10]), tz=None)
        #    _[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        #    entries.append(dict(zip(fields, _)))

    #entries = sorted(entries, key=lambda x: x['timestamp'], reverse=True)
    #return entries, reporters, client_ips, codes
            #lines.append(parts)
    #return data[0:3], reporters
    #newest_first = sorted(data, key=lambda x: x[0], reverse=True)
    #return newest_first[0:3], reporters
    #data = []
    #return entries, reporters
    return entries, reporters, client_ips, codes
    newest_first = sorted(entries, key=lambda x: x['timestamp'], reverse=True)
    del entries
    return newest_first, reporters, client_ips, codes
    #return newest_first, reporters, client_ips, codes
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

    del newest_first
    return data, reporters, client_ips, codes


