import datetime
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema, MongoException, MongoError
from bson import json_util
from bson.objectid import ObjectId


class Person(Schema):
    schema_name = "persons"
    
    # Attributes
    id = None
    name = None
    lastname = None
    email = None

    def __init__(self, **kwargs):
        self.schema = {
            "name": {
                "type": Types.String,
                "required": True
            },
            "lastname": {
                "type": Types.String,
                "required": True
            },
            "email": {
                "type": Types.String,
                "required": True
            } 
        }

        super().__init__(self.schema_name, self.schema, kwargs)


    def __str__(self):
        return f"Name: {self.name}, Last Name: {self.lastname}, Email: {self.email}"