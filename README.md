# Flight booking system

[![CircleCI](https://circleci.com/gh/nebanat/lms_flight_booking.svg?style=svg)](https://circleci.com/gh/nebanat/lms_flight_booking)

## Features
- Create an account with username(optional), email and password
- Login with email and password
- Upload passport photograph
- Create/Edit/Delete flights (for admin user only)
- View available flights
- Reserve flight tickets
- Book flight tickets
- Receive Booked flight ticket info via email
- Receive reminder 24 hours before flying


## Installation Guide

### Development Environment
- Ensure you have RabbitMQ installed and running on your computer
- Ensure you have Postgresql installed and running on your computer
- Clone this repository with `git clone https://github.com/nebanat/lms_flight_booking.git`
- `cd lms_flight_booking`
- Install virtualenv `pip install virtualenv`
- Create virtual env `python3 -m venv`
- Activate virtual env `source venv/bin/activate`
- Install dependencies `pip install -r requirements.txt`
- Start app `python manage.py runserver`
- Navigate to `localhost:8000`
- Start celery `celery -A flight_booking worker -B -l INFO`
- Start celery beat `celery -A flight_booking beat -l INFO`

## Technologies
- Python3/Django: A Python web framework
- Celery: Task/Queue manager
- RabbitMQ: Message broker
- Postgresql: Relational Database Management System 

## API Documentation
[API Documentation](https://documenter.getpostman.com/view/2364904/S1EQSdUK)



