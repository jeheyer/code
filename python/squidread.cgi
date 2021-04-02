#!/usr/bin/env python

from squidread import *

if __name__ == '__main__':

    import sys, time, os, json, traceback

    sys.stderr = sys.stdout

    start_time = time.time()

    try:
        data, reporters = GetData()

        if 'REQUEST_METHOD' in os.environ:
            output = json.dumps(data[0:10], indent=2)
            print("Status: 200")
            print("Content-Length: {}".format(len(output)+1))
            print("Cache-Control: no-cache")
            print("Content-Type: application/json; charset=UTF-8\n")
            print(output)
        else:
            print("Status: 200")
            print("Content-Type: text/plain; charset=UTF-8\n")
            print("Total lines read:", len(data))
            print("seconds_to_execute:", round((time.time() - start_time), 3))
            for reporter, hitcount in reporters.items():
                print(reporter, ":", hitcount)
            #for _ in data:
            #    print(_['timestamp'], _['reporter'])
            print(data[0])
            print(data[-1])

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)
