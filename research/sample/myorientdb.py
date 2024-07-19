# import pyorient
import requests

from requests.auth import HTTPBasicAuth

server_url = "http://103.75.186.135:2480"

auth = HTTPBasicAuth("root", "nghiadinhdung")

def connect_to_database(db_name):
    connect_url = f"{server_url}/connect/{db_name}"
    response = requests.get(connect_url, auth=auth)
    if response.status_code == 204:
        print(f"Connected to the database: {db_name}")
    else:
        print(f"Failed to connect: {response.status_code}, {response.text}")

connect_to_database("demodb")

def execute_query(db_name, query):
    query_url = f"{server_url}/command/{db_name}/sql"
    headers = {"Content-Type": "application/json"}
    payload = {"command": query}
    response = requests.post(query_url, json=payload, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to execute query: {response.status_code}, {response.text}")
        return None

query_result = execute_query("demodb", "SELECT FROM V")
if query_result:
    print(query_result)
    
# client = pyorientdb.OrientDB("103.75.186.135", 2480)
# client.set_session_token( True ) 
# session_id = client.connect( "root", "nghiadinhdung" )

# # Open the database
# db_name = "demodb"
# if client.db_exists(db_name, pyorient.STORAGE_TYPE_MEMORY):
#     client.db_open(db_name, "root", "nghiadinhdung")
# else:
#     print(f"Database {db_name} does not exist.")
#     exit()

# # Define a class if not already defined
# try:
#     client.command("CREATE CLASS Person EXTENDS V")
# except pyorient.exceptions.PyOrientCommandException:
#     # Class already exists
#     pass

# # Insert a record into the Person class
# command = "INSERT INTO Person (name, age) VALUES ('John Doe', 30)"
# client.command(command)

# # Fetch and print the inserted record to confirm
# records = client.query("SELECT FROM Person WHERE name = 'John Doe'")
# for record in records:
#     print(record.oRecordData)

# # Close the connection
# client.db_close()
