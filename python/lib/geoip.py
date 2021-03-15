import geoip2.database
import json
import math

class GeoIP:

    def __init__(self, ipv4_address):

        self.hostname = None
        self.ipv4_address = ipv4_address
        self.lat = 0; self.lng = 0
        self.city = None
        self.region_code = None
        self.region_name = None
        self.country_code = None
        self.country_name = None

        # Check for loopbacks
        if self.hostname == "localhost" or self.ipv4_address == "127.0.0.1":
            return None

        # Get City Information
        with geoip2.database.Reader('/var/cache/mmdb/GeoIP2-City.mmdb') as reader:
            try:
                response = reader.city(ipv4_address)
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
                self.asn = response.autonomous_system_number
                self.org = response.autonomous_system_organization
                self.isp = response.isp

    def __str__(self):

        return json.dumps(vars(self))
