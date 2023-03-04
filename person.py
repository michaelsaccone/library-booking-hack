import requests
from random import randint


class Person:
    def __init__(self, name: str, surname: str, email=None, phone=None):
        self.name = name
        self.surname = surname
        self.email = email if email is not None else Person.generate_email(name, surname
                                                                           .replace(" ", "")
                                                                           .replace("’", ""))
        self.phone = phone if phone is not None else Person.generate_phone()

    def __str__(self):
        return (" Name:  " + self.name + "\n"
                " Surname:  " + self.surname + "\n"
                " Email:  " + self.email + "\n"
                " Phone:  " + self.phone)

    @staticmethod
    def generate_email(name, surname):
        patternChoser = randint(1, 3)

        if patternChoser == 1:
            return name + '.' + surname + str(randint(89, 2000)) + '@' + 'gmail.com'
        elif patternChoser == 2:
            return name[0] + surname + str(randint(92, 99)) + '@gmail.com'
        elif patternChoser == 3:
            return surname[0].lower() + name[0].lower() + str(randint(89, 2000)) + surname + '@outlook.it'

    @staticmethod
    def generate_phone():
        num = '+393'
        for i in range(1, 9):
            num = num + str(randint(0, 9))
        return num

    '''
        The backend server was badly implemented.
        If a request is for a single person, it uses one pattern (single object)
        otherwise returns array
    '''

    @staticmethod
    def generate_random(n):
        persons = []
        gen1 = randint(1, n)
        gen2 = n - gen1
        print("males : " + str(gen1))
        print("females : " + str(n - gen1))

        males = requests.get('https://story-shack-cdn-v2.glitch.me/generators/italian-name-generator/male',
                             params={'count': str(gen1)} if gen1 > 1 else {})
        malesNames = males.json()['data']
        if gen1 > 1:
            for male in malesNames:
                persons.append(Person(male['name'], male['lastName']))
        else:
            persons.append(Person(malesNames['name'], malesNames['lastName']))

        if gen2 > 0:
            females = requests.get('https://story-shack-cdn-v2.glitch.me/generators/italian-name-generator/female',
                                   params={'count': str(gen2)} if gen2 > 1 else {})
            femalesNames = females.json()['data']
            if gen2 > 1:
                for female in femalesNames:
                    persons.append(Person(female['name'], female['lastName']))
            else:
                persons.append(Person(femalesNames['name'], femalesNames['lastName']))

        return persons
