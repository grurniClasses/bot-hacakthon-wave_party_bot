
from WaveForecast import WaveForecast


class SpotControl:
    def __init__(self, database):
        self.db = database
        self.spots = self.db.get_collection("spots")

    def get_spot_by_id(self, spot_id):
        spot = self.spots.find_one({"spot_id": spot_id})
        return spot

    def add_user_to_spot(self, spot_id, chat_id):
        spot = self.get_spot_by_id(spot_id)
        if not spot:
           return self.spots.insert_one({"spot_id": spot_id, "users": [chat_id], "imgs": [], "forecast": []})
        if chat_id not in spot["users"]:
            updated_spot = self.spots.update_one(
                {"spot_id": spot_id}, {"$push": {"users": chat_id}}
            )
            return updated_spot
        return spot

    def add_pic_to_spot(self, spot_id, pic):
        pass

    def get_pics_by_spot(self, spot_id):
        pass

    def set_spot_forecast(self, spot_id):
        spot = self.get_spot_by_id(spot_id)
        forecast = WaveForecast()
        forecast.get_forecast(spot_id)
        display_forecast = forecast.display_forecast()
        spot = self.spots.update_one(
            {"spot_id": spot["spot_id"]}, {"$set": {"forecast": display_forecast}}
        )

    def get_spot_forecast(self, spot_id):
        spot = self.get_spot_by_id(spot_id)
        return spot["forecast"]
