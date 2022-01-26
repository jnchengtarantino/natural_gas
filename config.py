# Days in the file system are written as MM%2FDD%2FYYYY
start_date = '01-01-2022'
end_date = '01-03-2022'
dateFormat = '%m-%d-%Y'

params = {
    'database': 'natural_gas',
    'user': 'postgres',
    'password': 'password',
    'host': '127.0.0.1', 
    'port': 5432
}

sql = {
    'create gas_data': 
        '''
        CREATE TABLE gas_data(
            id SERIAL PRIMARY KEY,
            loc INTEGER NOT NULL,
            loc_zone VARCHAR(32) NOT NULL,
            loc_name VARCHAR(64) NOT NULL,
            loc_purpose VARCHAR(2) NOT NULL,
            qti VARCHAR(3) NOT NULL,
            flow_ind VARCHAR(1),
            dc INTEGER,
            opc INTEGER,
            tsq INTEGER,
            oac INTEGER,
            it BOOLEAN,
            auth_overrun BOOLEAN,
            nom_cap_exceeded BOOLEAN,
            all_qty_available BOOLEAN,
            qty_reason TEXT,
            record_id INTEGER REFERENCES record(id)
            );
        ''',

    'create record':
        '''
        CREATE TABLE record (
            id SERIAL PRIMARY KEY,
            day DATE,
            cycle INTEGER
        );
        ''',

    'insert record':
        '''
        INSERT INTO record (day, cycle) VALUES (%s, %s) RETURNING id;
        ''',

    'insert gas_data':
    '''
    INSERT INTO gas_data (loc, loc_zone, loc_name, loc_purpose, qti, flow_ind, dc, opc, tsq, oac, it, auth_overrun, nom_cap_exceeded, all_qty_available, qty_reason, record_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
}