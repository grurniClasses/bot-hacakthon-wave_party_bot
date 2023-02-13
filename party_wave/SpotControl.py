from WaveForecast import WaveForecast


class SpotControl:
    def __init__(self, database):
        self.db = database
        self.spots = self.db.get_collection("spots")

    def get_spot_by_id(self, spot_id):
        spot = self.spots.find_one({"spot_id": spot_id})
        if not spot:
            new_spot = self.spots.insert_one(
                {"spot_id": spot_id, "imgs": [], "msgs": [], "forecast": ""}
            )
            return new_spot
        return spot

    def add_pic_to_spot(self, spot_id, pic):
        updated_spot = self.spots.update_one(
            {"spot_id": spot_id}, {"$push": {"imgs": str(pic)}}
        )
        return updated_spot

    def get_pics_by_spot(self, spot_id):
        spot = self.spots.find_one({"spot_id": spot_id})
        return spot["imgs"]

    def set_spot_forecast(self, spot_id):
        spot = self.get_spot_by_id(spot_id)
        forecast = WaveForecast()
        forecast.get_forecast(spot_id)
        display_forecast = forecast.display_forecast()
        updated_spot = self.spots.update_one(
            {"spot_id": spot["spot_id"]}, {"$set": {"forecast": str(display_forecast)}}
        )
        return updated_spot

    def get_spot_forecast(self, spot_id):
        spot = self.get_spot_by_id(spot_id)
        return spot["forecast"]
