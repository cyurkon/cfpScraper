# cfpScraper
Texts you when new timeslots are available for the Fall 2020 GT Computing Career Fair (by crawling [this Career Fair Plus page](https://app.careerfairplus.com/gt_ga/fair/2660/)). 

## Setup
1. Download [Google Chrome](https://www.google.com/chrome/) and [ChromeDriver](https://chromedriver.chromium.org/downloads). Their version numbers must match.
2. Sign up for [Twilio](https://www.twilio.com), create a new project, and get a phone number. On the console page, note the Account SID and Auth Token.
3. Fork this repository and create a local clone. Within your local repository run `cp .env.example .env` to create a copy of the expected environment. Update `ACCOUNT_SID`, `AUTH_TOKEN`, and `TWILIO_PHONE` with the values noted in step 2, `PERSONAL_PHONE` with your cell number, and `GOOGLE_CHROME_BIN` and `CHROMEDRIVER_PATH` with the paths to your Google Chrome binary and ChromeDriver executable.
4. Make sure python 3.8 and pip are installed on your system.
5. Install the required libraries: `pip3 install -r requirements.txt`.

## Running
Run this from the command line: `python3 run.py`. If you want to schedule this to run at certain times, use [cron](https://en.wikipedia.org/wiki/Cron) or a cloud platform like [Heroku](https://www.heroku.com).

## Documentation
[Selenium with Python](https://selenium-python.readthedocs.io)