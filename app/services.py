from app.database import get_db_driver

def add_person(person):
    driver = get_db_driver()
    query = """
    CREATE (p:Person {firstName: $firstName, lastName: $lastName, birthDate: $birthDate, deathDate: $deathDate})
    RETURN p
    """
    with driver.session() as session:
        result = session.run(query, **person)
    return {"message": "Osoba dodana pomyślnie"}

def get_person_by_id(person_id):
    driver = get_db_driver()
    query = """
    MATCH (p:Person)
    WHERE ID(p) = $person_id
    RETURN p, ID(p) AS id
    """
    with driver.session() as session:
        result = session.run(query, person_id=person_id)
        record = result.single()
        if record:
            person = dict(record["p"])
            person["id"] = record["id"]
            return person
        else:
            return None

def get_all_people():
    driver = get_db_driver()
    query = """
    MATCH (p:Person)
    OPTIONAL MATCH (p)<-[:PARENT_OF]-(father:Person {gender: 'male'})
    OPTIONAL MATCH (p)<-[:PARENT_OF]-(mother:Person {gender: 'female'})
    OPTIONAL MATCH (p)-[:MARRIED_TO]-(spouse:Person)
    WITH p, 
         ID(p) AS id,
         COALESCE(father.firstName + ' ' + father.lastName, '') AS father,
         COALESCE(mother.firstName + ' ' + mother.lastName, '') AS mother,
         COALESCE(spouse.firstName + ' ' + spouse.lastName, '') AS spouse
    RETURN DISTINCT p, id, father, mother, spouse
    """
    with driver.session() as session:
        result = session.run(query)
        people = []
        for record in result:
            person = dict(record["p"])
            person["id"] = record["id"]
            person["father"] = record["father"]
            person["mother"] = record["mother"]
            person["spouse"] = record["spouse"]
            people.append(person)
    return {"people": people}

def delete_person(person_id):
    driver = get_db_driver()
    query = """
    MATCH (p:Person)
    WHERE ID(p) = $person_id
    OPTIONAL MATCH (p)-[r]-()
    DELETE r, p
    """
    with driver.session() as session:
        result = session.run(query, person_id=person_id)
    return result.consume().counters.nodes_deleted > 0

def set_relationship(person1_id, person2_id, relationship_type, marriage_date=None):
    driver = get_db_driver()
    if relationship_type == "parent":
        query = """
        MATCH (p1:Person), (p2:Person)
        WHERE ID(p1) = $person1_id AND ID(p2) = $person2_id
        CREATE (p1)-[r:PARENT_OF]->(p2)
        RETURN r
        """
    elif relationship_type == "spouse":
        query = """
        MATCH (p1:Person), (p2:Person)
        WHERE ID(p1) = $person1_id AND ID(p2) = $person2_id
        CREATE (p1)-[r:MARRIED_TO {marriageDate: $marriage_date}]->(p2), (p2)-[r2:MARRIED_TO {marriageDate: $marriage_date}]->(p1)
        RETURN r, r2
        """
    with driver.session() as session:
        result = session.run(query, person1_id=int(person1_id), person2_id=int(person2_id), marriage_date=marriage_date)
    return {"message": "Relationship created successfully"}

def delete_relationship(person1_id, person2_id):
    driver = get_db_driver()
    query = """
    MATCH (p1:Person)-[r]-(p2:Person)
    WHERE ID(p1) = $person1_id AND ID(p2) = $person2_id
    DELETE r
    """
    with driver.session() as session:
        result = session.run(query, person1_id=person1_id, person2_id=person2_id)
    return result.consume().counters.relationships_deleted > 0

def update_person(person_id, person_data):
    driver = get_db_driver()
    query = """
    MATCH (p:Person)
    WHERE ID(p) = $person_id
    SET p.firstName = $firstName, p.lastName = $lastName, p.birthDate = $birthDate, p.deathDate = $deathDate, p.gender = $gender
    RETURN p
    """
    with driver.session() as session:
        result = session.run(query, person_id=person_id, **person_data)
    return {"message": "Person updated successfully"}

def get_all_marriages():
    driver = get_db_driver()
    query = """
    MATCH (p1:Person)-[r:MARRIED_TO]->(p2:Person)
    RETURN p1.firstName + ' ' + p1.lastName AS person1,
           p2.firstName + ' ' + p2.lastName AS person2,
           r.marriageDate AS marriageDate
    """
    with driver.session() as session:
        print("Executing query to fetch marriages...")
        result = session.run(query)
        marriages = []
        for record in result:
            marriages.append({
                "person1": record["person1"],
                "person2": record["person2"],
                "marriageDate": record["marriageDate"]
            })
    return {"marriages": marriages}

def get_all_siblings():
    driver = get_db_driver()
    query = """
    MATCH (parent:Person)-[:PARENT_OF]->(sibling1:Person)
    MATCH (parent)-[:PARENT_OF]->(sibling2:Person)
    WHERE sibling1 <> sibling2
    RETURN DISTINCT sibling1.firstName + ' ' + sibling1.lastName AS sibling1,
                    sibling2.firstName + ' ' + sibling2.lastName AS sibling2
    """
    with driver.session() as session:
        result = session.run(query)
        siblings = []
        for record in result:
            siblings.append({
                "sibling1": record["sibling1"],
                "sibling2": record["sibling2"]
            })
    return {"siblings": siblings}
