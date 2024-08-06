import mysql.connector
import csv

# Connect to the MySQL server
mydb = mysql.connector.connect(
    host="databases-url",
    user="root",
    password="XXXXXXXXX"
)
cursor = mydb.cursor()

# Read users from CSV file
csv_file_path = input("Enter the path to the CSV file containing usernames: ")

users_to_update = []

try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Debug output to check each row
            print(f"Processing row: {row}")

            if len(row) == 1 and row[0].strip():
                name = row[0]
                users_to_update.append(name)
            else:
                print(f"Invalid row format or empty value: {row}. Skipping.")

    if not users_to_update:
        print("No valid rows found in the CSV file. No users will be updated.")
    else:
        for name in users_to_update:
            # Check if the user exists
            query = "SELECT COUNT(*) FROM mysql.user WHERE User = %s"
            cursor.execute(query, (name,))
            if cursor.fetchone()[0] == 1:
                print(f"User {name} exists.")

                # Revoke all existing permissions
                revoke_query = """
                REVOKE ALL PRIVILEGES ON *.* FROM %s@'%';
                """
                cursor.execute(revoke_query, (name,))
                print(f"All permissions revoked for {name}.")

                # Grant new permissions
                grant_query = """
                GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, ALTER, INDEX
                ON *.* TO %s@'%';
                """
                cursor.execute(grant_query, (name,))
                print(f"New permissions granted for {name}.")

                # Apply changes
                cursor.execute("FLUSH PRIVILEGES;")
            else:
                print(f"User {name} does not exist.")

except FileNotFoundError:
    print(f"File not found: {csv_file_path}.")
except csv.Error as e:
    print(f"Error reading CSV file: {e}")

# Commit changes and close the connection
mydb.commit()
cursor.close()
mydb.close()
