# top 8 ou 10 à chaque fois

# Gares les plus fréquentées (ville ?)

# Gares qui génèrent le plus de retard (departure time ou delay)  [V]

# trajets qui ont le plus de retard   [V]


from flask import Flask, json

import pandas as pd
from sqlalchemy import create_engine

DB_NAME = "SNCB"
DB_USERNAME = "postgres"
DB_PASSWORD = "luka"
DB_HOST = "localhost"
DB_PORT = 5432
app = Flask(__name__)
engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))


@app.route('/delaybyroute')
def get_delay_by_route():

    query = '''
    select distinct trip_id, route_long_name, max(bebou.total_departure_delay) as total_delay
    from ( SELECT distinct AVG(departure_delay)/60 as total_departure_delay, sncb.trip_id , COALESCE(r.route_long_name, 'Unknown') as route_long_name
	   FROM sncb, trips t
	   LEFT JOIN routes r ON t.route_id = r.route_id
	   WHERE schedule_relationship = '0' and departure_delay is not null and t.trip_id = sncb.trip_id
	   GROUP BY sncb.trip_id, sncb.stop_id, sncb.query_time, r.route_long_name
	   ORDER BY total_departure_delay DESC ) as bebou
    group by bebou.route_long_name, bebou.trip_id
    order by total_delay desc
    ;
    '''
    delays = pd.read_sql_query(query, engine)
    delays.to_json(r'C:\Users\lukag\PycharmProjects\GS-New-Project\JsonFiles\get_delay_by_route.json', orient='records', lines=True)
    return delays

@app.route('/delaybystop')
def get_delay_by_stop(engine):

    query = '''
    SELECT s.stop_id, s.stop_name, AVG(sncb.departure_delay)/60 AS average_delay
    FROM stops s
    JOIN sncb ON s.stop_id = sncb.stop_id
    WHERE sncb.schedule_relationship = '0' AND sncb.departure_delay IS NOT NULL
    GROUP BY s.stop_id, s.stop_name
    ORDER BY average_delay DESC;
    '''
    delays = pd.read_sql_query(query, engine)

    delays.to_json(r'C:\Users\lukag\PycharmProjects\GS-New-Project\JsonFiles\get_delay_by_stop.json', orient='records', lines=True)

    return delays


@app.route('/mostfrequented')
def get_most_frequented_stations(engine):

    query = '''
    SELECT s.stop_id, s.stop_name, COUNT(sncb.trip_id) AS departure_count
    FROM stops s
    JOIN sncb ON s.stop_id = sncb.stop_id
    WHERE sncb.schedule_relationship = '0'
    GROUP BY s.stop_id, s.stop_name
    ORDER BY departure_count DESC;
    '''
    most_frequented_stations = pd.read_sql_query(query, engine)

    most_frequented_stations.to_json(r'C:\Users\lukag\PycharmProjects\GS-New-Project\JsonFiles\most_frequented_stations.json', orient='records', lines=True)

    return most_frequented_stations

@app.route('/')
def homepage():
    return 'Quick RESTFUL API For scnb app'


if __name__ == '__main__':
    app.run()