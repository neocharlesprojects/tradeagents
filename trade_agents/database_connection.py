
class DatabaseConnection:
    def __init__(self, database_name="test_db"):
        self.database_name = database_name
        self.connected = False
        self.tables = []

    def _ensure_database_exists(self):
        print(f"Ensuring database '{self.database_name}' exists.")

    def connect(self):
        if not self.connected:
            self.connected = True
            print(f"Connected to database '{self.database_name}'.")

    def close(self):
        if self.connected:
            self.connected = False
            self.tables.clear()
            print(f"Closed connection to database '{self.database_name}'.")
        else:
            print("Connection already closed.")

    def create_table(self, table_name):
        if self.connected:
            if table_name not in self.tables:
                self.tables.append(table_name)
                print(f"Table '{table_name}' created.")
            else:
                print(f"Table '{table_name}' already exists.")
        else:
            print("Cannot create table. No active connection.")

    def list_tables(self):
        return self.tables if self.connected else []
