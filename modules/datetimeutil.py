import datetime

import dateutil.parser
import pytz

from config import TimeConfig


class Now:
    @staticmethod
    def utc(datetime_format):
        """Use case: when a UTC timestamp is needed (just to be printed somewhere, not to be sent via JSON)"""
        return datetime.datetime.utcnow().strftime(datetime_format)

    @staticmethod
    def to_utc_us_datetime():
        """Use case: when a datetime object needs to be stored into a DB"""
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def localized(timezone, date_format=TimeConfig.DEFAULT):
        """Use case: when a localized timestamp is needed (just to be printed somewhere, not to be sent via JSON)"""
        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone(pytz.timezone(timezone)).strftime(date_format)
        return local_time


class FutureDate:
    @staticmethod
    def next_week():
        """Use case: when a future data needs to be stored in a DB"""
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=7)
        next_week = now + delta
        return next_week


class ISO8601:
    @staticmethod
    def to_datetime_obj(iso8601_datetime):
        """Use case: when a iso8601 formatted datetime needs to be stored into a DB"""
        return dateutil.parser.parse(iso8601_datetime)

    @staticmethod
    def to_utc_us_datetime(iso8601_datetime):
        """Use case: when a iso8601 formatted datetime needs to be saved into a DB"""
        ISO8601.to_datetime_obj(iso8601_datetime)
        return

    @staticmethod
    def from_utc_us_datetime(utc_us_datetime):
        """Use case: when a datetime string fetched from a DB has to be sent via JSON we use iso8601 format"""
        if utc_us_datetime:
            datetime_obj = datetime.datetime.strptime(
                utc_us_datetime, "%Y-%m-%d %H:%M:%S"
            )
            return ISO8601.from_datetime_obj(datetime_obj)
        else:
            return utc_us_datetime

    @staticmethod
    def from_datetime_obj(datetime_obj):
        """Use case: when a datetime object needs to be sent via JSON we use iso8601 format"""
        if datetime_obj:
            return datetime_obj.isoformat()
        return datetime_obj


class Year:
    @staticmethod
    def current_year():
        now = datetime.datetime.now()
        return now.year
