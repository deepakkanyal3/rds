import pymongo
import csv

# Connect to the DocumentDB server
client = pymongo.MongoClient(
    "mongodb://deepak:xxxx$@gromo-production-docdb.cluster-cgfbihskxfkk.ap-south-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
)
admin_db = client.admin  # Connect to the admin database

# Read users from CSV file
csv_file_path = input("Enter the path to the CSV file containing usernames and passwords: ")

users_to_create = []

try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Debug output to check each row
            print(f"Processing row: {row}")

            if len(row) == 2 and row[0].strip() and row[1].strip():
                name, passw = row
                users_to_create.append((name, passw))
            else:
                print(f"Invalid row format or empty values: {row}. Skipping.")

    if not users_to_create:
        print("No valid rows found in the CSV file. No users will be created.")
    else:
        for name, passw in users_to_create:
            # Check if the user already exists
            users_collection = admin_db.command('usersInfo', name)
            if 'users' in users_collection and len(users_collection['users']) > 0:
                print(f"User {name} already exists.")
                for user in users_collection['users']:
                    print("==============================================")
                    print(user)
            else:
                # Create the new user with readWriteAnyDatabase role
                admin_db.command('createUser', name, pwd=passw, roles=[
                    {'role': 'readWriteAnyDatabase', 'db': 'admin'}
                ])
                print(f"User {name} created with read and write access to all databases.")

except FileNotFoundError:
    print(f"File not found: {csv_file_path}.")
except csv.Error as e:
    print(f"Error reading CSV file: {e}")
except pymongo.errors.PyMongoError as e:
    print(f"MongoDB error: {e}")

# Close the connection
client.close()
