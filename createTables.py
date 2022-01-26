import psycopg2
from config import params, sql

conn = None

try:
    conn = psycopg2.connect(**params)
    print('connected to database')
    cursor = conn.cursor()

    print('executing CREATE commands')
    cursor.execute(sql['create record'])
    cursor.execute(sql['create gas_data'])
    cursor.close()

    print('commiting')
    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()