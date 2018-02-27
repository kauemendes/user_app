import boto
import os

from app import app, mailer, mail


class EmailKit:
    @staticmethod
    def message_dispatch(email_to, subject, body):

        # converting it to array
        if type(email_to) == str:
            email_to = [email_to]

        # apenas o ambiente de development
        if os.getenv('APP_SETTINGS') == "config.DevelopmentContainerConfig" and app.config["DEBUG"]:
            # replace for medt.com.br emails with debug true making sure we are sending not to production
            for i, val in enumerate(email_to):
                val = val.split("@")[0] + "@medt.com.br"
                email_to[i] = val

        try:
            mailer.send(
                to_addresses=email_to,
                subject=subject,
                body=body,
                format="html"
            )
            return True
        except boto.exception.BotoServerError as error:
            return False

    @staticmethod
    def message_dispatch_sendgrid(email_to: list, subject: str, body: str, *args, **kwargs) -> object:

        # converting it to array
        if type(email_to) == str:
            email_to = [email_to]

        # apenas o ambiente de development
        if (os.getenv('APP_SETTINGS') == "config.DevelopmentConfig" or
                    os.getenv('APP_SETTINGS') == "config.DevelopmentContainerConfig") or app.config["DEBUG"]:
            # replace for medt.com.br emails with debug true making sure we are sending not to production
            for i, val in enumerate(email_to):
                val = val.split("@")[0] + "@medt.com.br"
                email_to[i] = val

        to_email = []
        for m in email_to:
            key = "email"
            to_email.append({key: m})

        from_email = kwargs["from_email"] if "from_email" in kwargs else app.config['SENDGRID_DEFAULT_FROM']

        if "from_email" in kwargs:
            kwargs.pop("from_email")

        try:
            mail.send_email(
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                html="<html><body><b> This is something default content </body></html>",
                *args,
                **kwargs
            )
            return True
        except Exception as e:
            raise e
