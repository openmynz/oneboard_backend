from abc import ABC, abstractmethod

class DatabaseHandler(ABC):
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.transaction_started = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def start_transaction(self):
        pass

    @abstractmethod
    def commit_transaction(self):
        pass

    @abstractmethod
    def rollback_transaction(self):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, query):
        pass

    @abstractmethod
    def update(self, query, data):
        pass

    @abstractmethod
    def delete(self, query):
        pass

    @abstractmethod
    def setup_replication(self, replica_params):
        pass

class SQLDatabaseHandler(DatabaseHandler):
    def connect(self):
        # Implement SQL database connection logic
        pass

    def disconnect(self):
        # Implement SQL database disconnection logic
        pass

    def start_transaction(self):
        # Implement SQL transaction start logic
        self.transaction_started = True

    def commit_transaction(self):
        # Implement SQL transaction commit logic
        self.transaction_started = False

    def rollback_transaction(self):
        # Implement SQL transaction rollback logic
        self.transaction_started = False

    def create(self, data):
        # Implement SQL insert operation
        pass

    def read(self, query):
        # Implement SQL select operation
        pass

    def update(self, query, data):
        # Implement SQL update operation
        pass

    def delete(self, query):
        # Implement SQL delete operation
        pass

    def setup_replication(self, replica_params):
        # Implement SQL replication setup logic
        pass

class MongoDBHandler(DatabaseHandler):
    def connect(self):
        # Implement MongoDB connection logic
        pass

    def disconnect(self):
        # Implement MongoDB disconnection logic
        pass

    def start_transaction(self):
        # Implement MongoDB transaction start logic
        self.transaction_started = True

    def commit_transaction(self):
        # Implement MongoDB transaction commit logic
        self.transaction_started = False

    def rollback_transaction(self):
        # Implement MongoDB transaction rollback logic
        self.transaction_started = False

    def create(self, data):
        # Implement MongoDB insert operation
        pass

    def read(self, query):
        # Implement MongoDB find operation
        pass

    def update(self, query, data):
        # Implement MongoDB update operation
        pass

    def delete(self, query):
        # Implement MongoDB delete operation
        pass

    def setup_replication(self, replica_params):
        # Implement MongoDB replication setup logic
        pass

# Example usage:
sql_handler = SQLDatabaseHandler(connection_params={'host': 'localhost', 'user': 'root', 'password': 'password', 'database': 'example'})
sql_handler.connect()
sql_handler.start_transaction()
try:
    sql_handler.create({'name': 'John', 'age': 30})
    sql_handler.commit_transaction()
except Exception as e:
    sql_handler.rollback_transaction()
    print(f"Transaction failed: {e}")
finally:
    sql_handler.disconnect()

mongodb_handler = MongoDBHandler(connection_params={'host': 'localhost', 'port': 27017, 'database': 'example'})
mongodb_handler.connect()
mongodb_handler.start_transaction()
try:
    mongodb_handler.create({'name': 'Alice', 'age': 25})
    mongodb_handler.commit_transaction()
except Exception as e:
    mongodb_handler.rollback_transaction()
    print(f"Transaction failed: {e}")
finally:
    mongodb_handler.disconnect()
