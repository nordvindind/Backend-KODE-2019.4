# Backend-KODE-2019.4

Solutions for 3 problems to get training

## 1. Algorithms.

Please, make sure to use Python 3. 
To launch code:
```
Python3 Algorithms/phrase_search.py
```

## 2. Project


### Prerequisites and installation

For 2nd problem we will need Python 3 and venv.
Navigate to folder KODE-2019.4/Project

```
python3 -m venv KODEenv
```

To activate venv

```
source KODEenv/bin/activate
```

To install all prerequisites 

```
pip install -r requirements.txt
```

Be aware, certain variables should be set in .env file for security reasons.


### Launching

To set up flask on Ubuntu/Debian:
(Make sure that working directory is KODE-2019.4/Project.)


```
export FLASK_APP=sps.py
export FLASK_ENV=development
flask run
```

Flask app will run at 127.0.0.1:5000 by default. To access application from outside:

```
flask run --host=0.0.0.0
```

To launch celery open second terminal and navigate to project's folder for your convinience.
Because we run in development enviroment, we can cut corners to test it.

```
celery worker -A celery_worker.celery -B --loglevel=info -E
```
By that command we launched worker with beat in 1 place. Easier to test.

## Running the tests

It was deadline and tests were not automated. World is full of pain and sadness.

### To test fueatures

By installing dependencies, you also installed HTTPie. So, next steps are easy and great.


To create subscription on certain stocks.
```
http POST http://127.0.0.1:5000/api/subscription email='your_email' ticker='ticker_acronym' min_price='min_number' max_price='max_price'
```
max_price and min_price are optional, but at least 1 have to be. Otherwise server will reject it.

To check subscriptions: (Only for development puposes)

```
http GET http://127.0.0.1:5000/api/subscription email='your_email'
```

To remove subscription from ticker: (It's clanky, but not I asked)


```
http POST http://127.0.0.1:5000/api/subscription email='your_email' ticker='ticker_acronym'
```

To unsubscribe:

```
http Delete http://127.0.0.1:5000/api/subscription email='your_email'
```

## Email

Well... You know aboutdeadlines...
It was not tested with real mail server. Do not try.

## Deployment

DO NOT DEPLOY IT! Your clients will go crazy because of essence of that problem.
It wasn't me, who asked for such confusing API. I'm sorry.

## Versioning

I hope, I will make v.2 in future to show how it should be done, But should I spend time on it?

## Authors

* **Mark Kalinin** - *Initial work* - [NordVindInd](https://github.com/nordvindind)

## License

Shoud I?

## Acknowledgments

* Thank you to my dog, that was resting around.
