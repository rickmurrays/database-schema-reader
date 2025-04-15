import json
import os

class JSONWriter:
    """
    A class to handle writing structured data to JSON files.
    """

    def __init__(self, output_dir='schemas'):
        """
        Initializes the JSONWriter with the directory to store JSON files.

        :param output_dir: Directory to save JSON files. Defaults to 'schemas'.
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def write(self, data, filename):
        """
        Writes the given data to a JSON file with the specified filename.

        :param data: Data to be written to the file.
        :param filename: Name of the file to write the data to (e.g., 'schema.table.json').
        """
        file_path = os.path.join(self.output_dir, filename)

        # Ensure the filename ends with .json extension
        if not filename.endswith('.json'):
            filename += '.json'
            file_path = os.path.join(self.output_dir, filename)

        # Write the data to the file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        
        print(f"✅ Schema for {filename} saved successfully at {file_path}.")

    def write_multiple(self, data_list, filenames):
        """
        Writes multiple JSON files in bulk.

        :param data_list: List of data dictionaries to be written.
        :param filenames: List of filenames to save the data to.
        """
        for data, filename in zip(data_list, filenames):
            self.write(data, filename)
