![](https://img.shields.io/badge/Licensed%20by-Wayne%20Wu-blue.svg)
![](https://img.shields.io/badge/Language-python-brightgreen.svg)


# Taipei-City-Fire-Department-Data-Processing
This is the code work fully composed by Ting-Wei Wu to support and accelerate taipei city fire department information analysis

## 1. Excel VBA work for weekly and monthly report analysis
* month_fire_event_depart_time_analysis.txt: Calculate the average departure time for every fire divisions in Taipei City monthly. <br>
* month_service.txt: Analysis of different public service such as snake, bee capturing etc monthly. <br>
* week_fire_event_analysis.txt: Analysis of fire events and phone calls analysis. <br>
* week_fire_post.txt: Analysis of public service associated with fire events weekly. <br>

## 2. day folder: python scraping with selenium:
* Use `day.ipynb or daily-event-processing.ipynb` to do online scraping from fire department database every day. Record every event's time, divisions, and event contents. <br>
* Import `utils.py` for weekday processing; Import `utils-weekend.py` for weekend processing. <br>

## 3. week folder: python downloads with selenium and os:
* Automatically download excel files and file manipulation in os for excel vba work.
* Scrape the service event of fire divisions by cell phone call for the satisfaction survey purposes.

## 4. month folder: python scraping with selenium:
* Use `month.ipynb` to record monthly fire rescue events with dispatch, travel and arrival time for tracking and improvements.

## 5. rescue folder: python scraping with selenium:
* Manage daily event departure time calculation of each divisions for rescue events.

## 6. html_scraping folder: python scraping with selenium:
* Consecutive Checking with availability of url links on Taipei City Fire Department homepage and subpages.

## 7. disable folder: python pandas and selenium:
* Automatically input all information of people with disability into the personnel database.

## 8. weather_analysis folder: python pandas
* Data processing to find relations between weather condition and personal refusal to hospital delivery when rescued.

## 9. locate folder: python pandas and selenium
* Automatic validation for vague city address collected in dispatch system by searching on website of Taipei City Department of Civil Affairs.
