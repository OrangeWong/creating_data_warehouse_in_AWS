# Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

# Description
Building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. 

# Repo Structure
This repo contains the following files:
- create_tables.py: to create the staging tables and target tables in AWS Redshift.
- etl.py: 1. to extract data from S3, 2. to load the data into staging tables, 3. to copy the selected and transformed data into the desired tables in Redshift.
- sql_queries.py: contains the SQL queries that are used to create, load, and insert data into Redshift.
- demo.ipynb: a Jupyter Notebook to demo the flow of creating the database into Redsihft.

# Database Structure
The database contains the following tables:
- fact table: songplays.
- dimension tables:
	- users
	- songs
 	- artists
	- time

# To Fill the credentials
We need to fill the credentials into dwh.cfg with the following format to get access to the AWS Redshift database:

[CLUSTER]
HOST=<aws_host>
DB_NAME=<your_db_name>
DB_USER=<your_db_user_name>
DB_PASSWORD=<your_db_passowrd>
DB_PORT=<your_db_port_to_connect>

[IAM_ROLE]
ARN='<your_iam_role_in_aws>'

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

# Hoe to Run
To create and insert data into data warehouse in Redshift, run the following commands:
- python create_tables.py
- python etl.py
