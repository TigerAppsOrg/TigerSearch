# ----------------------------------------------------------------------
# stats.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------

from tigerapp import db  # , model
from tigerapp.models import Tags, Items, Users
from datetime import datetime

print("\nGenerating Simple Stats\n")


# tags = Tags.query.all()
# print(f"Total tags: {len(tags)}")

users = Users.query.all()
print(f"Total users: {len(users)}")

# TODO: users with at least one post
items = Items.query.all()
users = set()
for item in items:
    users.add(item.user[0].netid)
print(f"Users with >= 1 post: {len(users)}")


items = Items.query.all()
print(f"Total posts: {len(items)}")
items = Items.query.filter(Items.isFoundItem == True).all()
print(f"Total found posts: {len(items)}")
items = Items.query.filter(Items.isFoundItem == False).all()
print(f"Total lost posts: {len(items)}")

items = Items.query.filter(Items.isActive == True).all()
print(f"Total active posts: {len(items)}")
items = Items.query.filter(Items.isActive == False).all()
print(f"Total resolved posts: {len(items)}")


now = datetime.utcnow()
start = datetime(now.year, now.month, now.day, 0, 0, 0)
now = datetime(now.year, now.month, now.day, 23, 59, 59)

# find newly expired items and update to inactive
items = Items.query.filter((Items.created_date < now)
                           & (Items.created_date > start)).all()
print(f"New posts today: {len(items)}")
