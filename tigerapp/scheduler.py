# ----------------------------------------------------------------------
# scheduler.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------

import atexit
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from tigerapp import db, app
from tigerapp.config import SCHEDULER_FREQ, RENEWAL_THRESHOLD
from tigerapp.models import Items
from threading import Thread
import time

# ----------------------------------------------------------------------

scheduler = APScheduler()
# ----------------------------------------------------------------------

def update_db():
    """
    Task 1: check db for newly expired items 
    Task 2: send renewal emails for items approaching expiration
    """
    app = scheduler.app
    with app.app_context():

        # comparison date: set to end of day today in UTC time
        now = datetime.utcnow()
        now = datetime(now.year, now.month, now.day, 23, 59, 59)

        # find newly expired items and update to inactive
        items = Items.query.filter(
            (Items.isActive == True) & (Items.end_date < now)).all()

        for item in items:
            item.isActive = False
            db.session.commit()

        # get items that are now renewable
        threshold_date = now + timedelta(days=RENEWAL_THRESHOLD)
        renewable_items = Items.query.filter((Items.isActive == True) &
                                             (Items.isRenewable == False) &
                                             (Items.end_date < threshold_date)).all()

        # build email: items dictionary to email users
        emails = dict()
        for item in renewable_items:
            item.isRenewable = True

            netid = item.user[0].netid + "@princeton.edu"
            emails[netid] = emails.get(netid, []) + [item.title]
            db.session.commit()
        if emails:
            send_mail(app, emails)

# ----------------------------------------------------------------------

def send_async_email(app, msg, delay):
    """
    Helper function for sending emails with Flask-Mail.
    Delay is so max concurrent processes is not exceeded
    """
    time.sleep(delay)
    mail = Mail(app)
    with app.app_context():
        try:
            mail.send(msg)
            print("sent")
        except Exception as e:
            print(e.message)

def send_mail(app, emails):
    """
    Send renewal notifications to users.
    """
    delay = 0
    for addr, posts in emails.items():
        body_items = ' \n'.join(posts)
        body_text = f"""Hello {addr.split('@')[0]},\n\nThe following post(s) will expire soon:\
            \n\n{body_items}\
            \n\nPlease go to https://tigersearch.tigerapps.org/myposts to renew or resolve your post. \
            \n\nThank you,\
            \nTigerSearch Team"""

        msg = Message(subject="TigerSearch: Post(s) expiring soon",
                      sender=app.config.get("DEFAULT_SENDER"),
                      recipients=[addr],
                      body=body_text)
        delay += 1
        thr = Thread(target=send_async_email, args=[app, msg, delay])
        thr.start()

# ----------------------------------------------------------------------


def scheduler_start():
    """
    Schedule periodic db updates.
    """
    # perform task every _ hours
    scheduler.add_job(timezone="America/New_York", id='update_db',
                      func=update_db, trigger="interval",
                      hours=SCHEDULER_FREQ)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())