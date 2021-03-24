
def GetDNSServersFromToken(token = "testing1234"):

    from logfile import LogFile
    import re

    try:
        # Override if this is test token
        if token == "testing1234":
            dns_resolvers = [ "192.0.2.53", "198.51.100.53", "203.0.113.53" ]
        else:
            # Open the BIND log file for A record queries
            dns_resolvers = []
            dns_resolvers_hash = dict()
            bind_log_file = LogFile("/var/log/named/query.log", " IN A ")
            for line in bind_log_file.contents:
                if token in line[7]:
                    source_ip, source_port = line[6].split("#")
                    if not re.match("10.|192.168.", source_ip) and source_ip not in dns_resolvers_hash:
                        dns_resolvers_hash[source_ip] = True
                        dns_resolvers.append(source_ip)

        return dict(dns_resolvers = dns_resolvers)

    except Exception as e:
        raise Exception(e)


def GetConfig(type, key = None):

    import configparser

    # Read config file
    config = configparser.ConfigParser()
    config.read('/mnt/web/private/cfg/{}.cfg'.format(type))

    if key:
        return config[key]
    return config
