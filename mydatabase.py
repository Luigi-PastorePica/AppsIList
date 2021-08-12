from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

# db = []
current_id = 12  # TODO get from last item in csv file
fieldnames = ["id", "title", "media", "description", "numerical", "external_link", "list"]  # TODO Handle differently


class MyDatabase:

    def __init__(self, file_name: str):
        self.db_name = file_name
        self.db: [dict] = []  # TODO this should change to be a list of Resource objects.

    # TODO Load only basic info.
    # Load entries in "database" into memory
    def load_basic_data(self) -> list:
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                row["list"] = eval(row["list"])  # String to Dict for reviews
                self.db.append(row)

        return self.db

    # TODO consider case where rid is not found. This should not happen, but still, it is good to have a backup
    def load_detailed_resource(self, rid: int) -> dict:
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

    # TODO Deprecate..... maybe
    # Load entries in "database" into memory
    def load_data(self) -> list:
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                row["list"] = eval(row["list"])  # String to Dict
                self.db.append(row)

        return self.db