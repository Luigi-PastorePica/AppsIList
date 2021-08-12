class Resource:
    def __init__(self):
        self.rid: int
        self.title: str
        self.image_link: str
        self.category: str
        self.rating: float

    # def __init__(self, rid: int, title: str, image_link: str, category: str, rating: float):
    def __init__(self, resource_data: dict):
        self.rid: int = resource_data["rid"]
        self.title: str = resource_data["title"]
        self.image_link: str = resource_data["image_link"]
        self.category: str = resource_data["category"]
        self.rating: float = resource_data["rating"]

    def set_id(self):
        pass

    def set_title(self):
        pass

    def set_image_link(self):
        pass

    def set_category(self):
        pass

    def set_rating(self):
        pass

    def get_id(self):
        pass

    def get_title(self):
        pass

    def get_image_link(self):
        pass

    def get_category(self):
        pass

    def get_rating(self):
        pass
