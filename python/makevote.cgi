#!/usr/bin/env python3

def main(request):

    from database import MySQLDatabase
    return

# Primary entry point
if __name__ == '__main__':

    import sys, os, traceback

    sys.stderr = sys.stdout

    try:
        if os.environ.get('REQUEST_METHOD') == 'POST':
            main()

        print("Status: 302\nLocation: pollresults.html\n")

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)

