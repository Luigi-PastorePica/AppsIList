from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

from resource import Resource as Resource

# TODO need to add a "resource_type" field (e.g. book, blogpost, video, course, etc.). This would work for the basic view.
fieldnames = ["id", "title", "media", "description", "numerical", "external_link", "list"]  # TODO Handle differently
basic_fieldnames = ["id", "title", "media", "numerical"]  # TODO Handle differently


class MyDatabase:

    def __init__(self, file_name: str):
        self.db_name = file_name
        self.db: [dict] = []  # TODO this should change to be a list of Resource objects.
        self.current_id = self.get_newest_id()

    def load_basic_data(self) -> list:
        '''
        Loads basic data from entries in the "database" into memory

        Returns:
            self.db ([dict]): A list of dictionaries. Each dictionary holds basic data for one database entry
        '''

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
        '''Load entries in "database" into memory'''
        # TODO Deprecate..... maybe
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                row["list"] = eval(row["list"])  # String to Dict
                self.db.append(row)

        return self.db

    def get_newest_id(self) -> int:
        # TODO This is a hack, find if there is a more efficient way of doing this
        newest_id = 0
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                newest_id = int(row["id"])

        return newest_id

    def add_resource(self, resource_data: dict) -> int:

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
            # TODO return something that tells the user the record could not be created
            raise e

        newest_id = int(item_row["id"])

        if newest_id == self.get_newest_id():
            self.current_id = self.get_newest_id()
        else:
            # TODO Find a way to notify that something went wrong
            pass

        return newest_id

    def format_new_resource(self, resource_data: dict) -> dict:
        '''
        Creates a new row/entry for the database in a dictionary format

            Parameters:
                resource_data(dict): Contains the data of the record to be added to the database.

            Returns:
                item_row(dict): Contains properly formatted data for the new record to be added to the database
        '''

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
        '''
        Searches for occurrences of the given string in the database


        '''

        search_str_lower = search_str.lower()
        title_results: [dict] = []
        content_results: [dict] = []
        results: (list, list) = (None, None)

        # TODO Too many levels of abstraction
        resource_basic: dict = {}
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
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
