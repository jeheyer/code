
class HTTPRequest():

    def __init__(self, env_vars = {}):

        from urllib import parse

        self.host = env_vars.get('HTTP_HOST', 'localhost')
        self.path = env_vars.get('REQUEST_URI', '/').split('?')[0]
        self.request_uri = env_vars.get('REQUEST_URI', None)
        if not self.request_uri:
            self.request_uri = env_vars.get('RAW_URI', self.path)
        self.query_string = dict(parse.parse_qsl(parse.urlsplit(str(self.request_uri)).query))
        self.server_port = env_vars.get('SERVER_PORT', 80)
        self.server_protocol = env_vars.get('SERVER_PROTOCOL', None)
        self.server_software = env_vars.get('SERVER_SOFTWARE', 'Unknown')

        self.client_ip = GetClientIP(env_vars)

        # Check for HTTPS on the Front end
        self.front_end_https = False
        if env_vars.get('HTTP_X_FORWARDED_PROTO', 'http') == "https":
            self.front_end_https = True
        if env_vars.get('HTTP_X_FORWARDED_SSL', False):
            self.front_end_https = True
        if env_vars.get('HTTPS', False) == True or self.server_port == 443:
            self.front_end_https = True

        # Google App Engine
        if 'HTTP_X_APPENGINE_USER_IP' in env_vars:
            self.client_city = env_vars.get('HTTP_X_APPENGINE_CITY', None)
            self.client_region = env_vars.get('HTTP_X_APPENGINE_REGION', None)
            self.client_country = env_vars.get('HTTP_X_APPENGINE_COUNTRY', None)

        # Flask
        #'host': request.host.split(':')[0],
        #'path': "/" + path,
        #'query_string': request.args,
        #request.user_agent.string

        self.user_agent = env_vars.get('HTTP_USER_AGENT', 'Unknown')

def GetClientIP(env_vars = None):

    import socket

    # Nginx
    if 'HTTP_X_REAL_IP' in env_vars:
        return env_vars['HTTP_X_REAL_IP']

    # AWS Lambda
    if 'requestContext' in env_vars: 
        return env_vars['requestContext']['identity']['sourceIp']

    # Google App Engine
    if 'HTTP_X_APPENGINE_USER_IP' in env_vars:
        return env_vars['HTTP_X_APPENGINE_USER_IP']

    if 'HTTP_X_FORWARDED_FOR' in env_vars:
        x_fwd_for = env_vars['HTTP_X_FORWARDED_FOR']
        if ", " in x_fwd_for:
            # Get a list of IPs addresses used by this web server hostname
            server_ips = socket.gethostbyname(env_vars.get('HTTP_HOST', "localhost"))
            x_fwd_for_ips =  x_fwd_for.split(", ")
            for _ in range(len(x_fwd_for_ips)):
                if x_fwd_for_ips[_] in server_ips:
                    # Use last IP address before the IP of this web server
                    return x_fwd_for_ips[_-1]

    # Last resort
    return env_vars.get('REMOTE_ADDR', "127.0.0.1")

