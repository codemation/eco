# person
async def run(server):

    Person = server.Person
    Office = server.Office

    # get all persons
    @server.api_route('/persons', methods=['GET'])
    async def get_all_persons():
        all_persons = []
        for p in server.company['persons']:
            office = None
            if not server.company['persons'][p].office is None:
                office = server.company['persons'][p].office.name
            all_persons.append(
                {
                    'name': server.company['persons'][p].name, 
                    'age': server.company['persons'][p].age, 
                    'office': office
                }
            )
        return {'persons': all_persons}

    # get person by name
    @server.api_route('/person/{name}', methods=['GET'])
    async def get_person_by_name(name: str):
        if not name in server.company['persons']:
            return "404, Person not found"
        person = server.company['persons'][name]
        return {'name': person.name, 'age': person.age, 'office': person.office}
    
    # update person by name
    @server.api_route('/person/{name}', methods=['POST'])
    async def update_person_by_name(name: str, config: dict):
        if not name in server.company['persons']:
            return "404, Person not found"
        person = server.company['persons'][name]
        for k, v in config.items():
            if not k in ['age', 'name', 'office']:
                return {"message": f"invlaid input {k}"}
        person.update(config)
        return {"message": f"{person} updated"}

    # delete person by name
    @server.api_route('/person/{name}', methods=['DELETE'])
    async def delete_person_by_name(name: str):
        if not name in server.company['persons']:
            return "404, Person not found"
        person = server.company['persons'].pop(name)
        person.delete()
        return {'message': f"{person} removed"}


    # person - name change / birthday
    @server.api_route('/person/{name}/birthday', methods=['POST'])
    async def person_birthday(name: str):
        if not name in server.company['persons']:
            return "404, Person not found"
        server.company['persons'][name].happy_birthday()
        age = server.company['persons'][name].age
        return {"message": f"happy {age} birthday {name}!!"}

    # person - new
    @server.api_route('/person', methods=['POST'])
    async def person_add(person: dict):
        if not ('name' in person and 'age' in person):
            return f"missing name/age for new person {person}"
        name, age = person['name'], person['age']
        office = person['office'] if 'office' in person else None
        if not name in server.company['persons']:
            new_person = Person(name, age, office)
            server.company['persons'][name] = new_person
            return {'message': f"Person {new_person} created"}

    # person - name change / birthday
    @server.api_route('/person/{name}/change_name', methods=['POST'])
    async def person_name_change(name: str, new_name: dict):
        if not name in server.company['persons']:
            return "404, Person not found"
        if not 'name' in new_name:
            return "400, missing input for new_name: 'name': 'new_name'"
        person = server.company['persons'].pop(name)
        
        server.company['persons'][new_name['name']] = person
        person.change_name(new_name['name'])
        return {"messsage": f"{name} renamed to {new_name['name']}"}