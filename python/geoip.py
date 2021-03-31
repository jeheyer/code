
import ipaddress
import geoip2.database

class GeoIP:

    def __init__(self, param):

        import socket

        self.ipv4_address = None; self.ipv6_address = None

        try:
            ip = ipaddress.ip_address(param)
            self.ipv4_address = str(ip)
            if ip.is_private or ip.is_reserved:
                return 
            else:
                self.hostname = socket.gethostbyaddr(str(ip))[0][0:64]
        except:
            self.hostname = None

        if not self.ipv4_address:
            # Try getting IP via DNS Lookup
            try:
                self.hostname = param
                ip = ipaddress.ip_address(socket.gethostbyname(self.hostname))
                self.ipv4_address = socket.gethostbyname(str(ip))
            except:
                self.ipv4_address = None
                return

        self.lat = 0; self.lng = 0; self.city = None
        self.region_code = None; self.region_name = None
        self.country_code = None; self.country_name = None

        # Check for loopbacks
        if self.ipv4_address == "127.0.0.1" or self.ipv6_address == "::1":
            return

        # Get City Information
        with geoip2.database.Reader('/var/cache/mmdb/GeoIP2-City.mmdb') as reader:
            try:
                response = reader.city(self.ipv4_address)
            except:
                return
            if response:
                self.lat = round(response.location.latitude, 4)
                self.lng = round(response.location.longitude, 4)
                self.city = response.city.name
                self.country_code = response.country.iso_code.upper()
                self.country_name = response.country.name
                if len(response.subdivisions) > 0:
                    self.region_code = str(response.subdivisions[0].iso_code)
                    self.region_name = str(response.subdivisions[0].name)

        # Get ISP information
        with geoip2.database.Reader('/var/cache/mmdb/GeoIP2-ISP.mmdb') as reader:
            try:
                response = reader.isp(self.ipv4_address)
            except:
                return
            if response:
                self.isp_name = response.isp
                self.isp_asn = response.autonomous_system_number
                self.isp_org = response.autonomous_system_organization

    def __str__(self):

        import json

        return json.dumps(vars(self))
