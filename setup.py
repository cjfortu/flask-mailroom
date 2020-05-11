import random
from passlib.hash import pbkdf2_sha256
from model import db, Donor, Donation

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation])

db.create_tables([Donor, Donation])

alice = Donor(name="Alice", password=pbkdf2_sha256.hash("alice1"))
alice.save()

bob = Donor(name="Bob", password=pbkdf2_sha256.hash("bob2"))
bob.save()

charlie = Donor(name="Charlie", password=pbkdf2_sha256.hash("charlie3"))
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=round(random.uniform(100, 10000), 2)).save()
