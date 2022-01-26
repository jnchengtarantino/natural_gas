import csv
from urllib import request
from datetime import date, datetime, timedelta
import psycopg2
import config

def genDates(start: str, end: str) -> list:
    '''
    Used to parse the format of the dates in the URL, 
    generate all dates in range, convert them back to the original format,
    and return the list.
    '''
    startDate = datetime.strptime(start, config.dateFormat).date()
    endDate = datetime.strptime(end, config.dateFormat).date()
    return [(startDate+timedelta(days=x)).strftime(config.dateFormat) for x in range( (endDate-startDate).days + 1)]
    

baseURL = 'https://twtransfer.energytransfer.com/ipost/capacity/operationally-available?f=csv&extension=csv&asset=TW&'
cycleURL = '&cycle='
appendURL = '&searchType=NOM&searchString=&locType=ALL&locZone=ALL'

# By trial, these seem to be the only values that return data
# This hardcode should be confirmed or fixed
cycles = ['0','1']

conn = None

try:
    conn = psycopg2.connect(**config.params)
    print('connected to database')
    cursor = conn.cursor()

    for day in genDates(config.start_date, config.end_date):
        for cycle in cycles:
            print('Data for ' + day.replace('-','%2F') + ' cycle ' + str(cycle))
            resp = request.urlopen(baseURL + day.replace('-','%2F') + cycleURL + str(cycle) + appendURL)
            lines = [l.decode('utf-8') for l in resp.readlines()]
            m, d, y = day.split('-')
            
            cursor.execute(config.sql['insert record'], ('-'.join([y,m,d]), int(cycle)))
            record_id = cursor.fetchone()[0]

            csvReader = csv.reader(lines)
            next(csvReader) # Skip label line

            for row in csvReader:
                loc = int(row[0])
                loc_zone = row[1]
                loc_name = row[2]
                loc_purpose = row[3]
                qti = row[4]
                flow_ind = row[5]
                dc = int(row[6]) if row[6] != '' else None
                opc = int(row[7]) if row[7] != '' else None
                tsq = int(row[8]) if row[8] != '' else None
                oac = int(row[9]) if row[9] != '' else None
                it = (row[10] == 'Y')
                auth_overrun = (row[11] == 'Y')
                nom_cap_exceeded = (row[12] == 'Y')
                all_qty_available = (row[13] == 'Y')
                qty_reason = row[14]

                cursor.execute(config.sql['insert gas_data'], (loc, loc_zone, loc_name, loc_purpose, qti, flow_ind, dc, opc, tsq, oac, it, auth_overrun, nom_cap_exceeded, all_qty_available, qty_reason, record_id) )
                conn.commit()

except (psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()