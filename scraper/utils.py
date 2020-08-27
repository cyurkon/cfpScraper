import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))


def diff(prev_timeslots, curr_timeslots):
    new_timeslots = {}
    for company, recruiters in curr_timeslots.items():
        if company not in prev_timeslots:
            new_timeslots[company] = recruiters
            continue
        new_recruiters = {}
        prev_recruiters = prev_timeslots[company]
        for recruiter, timeslots in recruiters.items():
            if recruiter not in prev_recruiters:
                new_recruiters[recruiter] = timeslots
            elif prev_recruiters[recruiter] < timeslots:
                new_recruiters[recruiter] = timeslots - prev_recruiters[recruiter]
        if new_recruiters:
            new_timeslots[company] = new_recruiters
    print(new_timeslots)
    return new_timeslots


def format_message(time_slots):
    message = ""
    for company, recruiters in time_slots.items():
        message += f"{company}\n"
        for recruiter in recruiters:
            message += f"{recruiter} has {recruiters[recruiter]} timeslots.\n"
        message += "\n\n"
    return message


def send_text(message):
    try:
        message = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE"),
            to=os.getenv("PERSONAL_PHONE")
        )
        print(message)
    except TwilioRestException as e:
        print(e.msg)
