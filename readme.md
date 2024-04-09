## Airflow for Local Deployment ##
This repo contains resources for deploying an Apache Airflow on your local machine to speed up pipeline development

Goal is to replicate AWS MWAA deployment locally, so the dev process is faster and smoother

It uses the original Docker Compose file provided by the Airflow documentation and adds a few features for helping you synch your production variables and connections

Based on: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

## Dependencies
- docker (>=25.0.3)
- docker-compose (>=2.24.6)
- aws-cli(>=1.22.34)
- python(>=3.10)
-boto3 (>=1.34.73)

## Define your Airflow version and settings

First thing you need to do is define your Airflow version and add it to your .env file. Recommended to use the same version of your production Airflow instance. For example:
```echo -e "AIRFLOW_VERSION=2.5.1" >> .env

Next, specify the path to the DAG folder so that Docker Compose can map it to the container. Pass it to a local variable AIRFLOW_PROJ_DAG_PATH:
```echo -e "AIRFLOW_PROJ_DAG_PATH=/home/your-user/Documents/Repositories/cashapp/dags" >> .env

And finally, the Docker Compose file requires you to define an AIRFLOW_UID:
```echo -e "AIRFLOW_UID=$(id -u)" >> .env

The previous commands save your local env variables on a .env file and are referenced internally as parameters for Docker Compose.

Also make sure you create folder on repository for logs, plugins and confi, as Airflow would use it.

mkdir -p ./logs ./plugins ./config

## Defining Airflow Requirements

To define the requirements to be installed on your Airflow deployment, you need to create a requirements.txt file and all the libraries and dependencies. Make sure to add the versions and check for conflict.

## Project Structure

After the initial setup, your project repository would show the following structure:
Readme.md
docker-compose.yaml
Dockerfile
airflow.sh
requirements.txt
config/
dags/ # if dag folder inside the rep
logs/
plugins/
resources/
    - update_airflow_connections.py
    - connections.json
    - variables.json

## Running docker compose

After going through steps above, you only need to execute the Docker Compose command to deploy to Airflow on your machine
```docker compose up

The file docker-compose.yaml uses the Dockerfile as reference for pulling the Docker images. After a few minutes you should have 6 containers up.

To access the Airflow webserver you need to open your web browser on localhost:8080, with:
login: airflow, password: airflow

## Defining your Airflow connections
To make your dev process smoother, your can leverage the script resources/update_airflow_connections.py. To run it, you need to create a json file with connection name as key and the AWS Param Store key as the value so the script can fetch the connection URI. Also, make sure the AWS CLI is able to access AWS dev account using the default profile, as the scripts uses boto3 to fetch information from AWS Param Store

You can use the connections.json as a template and add new connections as needed. To execute the script:
```cd resources
python3 update_airflow_connections.py connections.json```

After fetching the connection URI listed on the json file, the script uses the Airflow CLI to create (import command) new connections.

## Importing Airflow Variables

Use the Airflow CLI using the below command
```./airflow.sh variables import resources/variables.json

## Using Airflow CLI
If you want to execute Airflow CLI, you can use the airflow.sh followed by the desired command. For example, if you want to list your DAGs:
```./airflow.sh dags list