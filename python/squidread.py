#!/usr/bin/env python3

def GetSquidData(host = "localhost", ** options):

    from datetime import datetime
    from logfile import LogFile

    import time
    start_time = time.time()
    
    log = LogFile("/web/{}.log".format(host))

    data = []
    fields = ['timestamp', 'elapsed', 'client_ip', 'code', 'bytes', 'method', 'url', 'rfc931', 'peer_status', 'type']
    for _ in log.contents:
        # Change first entry from timestamp to datetime
        datetimestr = datetime.fromtimestamp(int(_[0].split(".")[0]), tz=None)
        _[0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
        # Change from list to dictionary
        data.append(dict(zip(fields, _)))

    return data      

    return {
       'lines_read': log.num_lines,
       'entries_processed': len(log.contents),
       'seconds_to_execute': round((time.time() - start_time), 3)
    }


if __name__ == '__main__':

    import sys, os, json, traceback, time
    from datetime import datetime

    sys.stderr = sys.stdout

    start_time = time.time()

    try:
        entries = []; total_lines = 0
        for host in ["gcp-prox01-p002", "gcp-prox01-p004"]:
            #lines = ReadFromFile("/web/" + host + ".log")
            #lines = ReadFromHTTPS("j5-org.storage.googleapis.com", "/temp/" + host + ".log")
            #lines = ReadFromGoogleCloudStorage("j5-org", "temp/" + host + ".log")
            #lines = ReadFromGoogleCloudStorage("otc-core-network-prod", "squid/logs/" + host + ".log")
            #total_lines += len(lines)
            entries.extend(GetSquidData(host))
            #entries.extend(lines)
            
        if True:
            data = []
            print("Content-Type: text/json; charset=UTF-8\n")
            fields = ['timestamp', 'elapsed', 'client_ip', 'code', 'bytes', 'method', 'url', 'rfc931', 'peer_status', 'type']
            for _ in entries:
                datetimestr = datetime.fromtimestamp(int(_['data'][0].split(".")[0]), tz=None)
                _['data'][0] = datetimestr.strftime("%d-%m-%y %H:%M:%S")
                data.append(dict(zip(fields, _['data'])))

        print("lines read:", total_lines)
        print("entries processed:", len(data))
        print("seconds_to_execute:", round((time.time() - start_time), 3))

    except Exception as e:
        if 'REQUEST_METHOD' in os.environ:
            print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit = 3)


