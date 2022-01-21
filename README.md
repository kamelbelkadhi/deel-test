# Documentation

Question: How many hours this task took me to finish it
Answer: Around 2 hours 

Main files:
* docker-compose.yml
* Dockerfile
* python-app : Folder where the script and data lives
* *deel.py: Main script
* *data: Data folder

***How To Run***
- Navigate to the main folder 
- Run docker using this command: docker-compose up --build
- Get inside the container: docker exec -it deel-test-main_postgres_1 bin/bash
- Run inside the container: cd /var/www/html
- Run the script: python3 deel.py

***How it was done***
1- Connect to the Postgresql DB using sqlalchemy
2- Read data from Json files in DataFrame
3- Dump the data into postgresql DB using Pandas into the following tables: **Contracts** and **Invoices**
4- Run the following queries using chunk method in pandas (similar to batching, I used batch_size=5, feel free to change it :) ) 
***queries = {'Query 1':"""SELECT "RECEIVED_AT"::date as date, "IS_DELETED", count(*)
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
                    WHERE contracts."IS_DELETED"::bool is false group by "CLIENT_ID", "INVOICE_ID" """}***
5- After each runned query, a sleep of 10 seconds will be applied so user can see the results


***Challenges***
1- No majore challenge happened, I just had some difficulties with keychain in my laptop (MacOs) that prevents me from pushing the code into github, so I had to upload the code manually
 
