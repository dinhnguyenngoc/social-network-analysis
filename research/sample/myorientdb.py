import pyorient

# Connect to OrientDB server
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "123")

# Open the database
db_name = "myorientdb"
if client.db_exists(db_name, pyorient.STORAGE_TYPE_MEMORY):
    client.db_open(db_name, "root", "123")
else:
    print(f"Database {db_name} does not exist.")
    exit()

# Define a class if not already defined
try:
    client.command("CREATE CLASS Person EXTENDS V")
except pyorient.exceptions.PyOrientCommandException:
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
