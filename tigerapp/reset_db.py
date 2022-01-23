# ----------------------------------------------------------------------
# reset_db.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# Run this script to reset the database
# ----------------------------------------------------------------------

from tigerapp import db
from tigerapp.models import Users, Items, Tags

db.drop_all()
db.create_all()
print("Step 1: Dropped and recreated tables.")


user = 'tigersearch'
new_user = Users(netid=user)
new_user.isAdmin = True
db.session.add(new_user)
db.session.commit()

print("Step 2: Added admin user.")

location = ['Academic Buildings', 'Athletic Facilities', 'Butler', 'Eating Clubs', 'First',
            'Forbes', 'Graduate College', 'Libraries', 'Mathey',
            'Rockefeller', 'Upperclass Housing', 'Whitman']

type = ["Accessories", "Books", "Clothing",
        "Food", "Furniture", "Tech", "Transportation"]

in_out = ["Indoors", "Outdoors"]
tags = []

for tag in location:
    new_tag = Tags(tag_name=tag, category="Location")
    tags.append(new_tag)
    db.session.add(new_tag)

for tag in type:
    new_tag = Tags(tag_name=tag, category="Type")
    tags.append(new_tag)
    db.session.add(new_tag)

for tag in in_out:
    new_tag = Tags(tag_name=tag, category="Indoors-Outdoors")
    tags.append(new_tag)
    db.session.add(new_tag)

db.session.commit()

print(f"Step 3: Added {len(tags)} tags.")
