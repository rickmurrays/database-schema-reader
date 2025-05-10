import sys
from config_loader import ConfigLoader
from database_schema_reader import DatabaseSchemaReader
from json_writer import JSONWriter

def main(config_file):
    """
    Main function to load the config, process the schema, and save to JSON files.
    
    :param config_file: Path to the configuration JSON file.
    """
    try:
        # Step 1: Load the configuration
        print("📥 Loading configuration...")
        config_loader = ConfigLoader(config_file)
        config_loader.load()

        # Step 2: Initialize the DatabaseSchemaReader
        print("🔗 Initializing database connection and schema reader...")
        schema_reader = DatabaseSchemaReader(config_loader)
        schema_reader.connect()

        # Step 3: Process and retrieve schema details for tables
        print("📊 Retrieving schema data...")
        schema_reader.export_schema_to_json_files()

        print("✅ All schemas have been successfully exported to JSON files.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example: 'config.json' is the configuration file to be used
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)
