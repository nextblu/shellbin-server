# Version 2 bin creator for shellbin

#  """
#  Copyright (c) 2020 NextBlu systems - - All Rights Reserved.
#   * MIT License
#   * Written by Mattia Failla <mattia@nextblu.com>, Sept 2020
#   """
import datetime

from flask import request
from flask_restful import Resource
from tentalog import Tentacle

from modules import datetimeutil
from modules.stats import Stats

logger = Tentacle().logger


class StatsResource(Resource):
    def get(self):
        order = request.args.get('order')
        days = request.args.get('user')
        if not days or (not isinstance(days, int)) or (days not in range(1, 120)):
            days = 30
        if not order or ((order != 'ASC') and (order != 'DESC')):
            order = 'ASC'
        # Getting the last x Days of stats
        database_in_data = Stats().get_bin_per_day(interval=days, order=order)
        latest_bin = Stats().get_last_bin_timestamp()

        logger.debug(f"Database data for the last {days} days: {database_in_data}")

        # Cleaning days_data
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(int(days))]
        list_of_bin = []
        for day in date_list:
            day = day.date()
            logger.debug(f"Looking for day: {day}")
            res = [item for item in database_in_data if item['day'].strftime('%Y-%m-%d') == str(day)]
            logger.debug(f"Res item: {res}")
            if res is not None:
                # Get object data
                try:
                    list_of_bin.append({
                        "day": datetimeutil.ISO8601.from_datetime_obj(day),
                        "bins": res[0]['insertions']
                    })
                except IndexError:
                    list_of_bin.append({
                        "day": datetimeutil.ISO8601.from_datetime_obj(day),
                        "bins": 0
                    })
            else:
                list_of_bin.append({
                    "day": datetimeutil.ISO8601.from_datetime_obj(day),
                    "bins": 0
                })

        return {
                   "success": True,
                   "latestBin": latest_bin,
                   "statsPerDay": list_of_bin
               }, 200
