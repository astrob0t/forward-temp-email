import os
import random
import string
import json

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))

first_names = json.loads(open('fname.json').read())
last_names = json.loads(open('lname.json').read())

name_extra = ''.join(random.choice(string.digits))
names = random.choice(first_names) + random.choice(last_names) + name_extra

print(names.lower())
