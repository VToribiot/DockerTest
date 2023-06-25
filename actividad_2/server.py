import json
from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values 
from pymongo import MongoClient
from pymongoose.methods import set_schemas
from bson.json_util import dumps

from models.person import Person
from models.user import User

app = FastAPI()
uri = dotenv_values('.env')['uri']
client = MongoClient(uri)
db = client.test
person = db.persons
user = db.users
schemas = {
    "persons": Person(empty=True).schema,
    "users": User(empty=True).schema
}
set_schemas(db, schemas, False)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/persons", tags=["Person"])
async def get_persons():
    try:
        persons = json.loads(dumps(list(person.find({}))))
        if persons == []:
            raise HTTPException(status_code=204)
    except Exception:
        raise HTTPException(status_code=404, detail="Items not found")
    return persons

@app.post('/persons/{myname}/{mylastname}/{myemail}', status_code=201, tags=["Person"])
async def create_person(myname: str, mylastname: str, myemail: str):
    try:
        person = Person(
            name=myname,
            lastname=mylastname,
            email=myemail,
        )
        person.save()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    
    return "Person created"
    
@app.get("/persons/{name}", tags=['Person'])
async def get_one_person(name: str):
    try:
        person = person.find_one({"name": name}, {"_id": 0})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return person

@app.put("/persons/{name}/{email}", tags=['Person'])
async def update_person(name: str, email: str):
    try:
        person.update_one(
            {"name": name},
            {"$set": {"email": email}},
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return f"Person {name} updated, to new email: {email}"

@app.delete("/persons/{name}", tags=['Person'])
async def delete_person(name: str):
    try:
        person.delete_one({"name": name})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return f"Person {name} deleted"

@app.get("/users", tags=["User"])
async def get_users():
    try:
        users = json.loads(dumps(list(user.find({}))))
        if users == []:
            raise HTTPException(status_code=204)
    except Exception:
        raise HTTPException(status_code=404, detail="Items not found")
    return users

@app.post('/users/{email}/{password}', status_code=201, tags=["User"])
async def create_user(email: str, password: str):
    try:
        user = User(
            email=email,
            password=password
        )
        x = user.save()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    
    return "User created"
    
@app.get("/users/{email}", tags=['User'])
async def get_one_user(email: str):
    try:
        myuser = user.find_one({"email": email}, {"_id": 0})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return myuser

@app.put("/users/{email}/{newpass}", tags=['User'])
async def update_user(email: str, newpass: str):
    try:
        user.update_one(
            {"email": email},
            {"$set": {"password": newpass}},
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return f"User {email} updated, to new password: {newpass}"

@app.delete("/users/{email}", tags=['User'])
async def delete_user(email: str):
    try:
        user.delete_one({"email": email})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return f"User {email} deleted"

@app.get('/personuser')
async def get_user_person():
    try:
        pipeline = [
            {"$lookup": {"from": "users", "localField": "email", "foreignField": "email", "as": "user_email"}}
        ]
        info = json.loads(dumps(list(person.aggregate(pipeline))))
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return info
