import os
from config_loader import ConfigLoader
from database_connection_factory import DatabaseConnectionFactory
from database_schema_factory import DatabaseSchemaFactory
from json_writer import JSONWriter

class DatabaseSchemaReader:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load()
        self.db_type = self.config['db_type'].lower()
        self.connection = None
        self.output_dir = self.config.get('output_dir', 'schemas')
        self.schemas_to_process = self.config.get('schemas', None)
        self.tables_to_process = self.config.get('tables', {})
        self.column_aliases = self.config.get('column_aliases', {})
        self.schema_handler = None
        self.json_writer = JSONWriter(output_dir=self.output_dir)

    def connect(self):
        """ Use DatabaseConnectionFactory to create the appropriate connection """
        self.connection = DatabaseConnectionFactory.create_connection(self.config, self.db_type)

    def get_tables(self):
        """ Get list of tables from the database using the schema handler """
        schema = self.schemas_to_process[0]  # Use the first schema for simplicity
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'"
        tables_df = self.connection.read_table(query)
        tables = tables_df.collect()  # Get table names as a list
        return [table['table_name'] for table in tables]

    def get_columns(self, schema_name, table_name):
        """ Get columns for a specific table, including PK and FK information using PySpark """
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = '{schema_name}' AND table_name = '{table_name}'
        """
        columns_df = self.connection.read_table(query)
        columns = columns_df.collect()

        column_data = []
        for col in columns:
            column_data.append({
                'COLUMN_NAME': col['column_name'],
                'DATA_TYPE': col['data_type'],
                'IS_NULLABLE': col['is_nullable'],
                'PRIMARY_KEY': False,  # Placeholder for PK logic
                'FOREIGN_KEY': False   # Placeholder for FK logic
            })
        return column_data

    def apply_column_aliases(self, schema_name, table_name, column_data):
        """ Apply column aliases to the columns if specified in the config file """
        table_key = f"{schema_name}.{table_name}"
        aliases = self.column_aliases.get(table_key, {})

        for column in column_data:
            original_name = column['COLUMN_NAME']
            if original_name in aliases:
                column['COLUMN_NAME'] = aliases[original_name]

        return column_data

    def export_schema_to_json_files(self):
        """ Export the schema to JSON files for each table using JSONWriter """
        tables = self.get_tables()
        for schema in self.schemas_to_process:
            for table in tables:
                columns = self.get_columns(schema_name=schema, table_name=table)

                # Apply column aliases
                columns = self.apply_column_aliases(schema_name=schema, table_name=table, column_data=columns)

                # Create structured data for the table schema
                table_schema = {
                    "schema": schema,
                    "table": table,
                    "columns": []
                }

                # Add column details to the table schema
                for col in columns:
                    column_data = {
                        "name": col['COLUMN_NAME'],
                        "data_type": col['DATA_TYPE'],
                        "is_nullable": col['IS_NULLABLE'],
                        "primary_key": col['PRIMARY_KEY'],
                        "foreign_key": col['FOREIGN_KEY']
                    }
                    table_schema["columns"].append(column_data)

                # Construct the filename for the JSON file
                filename = f"{schema}.{table}.json".replace(" ", "_")

                # Use the JSONWriter to save the schema data to a JSON file
                self.json_writer.write(table_schema, filename)

    def close(self):
        """ Close the database connection """
        if self.connection:
            print("🔒 Connection closed.")
