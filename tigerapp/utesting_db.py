# ----------------------------------------------------------------------
# utesting_db.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------

from tigerapp import db
from tigerapp.models import Users, Items, Tags
from datetime import datetime, timedelta
import random

# comment out so we don't accidentally rerun
# db.drop_all()
# db.create_all()
print("Step 1: Dropped and recreated tables.")


users = []

netids = ['mandyl', 'mmir', 'anaghar', 'elkishky', 'tigersearch']
for user in netids:
    new_user = Users(netid=user)
    users.append(new_user)
    db.session.add(new_user)
db.session.commit()

print("Step 2: Added users.")

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

print(f"Step 4: Added {len(tags)} tags.")


# 0: 'Butler'
# 1: 'Forbes'
# 2: 'Rockefeller'
# 3: 'Mathey'
# 4: 'First'
# 5: 'Whitman'
# 6: 'Graduate College'
# 7: 'Academic Buildings'
# 8: 'Libraries'
# 9: 'Eating Clubs'
# 10: 'Indoors'
# 11: 'Outdoors'
# 12: 'Accessories'
# 13: 'Books'
# 14: 'Clothing'
# 15: 'Food'
# 16: 'Furniture'
# 17: 'Tech'
# 18: 'Transportation'

longdescription = "This was found on the Whitman steps near dining hall. \
        Specifically, the third step from the top, on the left side. Please contact me if this is your item so that \
            we can arrange a time and place for pick up."

longdescription2 = "I think I dropped it near firestone and chancellor green hall, but I am not 100 percent sure. \
    it's really important to me, i use this item everyday. please contact me asap if you found it. thank you. "

# dummy item parralel lists
titles = ['my Phone', 'Backpack', 'Water Bottle', 'Bike', 'Electric Scooter',
          'Umbrella', 'apple new iphone', 'Notebook', 'Princeton Jacket', 'Socks',
          'Nike basketball shoes', 'size 9 adidas sneakers', 'tennis racket',
          'Basketball', 'Apple Pencil', 'Charger for Mac', 'Canada goose',
          'portable charger', 'box of cookies', 'backpack with 2 books',
          'black and orange hat', 'patagonia winter jacket', 'iPad air with black case']

images = ['https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707090/gx9xvvsrgjasaolkxfef.jpg', '', '', '', '',
          '', 'https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707090/gx9xvvsrgjasaolkxfef.jpg', '', '', '',
          'https://res.cloudinary.com/drcv8tnqh/image/upload/v1635707078/imai9irv4oalokstnpgn.jpg', '', '',
          '', '', '', '', '', '', '', '', '', '']

descriptions = ['is expensive', 'Contact me about this item. It is red with white stripes', 'brand new',
                'designer brand, is expensive', 'has a stain', 'white, barely used', 'small',
                'this is a decription of the item', 'Contact me about this item. It is red with white stripes', 'brand new',
                'green and very old', 'has a stain', 'white, barely used', 'small',
                'Contact me about this item. It is red with white stripes', 'brand new',
                'green and very old', 'has a stain', 'white, barely used', 'small',
                'has a stain', 'white, barely used', 'small',
                ]

dummy_tags = [[5, 10, 17], [8, 4, 10], [11, 18], [2, 11], [5, 10], [1, 10], [2, 10], [1, 10, 17], [8, 4, 10], [11, 18], [2, 11], [5, 10], [1, 10], [2, 10],
              [1, 10, 17], [1, 10, 17], [8, 4, 10], [8, 4, 10], [11, 18], [2, 11], [5, 10], [1, 10], [2, 10]]

locations = ['Whitman dining hall', 'outside of Bloomberg arch', 'firestone reading room',
             'wawa near cash register', 'Nassau', 'Mathey', 'backyard of charter', 'Colonial',
             'Quad', 'Lewis library, 3rd floor table', 'Frist late meal area', 'sculpture near firestone',
             'outside of Bloomberg arch', 'firestone reading room',
             'wawa near cash register', 'Nassau', 'Mathey', 'backyard of charter', 'Colonial',
             'Quad', 'Lewis library, 3rd floor table', 'Frist late meal area', 'sculpture near firestone']


airpods_lost = ['headphones', 'new airpods 3', 'airppods pro',
                'apple earbuds', 'jbl earphones', 'empty case for airpods']
airpods_decript_lost = ['headphones i just bought yesterday at the u store', 'help me find them!!', 'i lost these while walking :(',
                        'pls contact me if u find them', 'very expensive', 'i lost my airpods case!!!!']
airpods_loc_lost = ['Mathey', 'backyard of charter', 'Colonial',
                    'Quad', 'Lewis library, 1st floor table', 'Frist late meal area']

airpods_lost_tags = [[3, 10, 17, 12], [9, 11, 17],
                     [17], [9, 17], [10, 8, 7, 17, 12], [10, 17]]
airpods_pics_lost = ['', '', 'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382709/x9qlzhf95xacaixatlpl.jpg',
                     '', '', 'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382499/uoncw3a98kndg9oetxy8.jpg']

# airpods found feed
airpods_found = ['found Airpods', 'Airpod earphones', 'Airpods Pro',
                 'Apple airpods', 'Airpods inside case', 'one left airpod',
                 'airpods and case', 'airpods pro empty case', 'airpods']

airpods_descript_found = ['small white, no case', 'found this', 'white',
                          'just the left one', 'i found a pair of airpods with a white case', 'it seems to be an airpod 3',
                          'white airpod pros inside case, seems new', 'just a white case, has some stains, no airpods inside', 'regular airpods pro']

airpods_loc_found = ['Whitman', 'firestone library 2rd floor', 'Whitman dining hall',
                     'poe field near bloomberg', 'butler basement', 'near wucox salad bar',
                     'u store by hoodies', 'fine hall room 333', 'dillon basketball court']

airpods_pics_found = ['https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382709/x9qlzhf95xacaixatlpl.jpg',
                      '', 'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382516/vyogoymozeyvgzpqjqpr.jpg',
                      '', 'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382724/ujemriy509vxnvgqip5y.jpg', '',
                      'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382516/vyogoymozeyvgzpqjqpr.jpg', '',
                      'https://res.cloudinary.com/drcv8tnqh/image/upload/v1636382709/x9qlzhf95xacaixatlpl.jpg']

airpods_found_tags = [[10, 5, 17], [10, 17, 8, 7], [10, 5, 17],
                      [11, 0, 17], [10, 0, 17], [0, 4, 10, 17],
                      [10, 17], [7, 10, 17], [10, 17]]

items = []


# lost airpods
for i, t in enumerate(airpods_lost):
    d = airpods_decript_lost[i]
    l = airpods_loc_lost[i]
    p = airpods_pics_lost[i]
    tag_list = airpods_lost_tags[i]

    if p:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=False, picture=p)
    else:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=False)  # default pic

    for t in tag_list:
        new_item.categories.append(tags[t])

    items.append(new_item)
print(len(items))
# found airpods posts
for i, t in enumerate(airpods_found):
    d = airpods_descript_found[i]
    l = airpods_loc_found[i]
    p = airpods_pics_found[i]
    tag_list = airpods_found_tags[i]

    if p:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=True, picture=p)
    else:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=True)  # default pic

    for t in tag_list:
        new_item.categories.append(tags[t])

    items.append(new_item)

print(len(items))

# regular dummy items
for i, t in enumerate(titles):
    # first 15 are found posts
    isFound = (i < 15)
    d = descriptions[i]
    l = locations[i]
    p = images[i]
    tag_list = dummy_tags[i]

    if p:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=isFound, picture=p)
    else:
        new_item = Items(title=t, description=d, location=l,
                         isFoundItem=isFound)  # default pic

    for t in tag_list:
        new_item.categories.append(tags[t])

    items.append(new_item)
print(len(items))

# manually set some created and end dates:
# indices: 0-6:lost airpods, 7-14:found airpods, 15-29?:regular found,30-37: regular lost,


def dummy_enddate(created_date):
    return created_date.date() + timedelta(days=30)


create1 = datetime(2021, 10, 20, 11, 10)
end1 = dummy_enddate(create1)
create2 = datetime(2021, 10, 31, 11, 10)
end2 = dummy_enddate(create2)
create3 = datetime(2021, 11, 4, 11, 10)
end3 = dummy_enddate(create3)

items[2].created_date = create1
items[2].end_date = end1
items[4].created_date = create2
items[4].end_date = end2
items[8].created_date = create3
items[8].end_date = end3
items[14].created_date = create2
items[14].end_date = end2
items[18].created_date = create3
items[18].end_date = end3
items[22].created_date = create1
items[22].end_date = end1
items[25].created_date = create1
items[25].end_date = end1
items[30].created_date = create1
items[30].end_date = end1
items[32].created_date = create3
items[32].end_date = end3
items[37].created_date = create2
items[37].end_date = end2


print("Step 3: Added items.")


for item in items:
    user = random.choice(users)
    user.posts.append(item)

db.session.commit()
