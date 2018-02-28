from validate_email import validate_email


class ValidateKit(object):

    @staticmethod
    def validate_email(email):
        return validate_email(email)
