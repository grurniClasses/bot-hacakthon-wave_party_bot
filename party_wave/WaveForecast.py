import datetime
import requests
import pytz


class WaveForecast:

    ENDPOINT = "https://magicseaweed.com/api/mdkey/forecast/?spot_id="
    FIELDS = "&units=eu&fields=localTimestamp,solidRating,fadedRating,swell.minBreakingHeight,swell.maxBreakingHeight,wind.speed"

    def __init__(self):
        self.forecast = []

    def get_forecast(self, spot_id):
        data = requests.get(self.ENDPOINT + spot_id + self.FIELDS).json()
        lists = [data[i : i + 8] for i in range(0, len(data), 8)]
        result = [[lists[i][j] for j in [2, 4, 6]] for i in range(len(lists))]
        self.forecast = result

    def localtimestamp_to_utc(self, timestamp):
        local_tz = pytz.timezone("Israel")
        local_timestamp = datetime.datetime.fromtimestamp(timestamp)
        local_timestamp = local_tz.localize(local_timestamp, is_dst=None)
        utc_timestamp = local_timestamp.astimezone(pytz.utc)
        return utc_timestamp.strftime("%d-%m-%Y %H:%M:%S")

    def display_forecast(self):
        forecast_week = ""
        for days in range(len(self.forecast)):
            print(self.forecast[days])
            forecast_day = ""
            for obj in self.forecast[days]:
                utc_timestamp = self.localtimestamp_to_utc(obj["localTimestamp"])
                solid_rating = "⭐️" * obj["solidRating"]
                min_height = obj["swell"].get("minBreakingHeight", 0)
                max_height = obj["swell"].get("maxBreakingHeight", 0)
                wind_speed = obj["wind"].get("speed", 0)
                forecast_day += f"Date: {utc_timestamp}\nRating: {solid_rating}\nMinHeight: {min_height}m\nMaxHeight: {max_height}m\nWindSpeed: {wind_speed}kph\n-----------------------------------\n"
            forecast_week += forecast_day + "**********************\n"
        return forecast_week
