# dependencies:
#   geoIP2      https://github.com/maxmind/GeoIP2-python
#   maxminddb   https://pypi.python.org/pypi/maxminddb/
#   ipaddress   https://pypi.python.org/pypi/py2-ipaddress

# response.country.iso_code
# response.country.name
# response.subdivisions.most_specific.name
# response.subdivisions.most_specific.iso_code
# response.city.name
# response.postal.code
# response.location.latitude
# response.location.longitude

# string formatting https://docs.python.org/2/library/string.html#format-string-syntax

import re
import os
import geoip2.database
import sys

regex = re.compile(r'(?P<owner>\S+) (?P<bucket>\S+) (?P<time>\[[^]]*\]) (?P<ip>\S+) ' + 
r'(?P<requester>\S+) (?P<reqid>\S+) (?P<operation>\S+) (?P<key>\S+) ' + 
r'(?P<request>"[^"]*"|-) (?P<status>\S+) (?P<error>\S+) (?P<bytes>\S+) ' + 
r'(?P<size>\S+) (?P<totaltime>\S+) (?P<turnaround>\S+) (?P<referrer>"[^"]*"|-) ' +
r'(?P<useragent>"[^"]*"|-) (?P<version>\S)')

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
directory = "LOGS"

for filename in os.listdir(directory):
    f=open(directory + '/' + filename, 'r')
    for line in f:
        match = regex.match(line)
        if match is None:
            print('********\nFailed to parse - fix your regex!\n********\n' + line)
            raw_input('Press enter to continue')
            continue
            
        dict = match.groupdict()
        ip = dict.get("ip", "none")
        response = reader.city(ip)

        try:
            string = "{}\n{:<16} {}, {}, {}\n{}\n{}: {}\n{}\n".format(
                                               dict.get("time"),
                                               dict.get("ip"),
                                               response.city.name,
                                               response.subdivisions.most_specific.name,
                                               response.country.iso_code,
                                               dict.get("useragent"),
                                               dict.get("status"),
                                               dict.get("request"),
                                               dict.get("referrer")
                                               )

        except UnicodeEncodeError:
            print('\n********\nFailed to parse Unicode Exception!\n********\n' + line + '\n\n')
            continue

        if (dict.get("operation") == "WEBSITE.GET.OBJECT"):
            print string
                
    continue

reader.close()    
# raw_input('Press enter to exit')
