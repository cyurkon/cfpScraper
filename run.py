import json

from sqlalchemy import desc

from scraper.models import Session, Timeslots
from scraper.scraper import scrape
from scraper.utils import diff, format_message, send_text


if __name__ == "__main__":
    curr_timeslots = scrape()
    print(curr_timeslots)
    session = Session()
    if record := session.query(Timeslots).order_by(desc(Timeslots.id)).first():
        prev_timeslots = json.loads(record.timeslots)
        new_timeslots = diff(prev_timeslots, curr_timeslots)
        message = format_message(new_timeslots)
    else:
        message = format_message(curr_timeslots)
    send_text(message)
    session.add(Timeslots(timeslots=json.dumps(curr_timeslots)))
    session.commit()
