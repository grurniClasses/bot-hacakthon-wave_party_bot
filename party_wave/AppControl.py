import bot_settings
from WaveForecast import WaveForecast


class SpotControl:
    def __init__(self, database):
        self.db = database
        self.spots = self.db.get_collection("spots")

    def add_user_to_spot(self, spot_id, chat_id):
        spot = self.spots.update_one({"spot_id": spot_id}, {'$push': {"users": chat_id}})
        return spot

    def add_pic_to_spot(self, spot_id, pic):
        pass

    def get_spot_by_id(self, spot_id):
        spot = self.spots.find_one({"spot_id": spot_id})
        return spot

    def get_spot_forecast(self, spot_id):
        spot = self.get_spot_by_id(spot_id)
        if not spot["forecast"]:
            forecast = WaveForecast()
            forecast.get_forecast(spot)
            display_forecast = forecast.display_forecast()
            spot = self.spots.update_one({"spot_id": spot}, {'$set': {"forecast": display_forecast}})
        return spot["forecast"]



class UserControl:
    def __init__(self, database):
        self.db = database
        self.user = self.db.get_collection("users")

    def add_user(self, chat_id):
        new_user = {"chat_id": chat_id, "spots": []}
        res = self.user.insert_one(new_user)
        return res.inserted_id

    def find_user(self, chat_id):
        res = self.user.find_one({"chat_id": chat_id})
        if not res:
            return False
        return True

    def get_user_from_db(self, chat_id):
        res = self.user.find_one({"chat_id": chat_id})
        res.pop("_id")
        return res

    def update_user(self, user):
        user = self.update_one({"chat_id": user["chat_id"]}, {**user})
        return user

    def set_spot(self, chat_id, spot_id):
        user = self.get_user_from_db(chat_id)
        if spot_id not in user["spots"]:
            update = self.user.update_one(
                {"chat_id": user["chat_id"]}, {"$push": {"spots": spot_id}}
            )
        return user

    def get_user_spots(self, chat_id):
        user = self.user.find_one({"chat_id": chat_id})
        spots = [
            value
            for area in bot_settings.BEACHES.values()
            for key, value in area.items()
            if key in user["spots"]
        ]

<<<<<<< HEAD
    def handle_user_report(self, report):
        pass

    def get_forecast(self, id):
        user = self.get_user_from_db(id)
        data = requests.get(self.ENDPOINT + user["spots"][0] + self.FIELDS).json()
        array_by_day = [
            [data[j] for j in range(2, len(data[i : i + 8]), 2)]
            for i in range(0, len(data), 8)
        ]
        return array_by_day


=======
>>>>>>> 7e67d784e3bd10f0188aa4dde65dac7bc3f3b256
