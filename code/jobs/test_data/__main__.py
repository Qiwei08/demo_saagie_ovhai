import random
from faker import Faker


# create a function to generate data
def generate_data():
    # create a list of 1000 random numbers
    data = [random.randint(0, 1000) for i in range(1000)]
    # return the data
    return data

# create a function to generate english names
def generate_names():
    # create a list of 1000 random names
    names = [fake.name() for i in range(1000)]
    # return the names
    return names

print(generate_data())