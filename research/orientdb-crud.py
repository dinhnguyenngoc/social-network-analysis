import requests
from requests.auth import HTTPBasicAuth
import json

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

# Check if class exists
def check_class_exists(class_name):
    query = f"SELECT FROM (SELECT expand(classes) FROM metadata:schema) WHERE name = '{class_name}'"
    response = requests.post(base_url, data=query, auth=auth)
    result = response.json()
    return len(result['result']) > 0

# Create the Posts class if it does not exist
def create_posts_class():
    if not check_class_exists("Posts"):
        query = """
        CREATE CLASS Posts EXTENDS V;
        CREATE PROPERTY Posts.postId STRING;
        CREATE PROPERTY Posts.authorId STRING;
        CREATE PROPERTY Posts.time DATETIME;
        CREATE PROPERTY Posts.isShared BOOLEAN;
        CREATE PROPERTY Posts.contentType STRING;
        CREATE PROPERTY Posts.share INTEGER;
        CREATE PROPERTY Posts.reactions INTEGER;
        """
        response = requests.post(base_url, data=query, auth=auth)
        return response.json()
    else:
        return {"result": "Class 'Posts' already exists."}

# Create (Insert) a new post
def create_post(postId, authorId, time, isShared, contentType, share, reactions):
    query = f"""
    INSERT INTO Posts SET 
    postId = '{postId}', 
    authorId = '{authorId}', 
    time = '{time}', 
    isShared = {isShared}, 
    contentType = '{contentType}', 
    share = {share}, 
    reactions = {reactions}
    """
    response = requests.post(base_url, data=query, auth=auth)
    return response.json()

# Read (Select) posts
def read_posts(condition=""):
    query = f"SELECT FROM Posts {condition}"
    response = requests.post(base_url, data=query, auth=auth)
    return response.json()

# Update a post
def update_post(postId, updates):
    set_clause = ", ".join([f"{key} = '{value}'" for key, value in updates.items()])
    query = f"UPDATE Posts SET {set_clause} WHERE postId = '{postId}'"
    response = requests.post(base_url, data=query, auth=auth)
    return response.json()

# Delete a post
def delete_post(postId):
    query = f"DELETE FROM Posts WHERE postId = '{postId}'"
    response = requests.post(base_url, data=query, auth=auth)
    return response.json()

# Example usage
# Create the Posts class if it does not exist
create_class_result = create_posts_class()
print("Create Class Result:", json.dumps(create_class_result, indent=2))

# Create a new post
#new_post = create_post("123", "author_1", "2024-07-19T12:34:56", True, "Text", 10, 5)
#print("Created Post:", json.dumps(new_post, indent=2))

# Read all posts
#posts = read_posts()
#print("All Posts:", json.dumps(posts, indent=2))

# Update a post
#updates = {"contentType": "Photo", "share": 20}
#updated_post = update_post("123", updates)
#print("Updated Post:", json.dumps(updated_post, indent=2))

# Delete a post
#deleted_post = delete_post("123")
#print("Deleted Post:", json.dumps(deleted_post, indent=2))
