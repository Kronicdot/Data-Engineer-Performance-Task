""" Retrieve data from API. Transform data into CSV and store in S3 bucket"""
import json
import uuid
import csv
import urllib.request
import boto3


# Initialize AWS clients
s3 = boto3.client('s3')

# Define S3 bucket and folder names
BUCKET_NAME = 'databucketmike'
FOLDER_NAME = 'fhv-data'


def transform_data(s3_path):
    """Transform data from JSON to CSV. Store in S3 Bucket"""
    try:
        # Read JSON data from S3
        response = s3.get_object(
            Bucket=BUCKET_NAME, Key=f"{FOLDER_NAME}/{s3_path}"
            )
        data = json.loads(response['Body'].read().decode('utf-8'))

        # Define column names and data
        columns = [
             'vehicle_year',
             'hack_up_date',
             'dmv_license_plate_number',
             'last_date_updated',
             'website',
             'base_number',
             'base_name',
             'last_time_updated',
             'license_type',
             'reason',
             'expiration_date',
             'vehicle_license_number',
             'certification_date',
             'veh',
             'base_type',
             'active',
             'wheelchair_accessible',
             'name',
             'vehicle_vin_number',
             'base_telephone_number',
             'base_address',
             'permit_license_number'
             ]
        headers = list(set(val for dic in data for val in dic.keys()))

        # Rearrange the headers to match the columns order
        headers = [header for header in columns if header in headers]

        # Verify if the ordered columns and headers are the same
        if headers != columns:
            raise ValueError("The headers and columns do not match.")

        for row in data:
            for key in row:
                if isinstance(row[key], str):
                    row[key] = row[key].replace(',', '')

        unique_filename = f'transformed_data_{uuid.uuid4()}.csv'
        # Create a CSV file with transformed data
        with open('/tmp/{unique_filename}',
                  'w', newline='',
                  encoding='utf-8'
                  ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        # Upload the CSV to S3
        s3.upload_file(
            '/tmp/{unique_filename}',
            BUCKET_NAME,
            f'{FOLDER_NAME}/transformed/{unique_filename}'
            )

        # Return the column names as metadata
        return columns
    except Exception as e:
        print(f"Error transforming data: {str(e)}")
        return None


def store_api_data(data):
    """ Storing API data JASON file in S3 bucket """

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{FOLDER_NAME}/raw/api_data.json",
            Body=json.dumps(data)
            )
        return True, 'raw/api_data.json'
    except Exception as e:
        print(f"Error storing data: {str(e)}")
        return False, None


def get_api_data(app_token):
    """Fetch data from the API using urllib"""

    api_url = 'https://data.cityofnewyork.us/resource/8wbx-tsch.json'

    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        print(f"Error fetching API data: {str(e)}")
        return None


def lambda_handler(event, context):
    """Fetches data from an API using a specific key,
    stores the fetched data in S3,
    transforms the stored data,
    and returns a success status if all operations are successful."""

    data = get_api_data("iyGcRT5Yvj5OrUnyHDlQhjCzd")
    if data:
        result, s3_path = store_api_data(data)
        if result:
            metadata = transform_data(s3_path)
            if metadata:
                return {
                        'statusCode': 200,
                        'body': 'success'
                    }

    return {
        'statusCode': 404,
        'body': 'failure'
    }
