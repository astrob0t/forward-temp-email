# Install the following python packages
    $ pip install flask_sqlalchemy
    $ pip install flask_marshmallow
    $ pip install marshmallow-sqlalchemy

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