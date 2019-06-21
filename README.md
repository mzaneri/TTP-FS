# TTP-FS

## Install

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Run

```
$ export FLASK_APP=entry.py
$ flask run
```

Open browser to `http://127.0.0.1:5000`

## TODOs
- [ ] Add check to make sure user enters valid email address
- [ ] Make buys and sells atomic. Currently the tx and update of user balance are separate transactions.
- [ ] Split up portfolio functions in seperate smaller functions
- [ ] Redirect invalid routes
- [ ] Change secret key to be initialize from enviornmental variable
- [ ] Enforce PEP8 syntax
- [ ] Unit tests with pytest
- [ ] Handle all response codes. Currently only handles 200
