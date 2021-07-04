
class HTTPRequest():

    def __init__(self, env_vars = {}, request = None, event = None):

        from urllib import parse

        self.headers = {}
        self.client_ip = None
        self.front_end_https = False

        # WSGI & CGI: Parse HTTP environment variables
        if env_vars:
            self.host = env_vars.get('HTTP_HOST', 'localhost')
            self.path = env_vars.get('REQUEST_URI', '/').split('?')[0]
            self.request_uri = env_vars.get('REQUEST_URI', None)
            if not self.request_uri:
                self.request_uri = env_vars.get('RAW_URI', self.path)
            self.query_fields = dict(parse.parse_qsl(parse.urlsplit(str(self.request_uri)).query))
            self.method = env_vars.get('REQUEST_METHOD', 'GET')
            self.server_protocol = env_vars.get('SERVER_PROTOCOL', None)
            self.server_software = env_vars.get('SERVER_SOFTWARE', 'Unknown')
            self.server_port = env_vars.get('SERVER_PORT', 80)
            self.remote_addr = env_vars.get('REMOTE_ADDR', "127.0.0.1")

            self.headers = {}
            self.headers['user-agent'] = env_vars.get('HTTP_USER_AGENT', 'Unknown')
            self.headers['x-forwarded-for'] = env_vars.get('HTTP_X_FORWARDED_FOR', None)
            self.headers['x-forwarded-proto'] = env_vars.get('HTTP_X_FORWARDED_PROTO', 'http')
            self.headers['x-forwarded-ssl']  = env_vars.get('HTTP_X_FORWARDED_SSL', False)
            self.headers['x-forwarded-port'] = env_vars.get('SERVER_PORT', 0)
            self.headers['x-real-ip'] = env_vars.get('HTTP_X_REAL_IP', "127.0.0.1")

            if self.headers['x-forwarded-proto'] == "https":
                self.front_end_https = True
            if env_vars.get('HTTP_X_FORWARDED_SSL', False):
                self.front_end_https = True
            if env_vars.get('HTTPS', False) == True or self.server_port == 443:
                self.front_end_https = True

            # Special headers for Google App Engine
            if 'HTTP_X_APPENGINE_USER_IP' in env_vars:
                self.client_city = env_vars.get('HTTP_X_APPENGINE_CITY', None)
                self.client_region = env_vars.get('HTTP_X_APPENGINE_REGION', None)
                self.client_country = env_vars.get('HTTP_X_APPENGINE_COUNTRY', None)
                self.client_ip = env_vars.get(['HTTP_X_APPENGINE_USER_IP'], None)

        # AWS Lambda
        if 'requestContext' in env_vars:
            self.headers =  event['multiValueHeaders'] if 'multiValueHeaders' in event else event['headers']
            self.host = self.headers['host']
            self.path = event['path']
            self.client_ip = event['requestContext']['identity']['sourceIp']
            self.user_agent = self.headers['user-agent']
            if self.headers['x-forwarded-proto'] == "https":
                self.front_end_https = True
            self.server_port = self.headers['x-forwarded-port']

        # FastAPI / Starlette
        if request:
            #self.vars = str(vars(request))
            self.headers = request.headers
            self.host = request.headers['host'].split(':')[0]
            self.path = request.url.path
            self.query_fields = dict(request.query_params)
            self.method = request.method
            self.server_port = request['server'][1]
            self.server_protocol = "HTTP/" + request['http_version']
            self.remote_addr = request.client.host
            if 'x-forwarded-proto' in self.headers and self.headers['x-forwarded-proto'] == "https":
                self.front_end_https = True
            self.user_agent = request.headers['user-agent']
            #if 'x-real-ip' in request.headers:
            #    self.client_ip = request.headers['x-real-ip']
            #elif 'x-forwarded-for' in request.headers:
            #    self.client_ip = self.headers['x-forwarded-for'][-2]
            #else:
            #    self.client_ip = request.client.host

        if not self.client_ip:
            self.client_ip = self.DetermineClientIP()

    def DetermineClientIP(self):

        import socket

        if 'x-real-ip' in self.headers:
            return self.headers['x-real-ip']

        if 'x-forwarded-for' in self.headers:
            if ", " in self.headers['x-forwarded-for']:
                return x_fwd_for_ips[-2]
                # Get a list of IPs addresses used by this web server hostname
                server_ips = socket.gethostbyname(self.host)
                x_fwd_for_ips =  x_fwd_for.split(", ")
                for _ in range(len(x_fwd_for_ips)):
                    if x_fwd_for_ips[_] in server_ips:
                        # Use last IP address before the IP of this web server
                        return x_fwd_for_ips[_]
                return x_fwd_for_ips[-2]

        # Last resort
        return self.remote_addr

