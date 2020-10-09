
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.age})"
    def __str__(self):
        return repr(self)
    def happy_birthday(self):
        self.age+=1
    def change_name(self, new_name):
        old_name = self.name[:]
        if 'office' in self.__dict__:
            self.office.people_working.pop(old_name)
            self.office.people_working[new_name] = self
        self.name = new_name

class Office:
    def __init__(self, name):
        self.name = name
        self.people_working = {}
    def __contains__(self, person: Person):
        return person.name in self.people_working
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}) {self.people_working}"
    def __str__(self):
        return repr(self)
    def __add_worker(self, person: Person):
        """
        add person to office
        """
        self.people_working[person.name] = person
        person.office = self

    def __rem_worker(self, person):
        """
        remove person from office
        """
        if person.name in self.people_working:
            person.office = None
            del self.people_working[person.name]
        
    def start_working_for(self, person: Person):
        if isinstance(person, Person):
            self.__add_worker(person)
    def stop_working_for(self, person: Person):
        if isinstance(person, Person):
            self.__rem_worker(person)

if __name__ == '__main__':
    eco = Office('Ecorus')

    josh = Person('josh', 29)
    eduardo = Person('ed', 29)

    eco.start_working_for(eduardo)
    print(eco)
    eco.start_working_for(josh)
    print(eco)
    eco.stop_working_for(eduardo)
    print(eco)
    josh.change_name('definity not josh')
    print(eco)