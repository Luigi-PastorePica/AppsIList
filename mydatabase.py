from csv import DictReader, DictWriter
from json import dumps as dumps
from copy import deepcopy as deepcopy

# db = []
current_id = 12  # TODO get from last item in csv file
fieldnames = ["id", "title", "media", "description", "numerical", "external_link", "list"]  # TODO Handle differently


class MyDatabase:

    def __init__(self, file_name: str):
        self.db_name = file_name
        self.db: dict = []

    # Load entries in "database" into memory
    def load_data(self) -> list:
        with open(self.db_name, "r") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                row["list"] = eval(row["list"])  # String to Dict
                self.db.append(row)

        return self.db
