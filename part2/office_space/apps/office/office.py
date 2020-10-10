# office
async def run(server):
    from fastapi import Request
    from pydantic import BaseModel

    class Office:
        def __init__(self, name: str):
            self.name = name
            self.people_working = {}
            self.db = server.data['office']
            self.db.loop.create_task(
                self.create_office_in_db()
            )
        def __contains__(self, person):
            return person.name in self.people_working
        def __repr__(self):
            return f"{self.__class__.__name__}({self.name}) {self.people_working}"
        def __str__(self):
            return repr(self)
        def __add_worker(self, person):
            """
            add person to office
            """
            self.people_working[person.name] = person
            person.office = self
            self.db.loop.create_task(
                self.db.tables['persons'].update(
                    office=self.name,
                    where={'name': person.name}
                )
            )

        def __rem_worker(self, person):
            """
            remove person from office
            """
            if person.name in self.people_working:
                person.office = None
                del self.people_working[person.name]
            self.db.loop.create_task(
                self.db.tables['persons'].update(
                    office=None,
                    where={'name': person.name}
                )
            )
        async def create_office_in_db(self):
            if not self.db:
                return  
            if await self.db.tables['offices'][self.name] in [[], None]:
                await self.db.tables['offices'].insert(
                    name=self.name
                )
        def start_working_for(self, person):
            if isinstance(person, Person):
                self.__add_worker(person)
        def stop_working_for(self, person):
            if isinstance(person, Person):
                self.__rem_worker(person) 
    server.Office = Office

    class Person:
        def __init__(self, name: str, age: int, office: Office = None):
            
            self.name = name
            self.age = age
            self.office = office
            self.db = server.data['office']
            self.db.loop.create_task(
                self.create_person_in_db()
            )

        async def create_person_in_db(self):
            if not self.db:
                return  
            if await self.db.tables['persons'][self.name] == None:
                await self.db.tables['persons'].insert(
                    name=self.name,
                    age=self.age,
                    office=self.office.name if not self.office == None else None
                )
        async def update_person_in_db(self, **kw):
            if not self.db:
                return
            if not await self.db.tables['persons'][self.name] == []:
                await self.db.tables['persons'].update(
                    **kw,
                    where={'name': self.name}
                )

        def __repr__(self):
            return f"{self.__class__.__name__}({self.name}, {self.age})"
        def __str__(self):
            return repr(self)

        def delete(self):
            self.db.loop.create_task(
                self.db.tables['persons'].delete(
                    where={'name': self.name}
                )
            )
        def update(self, data: dict):
            for k, v in data.items():
                if k == 'age':
                    self.__set_age(v)
                if k == 'name':
                    self.change_name(v)
            
        def __set_age(self, age):
            self.age = age
            self.db.loop.create_task(
                self.update_person_in_db(
                        age=self.age
                    )
            )
        def happy_birthday(self):
            return self.__set_age(self.age + 1)

        def change_name(self, new_name):
            old_name = self.name[:]
            if 'office' in self.__dict__:
                self.office.people_working.pop(old_name)
                self.office.people_working[new_name] = self
            
            
            self.db.loop.create_task(
                self.db.tables['persons'].update(
                    name=new_name,
                    where={'name': old_name}
                )
            )
            self.name = new_name
    server.Person = Person


    # Load all existing persons / offices

    server.company = {'persons': {}, 'offices': {}}
    all_persons = await server.data['office'].tables['persons'].select(
        '*'
    )
    for person in all_persons:
        office = person['office']
        if not office == None:
            if not office in server.company:
                server.company['offices'][office] = Office(
                    office
                )
        name, age = person['name'], person['age']
        a_person = Person(name, age, office=office)
        server.company['persons'][name] = a_person
        if not office == None:
            server.company['offices'][office].start_working_for(a_person)
    all_offices = await server.data['office'].tables['offices'].select(
        '*'
    )

    # load existing offices - with no employees
    for office in all_offices:
        if not office['name'] in server.company['offices']:
            existing_office = Office(office['name'])
            server.company['offices'][office['name']] = existing_office
        

    # get all offices
    @server.api_route('/offices', methods=['GET'])
    async def get_all_offices():
        office_list = []
        for office_name in server.company['offices']:
            office = server.company['offices'][office_name]
            print(office)
            people_working_list = []
            for emp in office.people_working:
                people_working_list.append(
                    {
                        'name': office.people_working[emp].name, 
                        'age': office.people_working[emp].age
                    }
                )
            office_list.append({
                'name': office_name, 
                'people_working': people_working_list
            })
        return {"offices": office_list}
    
    class OfficeObj(BaseModel):
        name: str

    # office - new
    @server.api_route('/office', methods=['POST'])
    async def office_add(office: OfficeObj):
        office = dict(office)
        name = office['name']
        if not name in server.company['offices']:
            new_office = Office(name)
            server.company['offices'][name] = new_office
            return {'message': f"Office {new_office} created"}

    # get office
    @server.api_route('/office/{name}', methods=['GET'])
    async def get_office_by_name(name: str):
        if not name in server.company['offices']:
            return f"404, {name} not found" 
        office = server.company['offices'][name]
        people_working_list = [
            {
                'name': office.people_working[emp].name, 
                'age': office.people_working[emp].age
            } for emp in office.people_working
        ]
        return {
            'name': office.name, 
            'people_working': people_working_list
        }

    # office remove / add worker 
    @server.api_route('/office/{office_name}/worker/{person_name}', methods=['POST'])
    async def add_person_to_office(office_name: str, person_name: str):
        if not office_name in server.company['offices']:
            return f"404, {office_name} not found"
        if not person_name in server.company['persons']:
            return f"404, {person_name} not found" 
        person = server.company['persons'][person_name]
        server.company['offices'][office_name].start_working_for(person)
        return {"message": f"{person_name} started working for {office_name}"}
    
    # office remove person from working   
    @server.api_route('/office/{office_name}/worker/{person_name}', methods=['DELETE'])
    async def delete_person_from_office(office_name: str, person_name: str):
        if not office_name in server.company['offices']:
            return f"404, {office_name} not found"
        if not person_name in server.company['persons']:
            return f"404, {person_name} not found" 
        person = server.company['persons'][person_name]
        server.company['offices'][office_name].stop_working_for(person)
        return {"message": f"{person_name} stopped working for {office_name}"}



