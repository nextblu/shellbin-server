# Version 2 bin creator for shellbin

#  """
#  Copyright (c) 2020 NextBlu systems - - All Rights Reserved.
#   * MIT License
#   * Written by Mattia Failla <mattia@nextblu.com>, Sept 2020
#   """
import datetime

from flask_restful import Resource
from tentalog import Tentacle

from modules.stats import Stats

logger = Tentacle().logger


class StatsResource(Resource):
    def get(self):
        # Getting the last 60 days
        database_in_data = Stats().get_bin_per_day()
        latest_bin = Stats().get_last_bin_timestamp()

        # Cleaning days_data
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(60)]
        list_of_bin = []
        for day in date_list:
            res = [item for item in database_in_data if item['day'] == str(day)]
            if res is not None:
                # Get object data
                try:
                    list_of_bin.append({
                        "day": day,
                        "bins": res[0]['insertions']
                    })
                except IndexError:
                    list_of_bin.append({
                        "day": day,
                        "bins": 0
                    })
            else:
                list_of_bin.append({
                    "day": day,
                    "bins": 0
                })

        return {
                   "success": True,
                   "lastBin": latest_bin,
                   "statsPerDay": list_of_bin
               }, 200
