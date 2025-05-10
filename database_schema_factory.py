from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

class DatabaseSchemaHandler(ABC):
    """
    Abstract class for database schema handlers. 
    Specific database types will implement methods to retrieve schema information.
    """
    
    @abstractmethod
    def get_tables(self, schemas_to_process):
        pass
    
    @abstractmethod
    def get_columns_with_constraints(self, schema_name, table_name):
        pass


class SQLServerSchemaHandler(DatabaseSchemaHandler):
    def __init__(self, connection):
        self.connection = connection

    def get_tables(self, schemas_to_process):
        schema = schemas_to_process[0]  # For simplicity, using the first schema
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'"
        return self.connection.read_table(query)

    def get_columns_with_constraints(self, schema_name, table_name):
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'
        """
        columns_df = self.connection.read_table(query)
        columns = columns_df.collect()

        column_data = []
        for col in columns:
            column_data.append({
                'COLUMN_NAME': col['COLUMN_NAME'],
                'DATA_TYPE': col['DATA_TYPE'],
                'IS_NULLABLE': col['IS_NULLABLE'],
                'PRIMARY_KEY': False,  # Placeholder for PK logic
                'FOREIGN_KEY': False   # Placeholder for FK logic
            })
        return column_data


class OracleSchemaHandler(DatabaseSchemaHandler):
    def __init__(self, connection):
        self.connection = connection

    def get_tables(self, schemas_to_process):
        schema = schemas_to_process[0]  # For simplicity, using the first schema
        query = f"SELECT table_name FROM all_tables WHERE owner = '{schema}'"
        return self.connection.read_table(query)

    def get_columns_with_constraints(self, schema_name, table_name):
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE, NULLABLE
            FROM ALL_TAB_COLUMNS 
            WHERE OWNER = '{schema_name}' AND TABLE_NAME = '{table_name}'
        """
        columns_df = self.connection.read_table(query)
        columns = columns_df.collect()

        column_data = []
        for col in columns:
            column_data.append({
                'COLUMN_NAME': col['COLUMN_NAME'],
                'DATA_TYPE': col['DATA_TYPE'],
                'IS_NULLABLE': col['NULLABLE'],
                'PRIMARY_KEY': False,  # Placeholder for PK logic
                'FOREIGN_KEY': False   # Placeholder for FK logic
            })
        return column_data


class TeradataSchemaHandler(DatabaseSchemaHandler):
    def __init__(self, connection):
        self.connection = connection

    def get_tables(self, schemas_to_process):
        schema = schemas_to_process[0]  # For simplicity, using the first schema
        query = f"SELECT table_name FROM dbc.tablesv WHERE databasename = '{schema}'"
        return self.connection.read_table(query)

    def get_columns_with_constraints(self, schema_name, table_name):
        query = f"""
            SELECT columnname, columndatatype, nullable
            FROM dbc.columnsv 
            WHERE databasename = '{schema_name}' AND tablename = '{table_name}'
        """
        columns_df = self.connection.read_table(query)
        columns = columns_df.collect()

        column_data = []
        for col in columns:
            column_data.append({
                'COLUMN_NAME': col['columnname'],
                'DATA_TYPE': col['columndatatype'],
                'IS_NULLABLE': col['nullable'],
                'PRIMARY_KEY': False,  # Placeholder for PK logic
                'FOREIGN_KEY': False   # Placeholder for FK logic
            })
        return column_data


class DatabaseSchemaFactory:
    """
    Factory class to instantiate the appropriate database schema handler based on the database type.
    """
    
    @staticmethod
    def create_schema(connection, db_type):
        if db_type == "sql_server":
            return SQLServerSchemaHandler(connection)
        elif db_type == "oracle":
            return OracleSchemaHandler(connection)
        elif db_type == "teradata":
            return TeradataSchemaHandler(connection)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
