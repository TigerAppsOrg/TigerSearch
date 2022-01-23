# ----------------------------------------------------------------------
# emailtest_db.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------

from datetime import datetime, timedelta
import random
from tigerapp import db
from tigerapp.models import Users, Items, Tags

# ----------------------------------------------------------------------

db.drop_all()
db.create_all()
print("Step 1: Dropped and recreated tables.")

# ----------------------------------------------------------------------

users = []

netids = ['mandyl', 'mmir', 'anaghar', 'elkishky', 'tigersearch']
for user in netids:
    new_user = Users(netid=user)
    users.append(new_user)
    if user == 'tigersearch':
        new_user.isAdmin = True
    db.session.add(new_user)
db.session.commit()
print("Step 2: Added users.")

# ----------------------------------------------------------------------


def dummy_enddate(created_date):
    return created_date.date() + timedelta(days=30)


create1 = datetime(2021, 12, 29, 11, 10)
end1 = dummy_enddate(create1)
create2 = datetime(2021, 10, 15, 11, 12)
end2 = dummy_enddate(create2)
create3 = datetime(2021, 10, 9, 11, 12)
end3 = dummy_enddate(create3)
create4 = datetime(2020, 10, 10, 11, 12)
end4 = dummy_enddate(create4)
create5 = datetime(2021, 7, 10, 11, 12)
end5 = dummy_enddate(create5)


# dummy items
item1 = Items(isActive=True, title="Airpods", description="airpods 3",
              location="Butler", isFoundItem=True, created_date=create1, end_date=end1)
item2 = Items(isActive=True, title="Water Bottle", description="hydroflask",
              location="Frist", isFoundItem=True, created_date=create2, end_date=end2)
item3 = Items(isActive=True, title="Jacket", description="warm",
              location="Whitman", isFoundItem=False, created_date=create3, end_date=end3)
item4 = Items(isActive=True, title="Umbrella", description="orange",
              location="Bloomberg", isFoundItem=True, created_date=create2, end_date=end2)
item5 = Items(isActive=False, title="Jacket3", description="warm",
              location="Mathey", isFoundItem=True, created_date=create4, end_date=end4)
item6 = Items(isActive=False, title="Bike", description="red",
              location="Nassau", isFoundItem=True, created_date=create5, end_date=end5)
item7 = Items(isActive=True, title="Shoes",
              description="i found a pair of shoes", location="Frist", isFoundItem=True)
item8 = Items(isActive=True, title="Pillow",
              description="found this in the hallway", location="Lewis", isFoundItem=True)
item9 = Items(isActive=True, title="Scooter", description="fast",
              location="Charter", isFoundItem=True)

items = [item1, item2, item3, item4, item5, item6, item7, item8, item9]

longdescription = "I found this item. I found this item. I found this item. \
    I found this item. I found this item. I found this item. I found this item. \
        I found this item. I found this item. I found this item. I found this item."

longdescription2 = "The Nike Air Force 1 Shadow puts a playful twist on a classic \
    b-ball design. Using a layered approach, doubling the branding and exaggerating the midsole, \
        it highlights AF-1 DNA with a bold, new look."

longdescription3 = "We the People of the United States, in Order to form a more perfect Union, \
        establish Justice, insure domestic Tranquility, provide for the common defense,"

longdescription4 = "Tune every heart and every voice, Bid every care withdraw; Let all with one accord rejoice, \
    In praise of Old Nassau. In praise of Old Nassau we sing, Hurrah! Hurrah! Hurrah! Our hearts will give, \
    while we shall live, Three cheers for Old Nassau."

titles = ['Airpods', 'Phone', 'Backpack', 'Water Bottle', 'Bike', 'Electric Scooter',
          'Umbrella', 'iPad', 'Notebook', 'Princeton Jacket', 'Socks', 'Nike Shoes', 'adidas sneakers', 'tennis racket'
          'Basketball', 'Apple Pencil', 'Charger for Mac', 'Canada goose', 'portable charger', 'box of cookies', 'backpack with 2 books',
          'black and orange hat', 'patagonia winter jacket', 'iPad air with black case', 'airpod pros',
          'Airpods', 'Phone', 'Backpack', 'Water Bottle', 'Bike', 'Electric Scooter',
          'Umbrella', 'iPad', 'Notebook', 'Princeton Jacket', 'Socks', 'Nike Shoes', 'adidas sneakers', 'tennis racket'
          'Basketball', 'Apple Pencil', 'Charger for Mac', 'Canada goose', 'portable charger', 'box of cookies', 'backpack with 2 books',
          'black and orange hat', 'patagonia winter jacket', 'iPad air with black case', 'airpod pros']

descriptions = ['this is a decription of the item', 'Contact me about this item. It is red with white stripes', 'brand new',
                'green and very old', 'has a stain', 'white', 'small', longdescription, longdescription2, longdescription3, longdescription4]
locations = ['Whitman dining hall', 'out side of Bloomberg arch', 'firestone reading room', 'wawa near cash register',
             'Nassau', 'Mathey', 'backyard of charter', 'Colonial', 'Quad', 'Lewis library, 3rd floor table', 'Frist late meal area']
images = ['https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707090/gx9xvvsrgjasaolkxfef.jpg',
          'https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707078/imai9irv4oalokstnpgn.jpg',
          'https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707062/lajfzq3dgnyhh4zgjuaz.jpg']

# assigning descriptions, locations, images, and types to items
tf = [True, False]
for t in titles:
    is_found = random.choice(tf)
    is_active = True
    d = random.choice(descriptions)
    l = random.choice(locations)
    p = random.choice(images)
    new_item = Items(isActive=is_active, title=t, description=d,
                     location=l, isFoundItem=is_found, picture=p, created_date=create1, end_date=end1)
    items.append(new_item)

for item in items:
    db.session.add(item)

db.session.commit()
print("Step 3: Added items.")

# ----------------------------------------------------------------------

# tags
location = ["Butler", "Forbes", "Rockefeller", "Mathey", "First", "Whitman", "Upperclass Housing", "Graduate College",
            "Academic Buildings", "Athletic Facilities", "Libraries", "Eating Clubs"]

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
print(f"Step 4: Added {len(tags)} tags.")

# ----------------------------------------------------------------------

# adding tags to items
for i, item in enumerate(items):
    user = random.choice(users)
    user.posts.append(item)
    item.categories.extend(random.sample(tags, 3))

db.session.commit()
print("Step 5: Added tags to items.")
print("#----------------------------------------------------------------------")
print("Script complete.")
