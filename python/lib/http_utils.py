
class HTTPRequest():

    def __init__(self, env_vars = {}, request = None, event = None):

        from urllib import parse

        self.headers = {}
        self.headers['x-forwarded-proto'] = "http"
        self.client_ip = None
        self.user_agent = None
        self.remote_addr = None
        self.server_port = None
        self.server_software = "Unknown"
        self.front_end_https = False

        # Parse environment variables dictionary
        if env_vars:

            if 'requestContext' in env_vars:
                # AWS Lambda
                self.headers =  event['multiValueHeaders'] if 'multiValueHeaders' in event else event['headers']
                self.host = self.headers['host']
                self.method = event['httpMethod']
                self.path = event['path']
                self.query_fields = event['queryStringParameters']
                self.client_ip = event['requestContext']['identity']['sourceIp']
                self.server_software = "awselb"

            else:
                # Standard WSGI or CGI web server
                self.host = env_vars.get('HTTP_HOST', 'localhost')
                self.method = env_vars.get('REQUEST_METHOD', 'GET')
                self.path = env_vars.get('REQUEST_URI', '/').split('?')[0]
                self.request_uri = env_vars.get('REQUEST_URI', None)
                if not self.request_uri:
                    self.request_uri = env_vars.get('RAW_URI', self.path)
                self.query_fields = dict(parse.parse_qsl(parse.urlsplit(str(self.request_uri)).query))
                self.server_protocol = env_vars.get('SERVER_PROTOCOL', None)
                if self.server_protocol:
                    self.http_version = self.server_protocol.split('/')[1]
                self.server_software = env_vars.get('SERVER_SOFTWARE', 'Unknown')
                self.server_port = env_vars.get('SERVER_PORT', 80)
                self.remote_addr = env_vars.get('REMOTE_ADDR', "127.0.0.1")
                self.headers['user-agent'] = env_vars.get('HTTP_USER_AGENT', 'Unknown')
                self.headers['x-forwarded-for'] = env_vars.get('HTTP_X_FORWARDED_FOR', None)
                self.headers['x-forwarded-proto'] = env_vars.get('HTTP_X_FORWARDED_PROTO', 'http')
                self.headers['x-forwarded-ssl']  = env_vars.get('HTTP_X_FORWARDED_SSL', False)
                self.headers['x-forwarded-port'] = env_vars.get('SERVER_PORT', None)
                self.headers['x-real-ip'] = env_vars.get('HTTP_X_REAL_IP', "127.0.0.1")

            if not self.server_port:
                self.server_port = self.headers.get('x-forwarded-port', 0)

            # Special headers for Google App Engine or GCP External HTTP/HTTPS load balancers
            if 'HTTP_X_APPENGINE_USER_IP' in env_vars:
                self.client_city = env_vars.get('HTTP_X_APPENGINE_CITY', None)
                self.client_region = env_vars.get('HTTP_X_APPENGINE_REGION', None)
                self.client_country = env_vars.get('HTTP_X_APPENGINE_COUNTRY', None)
                self.client_ip = env_vars.get('HTTP_X_APPENGINE_USER_IP', None)

        # Parse Request object
        if request:

            self.method = request.method

            # Quart
            if request and 'quart' in str(request.__class__):
                #self.vars = str(vars(request))
                for _ in request.headers.items():
                    self.headers[_[0].lower()] = _[1]
                self.host = request.host.split(':')[0]
                self.path = request.path
                self.query_fields = request.args
                self.remote_addr = request.remote_addr
                self.http_version = request.http_version
                self.server_protcol = "HTTP/" + request.http_version
                self.server_port = request.server[1]

            # FastAPI / Starlette 
            if request and 'starlette' in str(request.__class__):
                self.headers = request.headers
                self.host = request.headers['host'].split(':')[0]
                self.path = request.url.path
                self.query_fields = dict(request.query_params)
                self.remote_addr = request.client.host
                if 'http_version' in request:
                    self.http_version = request['http_version']
                    self.server_protocol = "HTTP/" + request['http_version']
                if 'server' in request:
                    self.server_port = request['server'][1]

        # Set handy variables
        self.user_agent = self.headers.get('user-agent', "Unknown")

        # Check various ways of indicating HTTPS is being used on frontend
        if self.headers['x-forwarded-proto'] == "https" or 'x-forwarded-ssl' in self.headers:
            self.front_end_https = True
        if self.headers.get('x-appengine-https', "off") == "on":
            self.front_end_https = True
        if self.server_port == 443 or self.server_port == 8443:
            self.front_end_https = True

        # Determine client IP if hasnt been determined already
        if not self.client_ip:
            self.client_ip = self.DetermineClientIP()

    def DetermineClientIP(self):

        if 'x-appengine-user-ip' in self.headers:
            return self.headers['x-appengine-user-ip']

        if 'x-real-ip' in self.headers and self.headers['x-real-ip'] != "127.0.0.1":
            return self.headers['x-real-ip']

        if 'x-forwarded-for' in self.headers:
            _ = self.headers['x-forwarded-for']
            if ", " in _:
                return _.split(", ")[-2]
            else:
                return _

        # Last resort
        if self.remote_addr:
            return self.remote_addr

