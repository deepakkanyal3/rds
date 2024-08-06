# rds
# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install the required package
pip install mysql-connector-python

# Run your Python script
python usercsv.py

# for documentdb
pip3 install pymongo


# give full path
/Users/deepak/rds/users.csv

# General Roles for documentdb
read:

Permissions: Provides read-only access to the data in a specific database.
Use Case: For users who need to view but not modify data.
Example:
json
Copy code
# { "role": "read", "db": "myDatabase" }
readWrite:

Permissions: Allows both read and write access to a specific database.
Use Case: For users who need to perform read and write operations on a specific database.
Example:
json
Copy code
# { "role": "readWrite", "db": "myDatabase" }
dbAdmin:

Permissions: Provides administrative access to a specific database, including the ability to create or modify indexes and view collection statistics.
Use Case: For users who need to manage and monitor a specific database but not perform operations on other databases or the cluster.
Example:
json
Copy code
# { "role": "dbAdmin", "db": "myDatabase" }
dbAdminAnyDatabase:

Permissions: Grants administrative rights on all databases, allowing the user to perform administrative operations such as managing indexes and views.
Use Case: For users who need broader administrative capabilities across multiple databases.
Example:
json
Copy code
# { "role": "dbAdminAnyDatabase", "db": "admin" }
userAdmin:

Permissions: Allows management of users and roles within a specific database.
Use Case: For users responsible for creating, modifying, and deleting users and roles.
Example:
json
Copy code
# { "role": "userAdmin", "db": "myDatabase" }
userAdminAnyDatabase:

Permissions: Grants user management capabilities across all databases.
Use Case: For users who need to manage users and roles across the entire MongoDB deployment.
Example:
json
Copy code
# { "role": "userAdminAnyDatabase", "db": "admin" }
clusterAdmin:

Permissions: Provides administrative access to the entire cluster, including the ability to manage replica sets and sharding.
Use Case: For users who need full administrative control over the MongoDB cluster.
Example:
json
Copy code
# { "role": "clusterAdmin", "db": "admin" }
readWriteAnyDatabase:

Permissions: Grants read and write access to all databases.
Use Case: For users who need comprehensive access to all databases for read and write operations.
Example:
json
Copy code
# { "role": "readWriteAnyDatabase", "db": "admin" }
Roles for Monitoring and Administrative Tasks
clusterManager:

Permissions: Allows a user to manage and monitor the MongoDB cluster.
Use Case: For users who need to perform cluster management tasks but not full administrative tasks.
Example:
json
Copy code
# { "role": "clusterManager", "db": "admin" }
clusterMonitor (as previously described):

Permissions: Provides read-only access to cluster-level monitoring commands and data.
Use Case: For users who need visibility into cluster health and performance without making changes.
Example:
json
Copy code
# { "role": "clusterMonitor", "db": "admin" }



