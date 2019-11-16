import os
import requests


class MailGun:
    api_key = os.environ.get('MAILGUN_API_KEY')
    drop_route_id = os.environ.get('MAILGUN_DROP_ROUTE')
    fwd_route_id = os.environ.get('MAILGUN_FWD_ROUTE')
    mail_domain = os.environ.get('MAILGUN_MAIL_DOMAIN')


    def __init__(self, operation, route, username):
        self.operation = operation
        self.route = route
        self.username = username

    def get_route(self, route_id):
        # global api_key
        # global drop_route_id
        # global mail_domain
        r = requests.get(
            "https://api.mailgun.net/v3/routes/" + str(route_id),
            auth=("api", str(self.api_key)))
        # return jsonify(r.json())
        route_exp = r.json()["route"]["expression"]
        route_recipient = route_exp.partition('match_recipient("(')[2]
        route_recipient = route_recipient.partition(
            ')@' + str(self.mail_domain) + '")')[0]
        # return route_exp
        return route_recipient.split('|')

    """
    accepts 3 parameters to decide what operation to perform on which route for the given username 
    """
    def update_route(self, operation, route, username):
        # global api_key
        # global drop_route_id
        if route == "forward":
            route_id = self.fwd_route_id
        elif route == "drop":
            route_id = self.drop_route_id

        route_recipients = MailGun.get_route(self, route_id)
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
            "https://api.mailgun.net/v3/routes/" + str(route_id),
            auth=("api", str(self.api_key)),
            data={"expression": match_recipient})

        # return ""
