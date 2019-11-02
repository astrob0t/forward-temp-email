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

