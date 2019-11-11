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

# start the app in ubuntu server
    $ export LC_ALL=C.UTF-8
    $ export LANG=C.UTF-8
    $ export FLASK_APP=mail.py
    $ flask run --host=0.0.0.0

### setup gunicorn
    activate the python venv
    $ pip install gunicorn
    $ gunicorn -w 3 mail:app

### setup supervisor
    $ sudo apt install supervisor
    $ sudo nano /etc/supervisor/conf.d/tempmail.conf

```conf
[program:tempmail]
directory=/home/<username>/<src_directory>
command=/home/<username>/<src_directory>/venv/bin/gunicorn -w 3 -b :5000 mail:app
user=<username>
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/<app_name>/tempmail.err.log
stdout_logfile=/var/log/<app_name>/tempmail.out.log
```

    [create the supervisor log and output directory and files](#setup-supervisor-log-and-output)
    $ sudo service supervisor restart

#### setup supervisor log and output
    $ sudo mkdir -p /var/log/`app_name`
    $ sudo touch /var/log/`app_name`/tempmail.err.log
    $ sudo touch /var/log/`app_name`/tempmail.out.log

