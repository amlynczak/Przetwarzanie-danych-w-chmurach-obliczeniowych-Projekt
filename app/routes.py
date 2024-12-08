from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import Optional
from app.services import add_person, get_all_people, delete_person, set_relationship, delete_relationship, update_person, get_person_by_id, get_all_marriages, get_all_siblings
from fastapi.responses import FileResponse

router = APIRouter()

class Person(BaseModel):
    firstName: str
    lastName: str
    gender: Optional[str] = None
    birthDate: str
    deathDate: Optional[str] = None

@router.get("/")
def index():
    return FileResponse("app/static/index.html")

@router.post("/api/person")
def create_person(person: Person):
    return add_person(person.dict())

@router.get("/api/person/{person_id}")
def get_person(person_id: int):
    person = get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.get("/api/people")
def list_people():
    people = get_all_people()
    if not people:
        raise HTTPException(status_code=404, detail="No people found")
    return people

@router.delete("/api/person/{person_id}")
def remove_person(person_id: int):
    if not delete_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted successfully"}

@router.put("/api/person/{person_id}")
def modify_person(person_id: int, person: Person):
    return update_person(person_id, person.dict())

@router.post("/api/relationship")
def create_relationship(person1_id: int = Form(...), person2_id: int = Form(...), relationship_type: str = Form(...), marriage_date: Optional[str] = Form(None)):
    return set_relationship(person1_id, person2_id, relationship_type, marriage_date)

@router.delete("/api/relationship")
def remove_relationship(person1_id: int = Query(...), person2_id: int = Query(...)):
    if not delete_relationship(person1_id, person2_id):
        raise HTTPException(status_code=404, detail="Relationship not found")
    return {"message": "Relationship deleted successfully"}

@router.get("/api/marriages")
def list_marriages():
    marriages = get_all_marriages()
    if not marriages:
        raise HTTPException(status_code=404, detail="No marriages found")
    return marriages

@router.get("/api/siblings")
def list_siblings():
    siblings = get_all_siblings()
    if not siblings:
        raise HTTPException(status_code=404, detail="No siblings found")
    return siblings