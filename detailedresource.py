from resource import Resource


class DetailedResource(Resource):

    def __init__(self, detailed_resource_data):
        # TODO Might not need the two dictionaries, I can just pass a single dict with as much or little info as needed
        resource_data: dict = {
            "rid": detailed_resource_data["rid"],
            "title": detailed_resource_data["title"],
            "image_link": detailed_resource_data["image_link"],
            "category": detailed_resource_data["category"],
            "rating": detailed_resource_data["rating"]
        }
        super(DetailedResource, self).__init__(resource_data)

        self.length: str = detailed_resource_data["length"]
        self.description: str = detailed_resource_data["description"]
        self.origin: str = detailed_resource_data["origin"]
        self.reviews: str = detailed_resource_data["reviews"]

    def set_length(self):
        pass

    def set_description(self):
        pass

    def set_origin(self):
        pass

    def set_reviews(self):
        pass

    def get_length(self):
        pass

    def get_description(self):
        pass

    def get_origin(self):
        pass

    def get_reviews(self):
        pass

    def to_dict(self):
        pass

    def to_json(self):
        pass

# TODO Need to provide a to_json and/or to_dict conversion