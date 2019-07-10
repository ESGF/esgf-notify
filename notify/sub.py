from datetime import datetime, timedelta

class Sub(object):

    def __init__(self, id, fields, email_in):

        self.fields = fields
        self.id = id
        self.email = email_in
