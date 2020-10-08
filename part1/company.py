
"""
1- Create a class "Person" in Python, that has 2 attributes (name and age). Also has 2 methods, (apart from the constructors):
   - happyBirthday, that adds one year to the age
   - changeName, changes the name with the new name provided
2 - Create the class "Office", 2 attributes (name and peopleWorking), 2 methods and a constructor:
   - contructor, based on the name, and initialize the peopleWorking as empty
   - startWorkingFor, receiving one object of the class "Person" and add it to the peopleWorking
   - finishedWorkingFor, receiving "Person", remove it from peopleWorking
3- Create an object of the class "Office", named Ecorus
4- Create 2 objects of that class (Eduardo and <your_name>)
5- Make Eduardo and <your_name> start working for Ecorus
6- Make Eduardo finish working from Ecorus
"""

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
        self.name = new_name

class Office:
    def __init__(self, name):
        self.name = name
        self.people_working = {}
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}) {self.people_working}"
    def __str__(self):
        return repr(self)
    def __add_worker(self, person: Person):
        """
        add person to office
        """
        self.people_working[person.name] = person
    def __rem_worker(self, person):
        """
        remove person from office
        """
        del self.people_working[person.name]
        
    def start_working_for(self, person: Person):
        if isinstance(person, Person):
            self.people_working[person.name] = person
    def stop_working_for(self, person: Person):
        if isinstance(person, Person):
            if person.name in self.people_working:
                del self.people_working[person.name]

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