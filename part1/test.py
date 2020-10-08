import unittest
from company import Person, Office

class CompanyTest(unittest.TestCase):
    def test_00_smoke(self):
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
    def test_01_basic_functionality(self):
        # birthday test
        age = 29
        josh = Person('josh', 29)
        josh.happy_birthday()
        assert josh.age == age+1, f'expected age of {josh} to be {age+1}, but is {josh.age}'

        # name change
        new_name = 'definity not josh'
        josh.change_name(new_name) 
        assert josh.name == new_name, f'expected name of {josh} to be {new_name}, but is {josh.name}'

        eco = Office('Ecorus')

        eco.start_working_for(
            Person('eduardo', 29)
        )
        eco.start_working_for(
            Person('bob', 29)
        )
        eco.start_working_for(
            Person('joe', 29)
        )
        eco.start_working_for(josh)

        assert len(eco.people_working) == 4, f"expected number of people working to be {4}, found {len(eco.people_working)}"

        # rename within company 

        josh.change_name('josh') 

        assert josh.name in eco.people_working, f"expected Person with name {josh.name} in {eco}"
