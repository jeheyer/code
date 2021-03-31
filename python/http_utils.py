
def GetClientIP(env_vars):

    import socket

    if env_vars.get('HTTP_X_REAL_IP', None):
        return env_vars['HTTP_X_REAL_IP']

    if env_vars.get('HTTP_X_FORWARDED_FOR', None):
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

