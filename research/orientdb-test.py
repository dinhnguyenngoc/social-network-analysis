import requests
from requests.auth import HTTPBasicAuth

# Connection parameters
hostname = "localhost"
port = 2480
username = "root"
password = "oracle"
db_name = "test"

# Base URL for OrientDB HTTP API
base_url = f"http://{hostname}:{port}"

# Open the database
auth = HTTPBasicAuth(username, password)
response = requests.get(f"{base_url}/connect/{db_name}", auth=auth)

if response.status_code == 204:
    print(f"Connected to database '{db_name}' successfully.")
else:
    print(f"Failed to connect to database '{db_name}'. Status code: {response.status_code}, Message: {response.text}")



# Example query: create a class
query = "CREATE CLASS Person EXTENDS V"
response = requests.post(f"{base_url}/command/{db_name}/sql", data=query, auth=auth)

if response.status_code == 200:
    print(f"Query executed successfully: {query}")
    #print("Response:", response.json())
else:
    print(f"Failed to execute query: {query}. Status code: {response.status_code}, Message: {response.text}")

# Example query: insert a record
query = "INSERT INTO Person SET name = 'John Doe', age = 30"
response = requests.post(f"{base_url}/command/{db_name}/sql", data=query, auth=auth)

if response.status_code == 200:
    print(f"Query executed successfully: {query}")
    #print("Response:", response.json())
else:
    print(f"Failed to execute query: {query}. Status code: {response.status_code}, Message: {response.text}")

# Example query: select records
query = "SELECT FROM Person"
response = requests.post(f"{base_url}/command/{db_name}/sql", data=query, auth=auth)

if response.status_code == 200:
    print(f"Query executed successfully: {query}")
    #print("Response:", response.json())
else:
    print(f"Failed to execute query: {query}. Status code: {response.status_code}, Message: {response.text}")
    