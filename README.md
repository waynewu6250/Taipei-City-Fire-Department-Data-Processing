# Taipei-City-Fire-Department-Data-Processing
This is the code work fully composed by Ting-Wei Wu to support and accelerate taipei city fire department information analysis

## 1. Excel VBA work for weekly and monthly report analysis
* month_fire_event_depart_time_analysis.txt: Calculate the average departure time for every fire divisions in Taipei City monthly. <br>
* month_service.txt: Analysis of different public service such as snake, bee capturing etc monthly. <br>
* week_fire_event_analysis.txt: Analysis of fire events and phone calls analysis. <br>
* week_fire_post.txt: Analysis of public service associated with fire events weekly. <br>

## 2. day folder: python scraping with selenium:
* Use /<day.ipynb or daily-event-processing.ipynb/> to do online scraping from fire department database every day. Record every event's time, divisions, and event contents. <br>
* Import </utils.py/> for weekday processing; Import </utils.weekend.py.> for weekend processing. <br>

## 3. rescue folder: python scraping with selenium:
* Manage daily event departure time calculation of each divisions for rescue events.

## 4. html_scraping folder: python scraping with selenium:
* Consecutive Checking with availability of url links on Taipei City Fire Department homepage and subpages.
