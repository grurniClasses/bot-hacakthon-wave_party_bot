import datetime
import pytz


class WaveForecast:
  
  def __init__(self, forecast):
    self.forecast = forecast

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
        forecast_day += f"Date: {utc_timestamp}\nRating: {faded_rating} / {solid_rating}\nMinHeight: {min_height}m\nMaxHeight: {max_height}m\nWindSpeed: {wind_speed}kph "