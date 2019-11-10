# insitiate a virtualENV and install the following python packages
    $ python3 -m venv .venv
    $ pip install requests
    $ pip install flask
    $ pip install flask_cors
    $ pip install flask_sqlalchemy
    $ pip install flask_marshmallow
    $ pip install marshmallow_sqlalchemy

# Generate SQLite database
### enter into python interactive shell
    $ python
    >>> from mail import db
    >>> db.create_all()
    >>> exit()

# create ENV variables
    MAILGUN_API_KEY -> mailgun private key
    MAILGUN_MAIL_DOMAIN -> email domain for the temporary emails
    MAILGUN_DROP_ROUTE -> id of the dropping route
    MAILGUN_FWD_ROUTE -> id of the forwarding route