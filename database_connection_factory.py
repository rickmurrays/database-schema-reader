from pyspark.sql import SparkSession

class DatabaseConnectionFactory:
    @staticmethod
    def create_connection(config, db_type):
        """
        Creates a Spark session with JDBC connection to the specified database.
        """
        spark = SparkSession.builder \
            .appName("DatabaseSchemaReader") \
            .config("spark.jars", config['jdbc_jar']) \
            .getOrCreate()

        if db_type == "sql_server":
            return SQLServerConnection(spark, config)
        elif db_type == "oracle":
            return OracleConnection(spark, config)
        elif db_type == "teradata":
            return TeradataConnection(spark, config)
        else:
            raise ValueError("Unsupported database type")

class SQLServerConnection:
    def __init__(self, spark, config):
        self.spark = spark
        self.url = f"jdbc:sqlserver://{config['server']};database={config['database']}"
        self.properties = {
            "user": config["username"],
            "password": config["password"],
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }

    def read_table(self, table_name):
        """ Read data from a table in SQL Server """
        return self.spark.read.jdbc(url=self.url, table=table_name, properties=self.properties)

class OracleConnection:
    def __init__(self, spark, config):
        self.spark = spark
        self.url = f"jdbc:oracle:thin:@//{config['server']}:{config['port']}/{config['sid']}"
        self.properties = {
            "user": config["username"],
            "password": config["password"],
            "driver": "oracle.jdbc.driver.OracleDriver"
        }

    def read_table(self, table_name):
        """ Read data from a table in Oracle """
        return self.spark.read.jdbc(url=self.url, table=table_name, properties=self.properties)

class TeradataConnection:
    def __init__(self, spark, config):
        self.spark = spark
        self.url = f"jdbc:teradata://{config['server']}/DATABASE={config['database']}"
        self.properties = {
            "user": config["username"],
            "password": config["password"],
            "driver": "com.teradata.jdbc.TeraDriver"
        }

    def read_table(self, table_name):
        """ Read data from a table in Teradata """
        return self.spark.read.jdbc(url=self.url, table=table_name, properties=self.properties)
