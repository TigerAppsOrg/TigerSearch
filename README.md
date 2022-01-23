# TigerSearch
## Developed by Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
TigerSearch is a centralized lost and found platform for Princeton students and staff to connect missing items with their owners. The web app allows Princeton University community members to create posts about lost or found items around campus, search and filter through feeds of posts to look for matching items to the one they lost or found, communicate with posters, and ultimately help people find their stuff. The web app also features an admin mode that allows administrators of the app to track basic usage statistics, hide inappropriate posts, and ban users. The application was developed as the final project for COS333 in Fall 2021.

## Assigning Admin Privileges:
### Only the user 'tigersearch' has the ability to assign or revoke Admin Privileges. To do so:
1. Login to TigerSearch using the 'tigersearch' (service account) login credentials
2. Click 'Turn On Admin Mode'
3. Go to 'Manage Users' Section and modify admin privileges for intended netids (the netid needs to be registered- i.e. logged in to TigerSearch once already)
4. Once assigned admin, the admin user will now see 'Turn On Admin Mode' button when they log in using their account

## Resetting database:
### Warning: This will remove all users and posts. The database may need to be reset if the database space limit has been exceeded. After clearing the database, the TigerSearch db needs to have the tags reinserted into the tables. The script reset_db.py resets the database and creates the tags. To reset the db on Heroku:
1. `heroku run flask shell -a tigersearch` <br />
2. `from tigerapp import reset_db` <br />

## Local development:

1. Clone the repository
2. Create and activate Python virtual environment using `python3 -m venv environment_name`
3. Install all the requirements using `pip install -r requirements.txt`
4. Create a .env file containing the following keys: CLOUD_NAME, API_KEY, API_SECRET, SENDGRID_API_KEY, and DEFAULT_SENDER.
5. Database setup:
    ### Step 1:
    - Setup postgres and add username and password to the config file <br />
    OR <br />
    - Change the Database URI link to `sqlite:///site.db`
    ### Step 2:
    - Run the database script using: <br />
    1. `flask shell` <br />
    2. `from tigerapp import utesting_db` <br />
    3. `quit()` or `ctrl + D` 
6. Make any changes you want
7. Run the app using `flask run`
