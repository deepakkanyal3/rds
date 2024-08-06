import mysql.connector
import csv

# Connect to the MySQL server
mydb = mysql.connector.connect(
    host="gromo-staging-rds.cgfbihskxfkk.ap-south-1.rds.amazonaws.com",
    user="root",
    password="X1wxSv2yNPds0CHHn4W"
)
cursor = mydb.cursor()

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
            query = "SELECT COUNT(*) FROM mysql.user WHERE User = %s"
            cursor.execute(query, (name,))
            if cursor.fetchone()[0] == 1:
                print(f"User {name} already exists.")
                query = "SHOW GRANTS FOR %s@'%';"
                cursor.execute(query, (name,))
                for x in cursor:
                    print("==============================================")
                    print(x)
            else:
                # Create the new user
                create_user_query = "CREATE USER %s@'%' IDENTIFIED BY %s;"
                cursor.execute(create_user_query, (name, passw))
                print(f"User {name} created.")

                # Get the database name or handle the case of all databases
                database = input(f"Enter the database name to grant access to {name} (or press Enter to grant access to all databases): ")
                if len(database) == 0:
                    grant_query = """
                    GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, ALTER, INDEX ON *.* TO %s@'%';
                    """
                    cursor.execute(grant_query, (name,))
                    print(f"Permissions granted to {name} on all databases.")
                else:
                    grant_query = f"""
                    GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, ALTER ON {database}.* TO %s@'%';
                    """
                    cursor.execute(grant_query, (name,))
                    print(f"Permissions granted to {name} on {database}.")

except FileNotFoundError:
    print(f"File not found: {csv_file_path}.")
except csv.Error as e:
    print(f"Error reading CSV file: {e}")

# Commit changes and close the connection
mydb.commit()
cursor.close()
mydb.close()
