from geoip import *
g = GeoIPList(['63.249.99.251', '127.0.0.1', '10.10.10.10', '66.170.1.10'])
for _ in g.geoips:
    print(vars(_))
