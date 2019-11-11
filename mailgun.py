import os
import requests


class MailGun:
    api_key = os.environ.get('MAILGUN_API_KEY')
    drop_route_id = os.environ.get('MAILGUN_DROP_ROUTE')
    fwd_route_id = os.environ.get('MAILGUN_FWD_ROUTE')
    mail_domain = os.environ.get('MAILGUN_MAIL_DOMAIN')

    def __init__(self, operation, username):
        self.operation = operation
        self.username = username

    def get_drop_route(self):
        # global api_key
        # global drop_route_id
        # global mail_domain
        r = requests.get(
            "https://api.mailgun.net/v3/routes/" + str(self.drop_route_id),
            auth=("api", str(self.api_key)))
        # return jsonify(r.json())
        route_exp = r.json()["route"]["expression"]
        route_recipient = route_exp.partition('match_recipient("(')[2]
        route_recipient = route_recipient.partition(
            ')@' + str(self.mail_domain) + '")')[0]
        # return route_exp
        return route_recipient.split('|')

    def update_drop_route(self, operation, username):
        # global api_key
        # global drop_route_id
        route_recipients = MailGun.get_drop_route(self)
        if operation == "add":
            route_recipients.append(username)
        elif operation == "del":
            if username in set(route_recipients):
                route_recipients.remove(username)
        # return jsonify(route_recipients)
        recipient_list = "|".join(route_recipients)
        match_recipient = 'match_recipient("(' + \
            recipient_list + ')@' + str(self.mail_domain) + '")'

        r = requests.put(
            "https://api.mailgun.net/v3/routes/" + str(self.drop_route_id),
            auth=("api", str(self.api_key)),
            data={"expression": match_recipient})

        return ""

    def get_fwd_route(self):
        # global api_key
        # global fwd_route_id
        r = requests.get(
            "https://api.mailgun.net/v3/routes/" + str(self.fwd_route_id),
            auth=("api", str(self.api_key)))

        # return jsonify(r.json())
        route_exp = r.json()["route"]["expression"]
        route_recipient = route_exp.partition('match_recipient("(')[2]
        route_recipient = route_recipient.partition(
            ')@' + str(self.mail_domain) + '")')[0]
        # return route_exp
        return route_recipient.split('|')

    def update_fwd_route(self, operation, username):
        # global api_key
        # global fwd_route_id
        route_recipients = MailGun.get_fwd_route(self)
        if operation == "add":
            route_recipients.append(username)
        elif operation == "del":
            if username in set(route_recipients):
                route_recipients.remove(username)
        # return jsonify(route_recipients)
        recipient_list = "|".join(route_recipients)
        match_recipient = 'match_recipient("(' + \
            recipient_list + ')@' + str(self.mail_domain) + '")'

        r = requests.put(
            "https://api.mailgun.net/v3/routes/" + str(self.fwd_route_id),
            auth=("api", str(self.api_key)),
            data={"expression": match_recipient})

        return ""
