class GeoIPList:


    def __init__(self, ip_list):

        import geoip2.database
        
        self.geoips = []

        city_reader = geoip2.database.Reader('/var/cache/mmdb/GeoIP2-City.mmdb')
        isp_reader = geoip2.database.Reader('/var/cache/mmdb/GeoIP2-ISP.mmdb')

        for _ in ip_list:
            geoip = Host(_)
            if geoip.is_routable:
                try:
                    # Get City Information
                    response = city_reader.city(geoip.ipv4_address)
                except:
                    continue
                if response:
                    geoip.lat = round(response.location.latitude, 4)
                    geoip.lng = round(response.location.longitude, 4)
                    geoip.city = response.city.name
                    geoip.country_code = response.country.iso_code.upper()
                    geoip.country_name = response.country.name
                    if len(response.subdivisions) > 0:
                        geoip.region_code = str(response.subdivisions[0].iso_code)
                        geoip.region_name = str(response.subdivisions[0].name)
                try:
                    # Get ISP Information
                    response = isp_reader.isp(geoip.ipv4_address)
                except:
                    continue
                if response:
                    geoip.isp_name = response.isp
                    geoip.isp_asn = response.autonomous_system_number
                    geoip.isp_org = response.autonomous_system_organization
            self.geoips.append(vars(geoip))
        city_reader.close()
        isp_reader.close()

class Host:

    def __init__(self, param):

        import ipaddress
        import socket

        self.ipv4_address = None
        self.ipv6_address = None
        self.hostname = None
        self.is_routable = False

        try:
            ip = ipaddress.ip_address(param)
            self.ipv4_address = str(ip)
            if ip.is_private or ip.is_reserved:
                return 
            else:
                self.is_routable = True
                # Try to get reverse DNS hostname
                #self.hostname = socket.gethostbyaddr(str(ip))[0][0:64]
        except:
            self.hostname = None

        if not self.ipv4_address:
            # Try getting IP via forward DNS Lookup
            try:
                self.hostname = param
                ip = ipaddress.ip_address(socket.gethostbyname(self.hostname))
                self.ipv4_address = socket.gethostbyname(str(ip))
            except:
                self.ipv4_address = None
                return


