import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists times"

# CREATE TABLES

staging_events_table_create= ("""
    create table if not exists staging_events (
        staging_event_id identity(0, 1) primary key,
        artist varchar,
        auth varchar,
        first_name varchar not null,
        gender varchar,
        item_in_session int not null,
        last_name varchar not null,
        length float,
        level varchar not null,
        location varchar,
        method varchar,
        page varchar,
        registration float,
        session_id int not null,
        song varchar,
        status int, 
        ts int,
        user_agent varchar,
        use_id int not null
    )
""")

staging_songs_table_create = ("""
    create table if not exists staging_songs (
        staging_song_id identity(0, 1) primary key,
        num_songs int, 
        artist_id varchar not null,
        artist_latitude float, 
        artist_longitude float, 
        artist_location varchar,
        artist_name varchar,
        song_id varchar not null, 
        title varchar not null,
        duration float not null, 
        year int
    )
""")

songplay_table_create = ("""
    create table if not exists songplays (
        songplay_id identity(0, 1) primary key
        start_time int,
        user_id int not null, 
        level varchar not null, 
        song_id varchar not null, 
        artist_id varchar not null, 
        session_id int not null, 
        location varchar, 
        user_agent varchar
    )
""")

user_table_create = ("""
    create table if not exists users (
        user_id int primary key not null, 
        first_name varchar not null, 
        last_name varchar not null, 
        gender varchar, 
        level varchar not null
        )
""")

song_table_create = ("""
    create table if not exists songs (
        song_id varchar primary key not null, 
        title varchar not null, 
        artist_id varchar not null, 
        year int, 
        duration float not null
    )
""")

artist_table_create = ("""
    create table if not exists artists (
        artist_id varchar primary key not null, 
        name varchar, 
        location varchar, 
        lattitude float, 
        longitude float
    )
""")

time_table_create = ("""
    create table if not exists times (
        start_time int primary key not null, 
        hour int not null, 
        day int not null, 
        week int not null, 
        month int not null, 
        year int not null, 
        weekday int not null
    )
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
