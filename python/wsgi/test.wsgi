import sys
#sys.path.append(r'/mnt/web/www/code/python/lib')
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'lib'))

def application(environ, start_response):
    status = '200 OK'

    output = u''
    output += u'sys.version = %s\n' % repr(sys.version)
    output += u'sys.prefix = %s\n' % repr(sys.prefix)
    for _ in sys.path:
       output += ":" + _

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output.encode('UTF-8')]
