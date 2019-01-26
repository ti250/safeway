import json
from datetime import date, time, datetime, timedelta
from pytz import timezone


class JourneyParameters(object):
    def __init__(self, origin, destination, safety_priority, travel_time=None):
        self.origin = origin
        self.destination = destination
        self.safety_priority = safety_priority
        self.travel_time = travel_time

    @classmethod
    def from_json(cls, string):
        loaded_json = json.loads(string)
        if 'origin' in loaded_json.keys():
            origin = (loaded_json['origin']['latitude'],
                      loaded_json['origin']['longitude'])
            destination = (loaded_json['destination']['latitude'],
                           loaded_json['destination']['longitude'])
            safety_priority = loaded_json['safety_priority']
            arrive_by = loaded_json['arrive_by']
            if arrive_by is not None:
                gmt = timezone('GMT')
                # Should let the timezone be set by the user
                arrival_time = time(arrive_by['hour'],
                                    arrive_by['minute'])
                current_date = date.today()
                if datetime.combine(current_date, arrival_time, tzinfo=gmt) < datetime.now(gmt):
                    arrive_by = datetime.combine(current_date, arrival_time, tzinfo=gmt) + timedelta(days=1)
                else:
                    arrive_by = datetime.combine(current_date, arrival_time, tzinfo=gmt)
                travel_time = (arrive_by - datetime.now(gmt)).seconds
            else:
                travel_time = None
            return cls(origin, destination, safety_priority, travel_time)

    def __repr__(self):
        return ('origin: ' + str(self.origin) + " destination: " + str(self.destination)
                + ' safety_priority: ' + str(self.safety_priority) + ' travel_time: ' + str(self.travel_time))

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    dictionary = {"origin": {"latitude": 50.39, "longitude": 40.31},
              "destination": {"latitude": 20.39, "longitude": 10.31},
              "arrive_by": {"hour": 12, "minute": 34, "timezone": -1},
              "safety_priority": 1.2}
    params = JourneyParameters.from_json(json.dumps(dictionary))
    print(params)
