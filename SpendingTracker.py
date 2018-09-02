#!/usr/bin/python

# mt940 parser package was installed to:
#    /usr/local/lib/python2.7/dist-packages/mt940

import mt940
import pprint
from decimal import Decimal

# note that each purchase_type must have a minimium of two entries in the list
shop_list = {
    'FOOD' : ('AH TOGO', 'AHTOGO', 'AH TO GO', 'DELIVEROO', 'VENDING', 'FOODORA', 'ALBERT HEIJN', 'SUPERMARK',
             'LUNCH', 'KFC', 'FOPPINGA', 'BROODZAAK', 'CHOCO', 'GELATERIA', 'TASTE OF HOME', 'FRIET',
             'DONER', 'WAFELS', 'RESTAU', 'KIOSK', 'JULIA', 'SWIRL', 'HOT DOG', 'STROOP', 'BAKKER', 'IJSSALON',
             'MCDONALD', 'SUMO', 'BURGER', 'JETTIES', 'FOOD', 'BOWLS', 'TUTTI', 'CREPE', 'SUSHI', 'FALAFEL',
             'KOOKREBELLEN', 'SIMON MEIJSSEN', 'BRASSERIE', 'WARUNG POJOK', 'TABLE 24', 'SPANEDER ROTTERDAM',
             'MARKUS WADDINXVEEN', 'BACK TO BASICS'),
    'CASH' : ('KRUISWEG 37', 'KRUISSTRAAT 10'), 
    'CLOTHES' : ('ETAM', 'H&M', 'VAN HAREN', 'SHOES', 'BRISTOL'),
    'HOUSEHOLD' : ('HEMA', 'ETOS', 'KRUIDVAT', 'IKEA', 'FLYING TIGER', 'BEVER', 'BODY SHOP', 'BLOKKER', 
                   'BOL.COM', 'AMAZON', 'ACTION', 'MEDIA MARKT', 'XENOS', 'BEDGENOTEN'),
    'ENTERTAINMENT' : ('SPELLENHUIS', 'EFTELING', 'KASTEEL DE HAAR', 'VOGELPAR', 'PATHE', 'TICKETS',
                       'DIERGAARDE', 'NIEUWE KERK', 'MUSEUM', 'ARTIS', 'ECOMARE', 'STALPLEIN BV HAARZUI',
                       'VOLENDAM', 'RONDVAART DELFT'),
    'TRAVEL' : ('CHIPKAART', 'NS-', 'NS '),
    }

not_found_count = 0
not_found_amount = Decimal(0.0)
found_count = 0
found_amount = Decimal(0.0)
month_data = {}

for purchase_type in shop_list:
    month_data[purchase_type] = {}

target_path = "/home/rick/Desktop/SpendingTracker/MT940.STA"

transactions = mt940.parse(target_path)

for transaction in transactions:
    found = False
    for purchase_type in shop_list:
        if any(s in transaction.data['transaction_details'] for s in shop_list[purchase_type]):
            found = True
            found_count += 1
            found_amount += transaction.data['amount'].amount
            if transaction.data['date'].month in month_data[purchase_type]:
                month_data[purchase_type][transaction.data['date'].month] += transaction.data['amount'].amount
            else:
                month_data[purchase_type][transaction.data['date'].month] = transaction.data['amount'].amount
    
    # ignore account credits
    if transaction.data['amount'].amount > 0:
        found = True
    
    if not found:
        not_found_count += 1
        not_found_amount += transaction.data['amount'].amount
        print transaction.data['amount'], transaction.data['transaction_details']

pprint.pprint(month_data)
print "Found: ", found_count, " for: ", found_amount
print "Not Found: ", not_found_count, " for: ", not_found_amount
