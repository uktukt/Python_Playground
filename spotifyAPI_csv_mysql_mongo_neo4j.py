# reads data from the Spotify API, processes that data, and then 
# saves it to multiple data storage systems,
# including CSV files, MySQL, MongoDB, and Neo4j

import base64
import requests
import json
import pandas as pd
import pymysql
import pymongo
import datetime
import ssl
from neo4j import GraphDatabase

CLIENT_ID = client_id
CLIENT_SECRET = client_secret

# Function to get the access token
def get_token():
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        json_result = response.json()
        token = json_result['access_token']
        return token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def search_popular_songs_by_year(access_token, year):
    tracks_with_audio_features = []

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    search_url = 'https://api.spotify.com/v1/search'


    params = {
        'q': f'year:{year}',
        'type': 'track',
        'limit': 50
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])

        # Extract relevant data from the tracks and add them to the tracks_with_audio_features list
        for track in tracks:
            # Get the track ID for audio features
            track_id = track['id']

            # Retrieve audio features for the track
            audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            audio_features_response = requests.get(audio_features_url, headers=headers)
            audio_features_data = audio_features_response.json()

            # Check if audio features are available for this track
            if 'danceability' in audio_features_data:
                track_data = {
                    'Track Name': track['name'],
                    'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'Duration_ms': track['duration_ms'],
                    'Popularity': track['popularity'],
                    'Release Date': track['album']['release_date'],
                    'Year': year,
                    'Danceability': audio_features_data['danceability'],
                    'Energy': audio_features_data['energy'],
                    'Tempo': audio_features_data['tempo']
                }
                tracks_with_audio_features.append(track_data)
            else:
                print(f"Audio features not available for track: {track['name']}")

    else:
        print(f"Error: {response.status_code} - {response.text}")

    return tracks_with_audio_features

def parse_release_date(date_str):
    # List of possible date formats Spotify might return
    date_formats = ['%Y-%m-%d', '%Y-%m', '%Y']

    for format_str in date_formats:
        try:
            return datetime.datetime.strptime(date_str, format_str).date()
        except ValueError:
            continue

    # If no valid format is found, return None
    return None

# loading to mysql and saving as csv file

def save_to_mysql_and_csv(tracks_with_audio_features):
    connection = pymysql.connect(host='localhost', user='root', password='pass', database='spotify')
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS tracks_with_audio_features (
        id INT AUTO_INCREMENT PRIMARY KEY,
        track_name VARCHAR(255),
        artist VARCHAR(255),
        duration_ms INT,
        popularity INT,
        release_date DATE,
        year INT,
        danceability FLOAT,
        energy FLOAT,
        tempo FLOAT
    )
    """

    cursor.execute(create_table_query)

    insert_query = """
    INSERT INTO tracks_with_audio_features (track_name, artist, duration_ms, popularity, release_date, year, danceability, energy, tempo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for track in tracks_with_audio_features:
        release_date = parse_release_date(track['Release Date'])
        if release_date is not None:
            release_date_str = release_date.strftime('%Y-%m-%d')
        else:
            release_date_str = None

        cursor.execute(insert_query, (
            track['Track Name'],
            track['Artist'],
            track['Duration_ms'],
            track['Popularity'],
            release_date_str,
            track['Year'],
            track['Danceability'],
            track['Energy'],
            track['Tempo']
        ))

    connection.commit()
    connection.close()

    # Save the data to a CSV file
    df = pd.DataFrame(tracks_with_audio_features)
    df.to_csv('raw_tracks_with_audio_features.csv', index=False)

# loading to mongoDB

uri = 'uri'
client = pymongo.MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)


db = client['mongo_task']
collection = db['tracks']


def save_to_mongodb(data):
    try:
        for track in data:
            # Convert the release date to a string in 'YYYY-MM-DD' format
            release_date = parse_release_date(track['Release Date'])
            if release_date is not None:
                release_date_str = release_date.strftime('%Y-%m-%d')
            else:
                release_date_str = None

            document = {
                'Track Name': track['Track Name'],
                'Artist': track['Artist'],
                'Popularity': track['Popularity'],
                'Release Date': release_date_str,
                'Year': track['Year'],
                'Danceability': track['Danceability'],
                'Energy': track['Energy'],
                'Tempo': track['Tempo']
            }

            collection.insert_one(document)

        print('Data inserted into MongoDB')
    except Exception as e:
        print(f'Error: {e}')

# loading to neo4j       

uri = 'uri'
username = 'neo4j'
password = 'pass'
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_data_to_neo4j(session, data):
    with session.begin_transaction() as tx:
        for track in data:
            create_track_query = (
                "CREATE (track:Track {"
                "   name: $name,"
                "   artist: $artist,"
                "   popularity: $popularity,"
                "   release_date: date($release_date),"
                "   year: $year,"
                "   danceability: $danceability,"
                "   energy: $energy,"
                "   tempo: $tempo"
                "})"
            )

            tx.run(create_track_query, {
                "name": track['Track Name'],
                "artist": track['Artist'],
                "popularity": track['Popularity'],
                "release_date": track['Release Date'],
                "year": track['Year'],
                "danceability": track['Danceability'],
                "energy": track['Energy'],
                "tempo": track['Tempo'],
            })


def create_same_artist_relationships(session):
    with session.begin_transaction() as tx:
        query = (
            "MATCH (t1:Track), (t2:Track)"
            "WHERE t1.artist = t2.artist AND id(t1) < id(t2)"
            "MERGE (t1)-[:SAME_ARTIST]->(t2)"
        )

        tx.run(query)



if __name__ == '__main__':
    access_token = get_token()

    if access_token:
        tracks_with_audio_features = []

        years_to_collect = range(2000, 2023)  # Change the end year as needed

        for year in years_to_collect:
            year_tracks = search_popular_songs_by_year(access_token, year)
            tracks_with_audio_features.extend(year_tracks)

        # save data to a file or process it further as needed

        # save_to_mysql_and_csv(tracks_with_audio_features)
        # save_to_mongodb(tracks_with_audio_features)
        # with driver.session() as session:
        #     load_data_to_neo4j(session, tracks_with_audio_features)
        #     create_same_artist_relationships(session)
        # driver.close()

    else:
        print('Access token retrieval failed.')
