import datetime
import requests
import pytz
from pydantic import BaseModel


class WaveForecast(BaseModel):
  ENDPOINT = "https://magicseaweed.com/api/mdkey/forecast/?spot_id="
  FIELDS = "&units=eu&fields=localTimestamp,solidRating,fadedRating,swell.minBreakingHeight,swell.maxBreakingHeight,wind.speed"
  # local_time_stamp: datetime
  # faded_rating: int
  # solid_rating: int
  # min_height: float
  # max_height: float
  # wind_speed: int
  forecast = []

  def get_forecast(self, spot_id):
        data = requests.get(self.ENDPOINT + spot_id + self.FIELDS).json()
        array_by_day = [
            [data[j] for j in range(2, len(data[i : i + 8]), 2)]
            for i in range(0, len(data), 8)
        ]
        self.forecast = array_by_day

  def localtimestamp_to_utc(self, timestamp):
    local_tz = pytz.timezone('Israel')
    utc_timestamp = local_tz.localize(timestamp).astimezone(pytz.utc)
    return utc_timestamp

  def display_forecast(self):
    foracast_week = ""
    for days in range(len(self.forecast)):
      forecast_day = ""
      for obj in self.forecast[days]:
        utc_timestamp = self.localtimestamp_to_utc(obj["localTimestamp"])
        faded_rating = "⭐️" * obj["fadedRating"]
        solid_rating = "⭐️" * obj["solidRating"]
        min_height = obj["swell"][0]
        max_height = obj["swell"][1]
        wind_speed = obj["wind"][0]
        forecast_day += f"Date: {utc_timestamp}\nRating: {faded_rating} / {solid_rating}\nMinHeight: {min_height}m\nMaxHeight: {max_height}m\nWindSpeed: {wind_speed}kph\n"
      foracast_week += forecast_day
    return foracast_week