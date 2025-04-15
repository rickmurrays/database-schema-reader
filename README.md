# Database Schema Generator

This project provides a Python solution to extract schema information (tables, columns, constraints) from different types of databases, including SQL Server, Oracle, and Teradata. The extracted schema data is written into structured JSON files, which can then be used for further processing or analysis.

## Components

#### **ConfigLoader**
   - **Purpose**: Loads and parses the configuration file (`config.json`), which contains the database connection details, schema and table information, and output configuration.
   - **Usage**: The `ConfigLoader` is used to read the configuration file and store the parsed information in a dictionary format.

#### **DatabaseConnectionFactory**
   - **Purpose**: Creates a connection to the database based on the configuration. Supports connections to SQL Server, Oracle, and Teradata using PySpark.
   - **Usage**: Used by the `DatabaseSchemaReader` to establish a connection to the database.

#### **DatabaseSchemaFactory**
   - **Purpose**: A factory class that creates the appropriate schema handler based on the database type (SQL Server, Oracle, or Teradata). The schema handler is responsible for retrieving tables, columns, and constraints from the database.
   - **Usage**: This is used to instantiate the correct handler for interacting with the database schema and extracting metadata.

#### **DatabaseSchemaReader**
   - **Purpose**: Orchestrates the process of connecting to the database, reading schema metadata (tables and columns), and exporting the data into JSON files.
   - **Usage**: Used to connect to the database, retrieve schema details, and write the information to files using the `JSONWriter`.

#### **JSONWriter**
   - **Purpose**: Writes the extracted schema data (tables, columns, constraints) to structured JSON files. Each table will be written to a separate JSON file.
   - **Usage**: Used by `DatabaseSchemaReader` to save the extracted schema metadata into JSON files.

#### **Main**
   - **Purpose**: The main entry point of the application. It ties together all components by loading the configuration, connecting to the database, retrieving schema data, and writing it to JSON files.
   - **Usage**: This script is run from the command line and processes the schemas and tables defined in the configuration file.


## Configuration File (`config.json`)

The configuration file defines the database connection details, schemas and tables to process, and output directory for the generated JSON files.

#### Example `config.json`:

```json
{
    "db_type": "sql_server",
    "server": "localhost",
    "database": "my_database",
    "username": "my_user",
    "password": "my_password",
    "jdbc_jar": "/path/to/sqljdbc4.jar",
    "schemas": ["public", "sales"],
    "tables": {
        "public": ["employees", "departments"],
        "sales": ["orders"]
    },
    "column_aliases": {
        "public.employees": {
            "employee_id": "emp_id",
            "first_name": "fname",
            "last_name": "lname"
        }
    },
    "output_dir": "schemas_output"
}
```

#### Configuration Fields:

- `db_type`: Specifies the database type. It can be sql_server, oracle, or teradata.
- `server`, database, username, password: Database connection credentials.
- `jdbc_jar`: Path to the JDBC driver JAR (needed for PySpark JDBC connections).
- `schemas`: List of schemas to process.
- `tables`: A dictionary that maps each schema to a list of tables to process.
- `column_aliases`: A dictionary where the key is the schema and table name (e.g., public.employees), and the value is a mapping of original column names to aliases.
- `output_dir`: The directory where the JSON files will be saved.


## Installation

Clone the Repository:

```bash
git clone https://your-git-repository-url.git
cd your-project-folder
```

Install Dependencies:

```bash
pip install pyspark
```

The project uses PySpark for database connectivity and JSON handling. Install the necessary dependencies using `pip`.
You may also need to download the appropriate JDBC driver for your database type (e.g., SQL Server, Oracle, or Teradata) and specify its path in the `jdbc_jar field` of `config.json`.


## How to Run

Prepare the Configuration File:

- Ensure that your config.json file is correctly set up with the appropriate database connection details, schemas, tables, and output directory. The configuration file must be passed as an argument when running the main module.

Run the Main Script:

- The main script will load the configuration, connect to the database, retrieve the schema details, and write the data to JSON files in the specified output directory.
   ```bash
   python main.py config.json
   ```
- Replace `config.json` with the path to your actual configuration file if it's located in a different directory.


## Output

After running the script, you will find the generated JSON files in the schemas_output directory (or the directory specified in the output_dir field of the configuration file). Each table will have its own JSON file, named in the format `schema.table.json`.

#### Example Output Files:
- schemas_output/public.employees.json
- schemas_output/public.departments.json
- schemas_output/sales.orders.json

The output JSON files will contain the following schema details for each table:
- **Table name**
- **Columns**: Name, data type, nullable status, primary and foreign key information.
- **Constraints**: Primary keys, foreign keys, etc.


## How it Works

#### Configuration Loading:

- The `ConfigLoader` loads the database connection details and schema/table settings from the `config.json` file.

#### Database Connection:

- The `DatabaseConnectionFactory` establishes a connection to the database based on the provided details (using PySpark JDBC).

#### Schema Extraction:

- The `DatabaseSchemaFactory` instantiates the appropriate schema handler (`SQLServerSchemaHandler`, `OracleSchemaHandler`, or `TeradataSchemaHandler`) based on the `db_type` specified in the config file.
- The handler retrieves schema metadata, including tables, columns, and constraints (if applicable).

#### JSON File Writing:

- The `JSONWriter` saves the extracted schema data to individual JSON files for each table.


## Customization

- **Column Aliases**: The column_aliases section in the configuration file allows you to specify new names for columns. This can be useful if you want to standardize or rename columns before exporting.
- **Multiple Databases**: You can extend this tool to support additional databases by adding new classes to the `database_schema_factory.py` file. Each new database should implement the `DatabaseSchemaHandler` interface.
- **Adding More Tables or Schemas**: You can specify multiple schemas and tables to extract in the configuration file, allowing you to process a variety of databases.
- **Output Directory**: You can customize the output directory in the configuration file. By default, the output is stored in `schemas_output`, but you can change it to any directory of your choice.


## Troubleshooting

#### Connection Issues: 
- Ensure that the database credentials and JDBC driver path are correctly configured in the `config.json` file.
   - For SQL Server, check that the `sqljdbc4.jar` driver is correctly specified.
   - For Oracle, ensure the appropriate Oracle JDBC driver is available.
   - For Teradata, ensure the Teradata JDBC driver is set correctly.

#### Missing JDBC Drivers:
- If you're connecting to a database (e.g., SQL Server, Oracle), ensure that the appropriate JDBC driver JAR file is specified in the `jdbc_jar` field of the configuration.

#### Missing Tables:
- If certain tables are not being processed, verify that the correct schema and table names are listed in the schemas and tables sections of `config.json`.

#### Permission Issues:
- Ensure that the database user specified in the configuration has the necessary permissions to access the schemas and tables you want to export.

#### File Writing Issues:
- If you encounter issues writing the JSON files, check the permissions for the `output_dir` directory and ensure it is writable.
