def get_full_name(first_name: str, last_name: str):
    full_name = first_name.upper() + " " + last_name.upper()
    
    return full_name



print(get_full_name("omar","Amgad"))

def prosess_items(items: list[str]):

    for item in items:
        print(item)
        print(type(item))

prosess_items(['omar','amgad', 10, 20])



def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

say_hi("omar")
say_hi()

class Person:

    def __init__(self, name:str):
        self.name = name
    def get_person_name(name):
        return f"hello {name}"
# def get_person_name(one_person: Person):
        # return one_person.name

print(Person.get_person_name("omar"))

# get_person_name()

