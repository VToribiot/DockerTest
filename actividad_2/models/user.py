import datetime
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema, MongoException, MongoError
from bson import json_util
from bson.objectid import ObjectId


class User(Schema):
    schema_name = "users"

    # Attributes
    id = None
    email = None
    password = None

    def __init__(self, **kwargs):
        self.schema = {
            "email": {
                "type": Types.String,
                "required": True
            },
            "password": {
                "type": Types.String,
                "required": True
            },
        }

        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self):
        return f"Username: {self.username}, Password: {self.password}"
