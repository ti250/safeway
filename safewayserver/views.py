from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from parse_json import JourneyParameters
from route_finder import route_finder
import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def get_route(request):
    try:
        journey_params = JourneyParameters.from_json(request.body)
        # Call some code to calculate the correct journey
        print('RECIEVED:', journey_params)
        route = json.dumps(route_finder(journey_params))
        response = HttpResponse(route)
        response.status_code = 201
    except Exception as e:
        print(e)
        response = HttpResponse('Invalid JSON')
        response.status_code = 400
    return response
