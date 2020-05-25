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
        staging_song_id bigint identity(0, 1),
        artist varchar,
        auth varchar,
        first_name varchar,
        gender varchar,
        item_in_session int,
        last_name varchar,
        length float,
        level varchar,
        location varchar,
        method varchar,
        page varchar,
        registration float,
        session_id int,
        song varchar,
        status int, 
        ts bigint,
        user_agent varchar,
        user_id int
    )
""")

staging_songs_table_create = ("""
    create table if not exists staging_songs (
        staging_song_id bigint identity(0, 1),
        num_songs int, 
        artist_id varchar,
        artist_lattitude float, 
        artist_longitude float, 
        artist_location varchar,
        artist_name varchar,
        song_id varchar, 
        title varchar,
        duration float, 
        year int
    )
""")

songplay_table_create = ("""
    create table if not exists songplays (
        songplay_id bigint identity(0, 1) primary key,
        start_time timestamp not null,
        user_id int not null, 
        level varchar, 
        song_id varchar not null, 
        artist_id varchar not null, 
        session_id int not null, 
        location varchar, 
        user_agent varchar
    )
""")

user_table_create = ("""
    create table if not exists users (
        user_id int primary key, 
        first_name varchar not null, 
        last_name varchar not null, 
        gender varchar, 
        level varchar not null
        )
""")

song_table_create = ("""
    create table if not exists songs (
        song_id varchar primary key, 
        title varchar not null, 
        artist_id varchar not null, 
        year int, 
        duration float not null
    )
""")

artist_table_create = ("""
    create table if not exists artists (
        artist_id varchar primary key, 
        name varchar, 
        location varchar, 
        lattitude float, 
        longitude float
    )
""")

time_table_create = ("""
    create table if not exists times (
        start_time timestamp primary key, 
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
    copy staging_events from {}
    iam_role {} format as json {}
""").format(
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH")
)

staging_songs_copy = ("""
    copy staging_songs from {}
    iam_role {} format as json 'auto'
""").format(
    config.get("S3", "SONG_DATA"),
    config.get("IAM_ROLE", "ARN")
)

# FINAL TABLES

#  there is no from_unixtime() in redshift (https://stackoverflow.com/questions/39815425/how-to-convert-epoch-to-datetime-redshift)

songplay_table_insert = ("""
    insert into songplays (
        start_time,
        user_id, 
        level, 
        song_id, 
        artist_id, 
        session_id, 
        location, 
        user_agent
    )
    select
        timestamp 'epoch' + se.ts / 1000 * interval '1 second' as start_time, 
        se.user_id,
        se.level,
        ss.song_id,
        ss.artist_id,
        se.session_id,
        se.location,
        se.user_agent
    from staging_events as se
    join staging_songs ss on se.song = ss.title and se.artist = ss.artist_name
    where se.page = 'NextSong'
""")

user_table_insert = ("""
    insert into users (
        user_id, 
        first_name, 
        last_name, 
        gender, 
        level
        )
    select distinct
        se.user_id,
        se.first_name,
        se.last_name,
        se.gender,
        se.level
    from staging_events as se where se.page = 'NextSong'    
""")

song_table_insert = ("""
    insert into songs (
        song_id, 
        title, 
        artist_id, 
        year, 
        duration
    )
    select 
        ss.song_id,
        ss.title,
        ss.artist_id,
        ss.year,
        ss.duration
   from staging_songs as ss
""")

artist_table_insert = ("""
    insert into artists (
        artist_id, 
        name, 
        location, 
        lattitude, 
        longitude
        )
    select 
        ss.artist_id,
        ss.artist_name as name,
        ss.artist_location as location,
        ss.artist_lattitude as lattitude,
        ss.artist_longitude as longitude
    from staging_songs as ss        
""")

time_table_insert = ("""
    insert into times (
        start_time, 
        hour, 
        day, 
        week, 
        month, 
        year, 
        weekday
        )
    select 
        timestamp 'epoch' + se.ts / 1000 * interval '1 second' as start_time, 
        extract(hour from start_time) as hour,
        extract(day from start_time) as day,
        extract(week from start_time) as week,
        extract(month from start_time) as month,
        extract(year from start_time) as year,
        extract(week from start_time) as weekday
    from staging_events as se where se.page = 'NextSong'        
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
