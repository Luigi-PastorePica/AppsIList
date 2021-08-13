from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

from resource import Resource as Resource

# TODO Handle differently. Create a class method that retrieves fieldnames from db headers.
fieldnames = ["id", "title", "format", "media", "description", "numerical", "external_link", "list"]
basic_fieldnames = ["id", "title", "format", "media", "numerical"]

class MyDatabase:
    """
    Handles interactions with the database for the AppsIList web application.
    """

    def __init__(self, file_name: str):
        """
        Constructor for the MyDatabase class.

        :param file_name: A string containing the path to the CSV file.
        """
        self.db_name = file_name
        self.db: [dict] = []  # TODO this should change to be a list of Resource objects.
        self.current_id = self.get_newest_id()

    def load_basic_data(self) -> [dict]:
        """
        Loads basic data from entries in the "database" into memory.

        :return self.db: A list of dictionaries. Each dictionary holds basic data for one database entry/row.
        """

        # TODO Too many levels of abstraction. Might need to extract functionality.
        resource_basic: dict = {}
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                for field in basic_fieldnames:
                    resource_basic[field] = row[field]
                self.db.append(deepcopy(resource_basic))
        return self.db

    def load_detailed_resource(self, rid: int) -> dict:
        """
        Loads all information in the database for a single resource. The resource is identified by rid.

        :param rid: An integer that represents the unique resource id in the database.
        :return resource_data: A dictionary containing a single resource's information.
        """

        # TODO consider case where rid is not found. This should not happen, but still, it is good to have a backup
        resource_data: dict = {}
        rid_str = str(rid)  # This conversion will be done away with when db transitions into using RDB instead of csv.
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                if row["id"] == rid_str:
                    row["list"] = eval(row["list"])  # String to Dict for reviews
                    resource_data = row
                    # print("Resource with id {} found: {}".format(rid_str, row))  # Debugging
                    break

        return resource_data

    def load_data(self) -> [dict]:
        """
        Load entries in database into memory.
        Note: This method is not in use and it remains to be seen whether there are cases where can still be useful.

        :return self.db: A dictionary containing all data from all entries in the database.
        """

        # TODO Be on the lookout for cases where this method might be useful. If not, eventually deprecate.
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                row["list"] = eval(row["list"])  # String to Dict
                self.db.append(row)

        return self.db

    def get_newest_id(self) -> int:
        """
        Retrieves the highest id in the database

        :return newest_id: An integer representing the highest id in the database.
        """

        # TODO This is a hacky implementation. Find a more efficient way of doing this
        newest_id = 0
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                newest_id = int(row["id"])

        return newest_id

    def add_resource(self, resource_data: dict) -> int:
        """
        Adds a new resource to the database based on the information contained in resource_data.

        :param resource_data: A dictionary containing all data fields for the entry that needs to be created in the db.
        :return newest_id: The unique id for the newly created entry, regardless of success or failure in creating said
        entry.
        """

        item_row = self.format_new_resource(resource_data)
        # print("resource_data (previously json_data):\n{}".format(resource_data))  # Debugging

        # Write new item to database
        try:
            with open(self.db_name, "a") as csvfile:
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(item_row)
        except FileNotFoundError as e:
            print(e, "Creating new file")
            with open("data.csv", "w") as output_file:
                writer = DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(item_row)
        except Exception as e:
            # TODO return exception/error that tells the user the record could not be created
            raise e

        newest_id = int(item_row["id"])

        if newest_id == self.get_newest_id():
            self.current_id = self.get_newest_id()
        else:
            # newest_id -= 1
            # TODO Find an appropriate error/exception to notify that something went wrong
            pass

        return newest_id

    def format_new_resource(self, resource_data: dict) -> dict:
        """
        Properly formats a new row/entry for the database.

        :param resource_data: A dictionary containing all the data of the record to be added to the database.
        :returns item_row: A dictionary holding properly formatted data for the entry to be added to the database.
        """

        newest_id = self.current_id + 1
        item_row: dict = {}

        # Creating row to be stored
        for field_name in fieldnames:
            if field_name == "id":
                item_row[field_name] = newest_id
            elif field_name == "list":
                # print("type of json_data[\"list_elem\"]:\n{}".format(type(resource_data["list_elem"])))  # Debugging
                # print("json_data[\"list_elem\"]:\n{}".format(resource_data["list_elem"]))  # Debugging
                # print("dumps(json_data[\"list_elem\"]:\n{}".format(dumps(resource_data["list_elem"])))  # Debugging
                user_id = resource_data["list_elem"].keys();
                # Using string instead of boolean simplifies storage and retrieval from a csv file
                resource_data["list_elem"][list(user_id)[0]]["mark_as_deleted"] = "False"
                item_row[field_name] = dumps(resource_data["list_elem"])  # Dict to String (for review entries)
            elif field_name is None or resource_data[field_name] is None:
                item_row[field_name] = None
            else:
                item_row[field_name] = resource_data[field_name]

        return item_row

    def search_for_string(self, search_str:str) -> ([dict], [dict]):
        """
        Searches for occurrences of the given string in the database. Currently it looks in title and description.

        :param search_str: A string containing a word or word fraction to be searched in the database's entries.

        :return results: A tuple containing two lists. The first list holds one dictionary per database entry that
        contains search_str in its title. The second list holds one dictionary per database entry that contains
        search_str in other fields (currently only in the description).
        """

        search_str_lower = search_str.lower()
        title_results: [dict] = []
        content_results: [dict] = []
        results: (list, list) = (None, None)

        # TODO Too many levels of abstraction
        resource_basic: dict = {}
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                # TODO Extract conditional into its own method
                if search_str_lower in row["title"].lower():
                    for field in basic_fieldnames:
                        resource_basic[field] = row[field]
                    title_results.append(deepcopy(resource_basic))
                elif search_str_lower in row["description"].lower():
                    for field in basic_fieldnames:
                        resource_basic[field] = row[field]
                    content_results.append(deepcopy(resource_basic))

        results = (title_results, content_results)

        return results
