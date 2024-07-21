import pyorientdb
    
client = pyorientdb.OrientDB("103.75.186.135", 2424)
client.set_session_token( True ) 
session_id = client.connect( "root", "nghiadinhdung" )

# Open the database
db_name = "demodb"
if client.db_exists(db_name, pyorientdb.STORAGE_TYPE_MEMORY):
    client.db_open(db_name, "root", "nghiadinhdung")
else:
    print(f"Database {db_name} does not exist.")
    exit()

# Define a class if not already defined
try:
    client.command("CREATE CLASS Person EXTENDS V")
except pyorientdb.exceptions.PyOrientCommandException:
    # Class already exists
    pass

# Insert a record into the Person class
command = "INSERT INTO Person (name, age) VALUES ('John Doe', 30)"
client.command(command)

# Fetch and print the inserted record to confirm
records = client.query("SELECT FROM Person WHERE name = 'John Doe'")
for record in records:
    print(record.oRecordData)

# Close the connection
client.db_close()
