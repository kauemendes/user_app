from datetime import datetime


class DateKit:

    @staticmethod
    def convert_to_mysql_date_format(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")

        return None

    @staticmethod
    def convert_to_email_format(value):
        if value:
            return value.strftime("%d/%m/%Y %H:%M")

        return None

    @staticmethod
    def convert_to_url_calendar(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")

        return None


    @staticmethod
    def hour_diff(
            date_1: datetime,
            date_2: datetime
    ):

        time_diff = abs(date_1.timestamp() - date_2.timestamp())
        return time_diff/60/60

