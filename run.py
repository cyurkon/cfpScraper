import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from scraper.models import Companies, Session
from scraper.scraper import scrape


client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))


if __name__ == "__main__":
    companies = scrape()
    timeslots = {}
    session = Session()
    for company, num_slots in companies.items():
        if prev := session.query(Companies).filter(Companies.name == company).first():
            if num_slots == prev.num_slots:
                continue
            elif num_slots > prev.num_slots:
                timeslots[company] = num_slots - prev.num_slots
            prev.num_slots = num_slots
            session.add(prev)
        else:
            session.add(Companies(name=company, num_slots=num_slots))
            timeslots[company] = num_slots
        session.commit()
    session.close()
    message = "\n".join([f"{k} has {v} new slots." for k, v in timeslots.items()])
    try:
        client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE"),
            to=os.getenv("PERSONAL_PHONE")
        )
    except TwilioRestException as e:
        print(e.msg)

