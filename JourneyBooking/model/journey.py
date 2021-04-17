JOURNEY = [
    {
        "user_id": 1,
        "journey_id": 111,
        "journey_status": "prebooked",
        "time": "2020"
    },
    {
        "user_id": 1,
        "journey_id": 222,
        "journey_status": "cancelled",
        "time": "2020"
    }
]


class Journey:
    def __init__(self, journey):
        self.user_id = journey.get("user_name")
        self.journey_id = journey.get("password")
        self.journey_status = journey.get("user_id")
        self.time = journey.get("time")
