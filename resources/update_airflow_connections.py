import argparse
import json
import boto3
import logging
import subprocess
import os

"""
Module used to update Airflow connections by fetching parameter values from AWS Systems Manager Parameter Store.

Usage:
    python3 update_airflow_connections.py <filename>

Arguments:
    file (str): Path to the JSON file containing the connection names and corresponding paramter names.

"""

logging.basicConfig(level=logging.INFO)

def fetch_parameter(parameter_name):
    """
    Fetches the value of a specified parameter from AWS Systems Manager Parameter Store

    Args:
        parameter_name (str): Name of the parameter to fetch

    Returns:
        str: Value of the parameter
    """

    try:
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except Exception as e:
        logging.error(f"Failed to fetch parameter: {parameter_name}")
        logging.error(str(e))
        return None
    
def main():
    #Open the JSON file
    with open(args.file) as f:
        data = json.load(f)
    logging.info(f"Processing JSON file: {data}")

    dict_conn_id = {}

    for connection_name, parameter_name in data.items():
        parameter_value = fetch_parameter(parameter_name)
        dict_conn_id[connection_name] = parameter_value

    # Create a temporary JSON file
    temp_file = "temp_file.json"
    with open(temp_file, "w") as f:
        json.dump(dict_conn_id, f, indent=4)

    # Cleanup temporary JSON file
    subprocess_commands = [
        "../airflow.sh",
        "connections",
        "import",
        "resources/temp_file.json"
    ]

    try:
        result = subprocess.run(subprocess_commands, capture_output=True, text=True)
        logging.info(f"Std Out: {result.stdout}")
        logging.info(f"Std Error: {result.stderr}")

    except Exception as e:
        logging.error("Failed to execute subprocess command")
        logging.error(str(e))

    os.remove(temp_file)


if __name__ == "__main__":
    main()