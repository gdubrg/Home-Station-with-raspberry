import requests


# query_sql = 'SELECT * FROM "a1c46cfe-46e5-44b4-9231-7d9260a38e68" WHERE "station_id" LIKE "4000022"'
# r = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql=' + query_sql).json()

r = requests.get('https://arpae.datamb.it/api/action/datastore_search_sql?sql=SELECT * from "a1c46cfe-46e5-44b4-9231-7d9260a38e68" '
                 'WHERE station_id=4000022'
                 'AND variable_id=8'
                 'ORDER BY reftime DESC '
                 # 'LIMIT 1'
                 ).json()

print(r)
