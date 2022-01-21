import pandas as pd
from sqlalchemy import create_engine
import time

conn_string = 'postgresql://deel:deel@172.28.1.4/deel' # this connection is coming from docker-compose.yml
db = create_engine(conn_string)
conn = db.connect()
batch_size = 5

# Q1
queries = {'Query 1':"""SELECT "RECEIVED_AT"::date as date, "IS_DELETED", count(*)
                    FROM contracts group by date, "IS_DELETED" order by date""",
            #Q2
            'Query 2':"""SELECT "RECEIVED_AT"::date as date, "CONTRACT_ID", "IS_DELETED", count(*)
                    FROM invoices group by date, "CONTRACT_ID", "IS_DELETED" order by date""",
            #Q3
            'Query 3':"""SELECT contracts."CONTRACT_ID", "CURRENCY", SUM("AMOUNT") AMOUNT
                    FROM invoices JOIN contracts on contracts."CONTRACT_ID"=invoices."CONTRACT_ID"
                    where contracts."IS_DELETED"::bool is false group by contracts."CONTRACT_ID", "CURRENCY" """,
            #Q4
            'Query 4':"""SELECT "CLIENT_ID", "INVOICE_ID", min(invoices."RECEIVED_AT") "RECEIVED_AT"
                    FROM contracts JOIN invoices on contracts."CONTRACT_ID"=invoices."CONTRACT_ID"
                    WHERE contracts."IS_DELETED"::bool is false group by "CLIENT_ID", "INVOICE_ID" """}

def load_data_to_db(conn):
    data_contracts = pd.read_json('data/contracts.json')
    data_invoices = pd.read_json('data/invoices.json')
    # renaming RECEIVED_AT\n to RECEIVED_AT in both dataframes
    data_contracts.rename({'RECEIVED_AT\n':'RECEIVED_AT'}, axis=1, inplace=True)
    data_invoices.rename({'RECEIVED_AT\n':'RECEIVED_AT'}, axis=1, inplace=True)
    #loading data into DB
    data_contracts.to_sql('contracts', con=conn, if_exists='replace', index=False)
    data_invoices.to_sql('invoices', con=conn, if_exists='replace', index=False)
    print('Json files loaded in DB')

load_data_to_db(conn)

def batch_processing(query):
    for chunk in pd.read_sql_query(query , conn, chunksize=batch_size):
            print(chunk)

for query in queries.keys():
    print(f'Running for {query}')
    batch_processing(queries[query])
    time.sleep(10)
