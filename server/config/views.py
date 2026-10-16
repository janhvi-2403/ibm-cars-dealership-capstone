import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

SAMPLE_DEALERS = [
    {
        "id": 1,
        "full_name": "Sample Motors",
        "city": "Detroit",
        "state": "Michigan",
        "address": "100 Main Street"
    },
    {
        "id": 2,
        "full_name": "Example Auto Center",
        "city": "Chicago",
        "state": "Illinois",
        "address": "200 Lake Street"
    }
]
SAMPLE_CAR_MAKES = [
    {
        "id": 1,
        "name": "Toyota",
        "models": ["Camry", "Corolla"]
    },
    {
        "id": 2,
        "name": "Honda",
        "models": ["Civic", "Accord"]
    },
    {
        "id": 3,
        "name": "BMW",
        "models": ["3 Series", "5 Series"]
    }
]



@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request,
        username=data.get("userName", ""),
        password=data.get("password", "")
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid username or password"},
            status=401
        )

    login(request, user)
    return JsonResponse({
        "userName": user.username,
        "status": "Authenticated"
    })


@csrf_exempt
def logout_user(request):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "GET or POST required"}, status=405)

    logout(request)
    return JsonResponse({"userName": ""})


def get_dealers(request, dealer_id=None):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    if dealer_id is not None:
        for dealer in SAMPLE_DEALERS:
            if dealer["id"] == dealer_id:
                return JsonResponse({
                    "status": 200,
                    "dealer": dealer
                })

        return JsonResponse({"error": "Dealer not found"}, status=404)

    dealers = SAMPLE_DEALERS
    state = request.GET.get("state")

    if state:
        dealers = [
            dealer for dealer in SAMPLE_DEALERS
            if dealer["state"].lower() == state.lower()
        ]

    return JsonResponse({"status": 200, "dealers": dealers})



def get_cars(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    return JsonResponse({
        "status": 200,
        "CarMakes": SAMPLE_CAR_MAKES
    })

def get_cars(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    cars = [
        {"CarMake": "Toyota", "CarModel": "Camry"},
        {"CarMake": "Toyota", "CarModel": "Corolla"},
        {"CarMake": "Honda", "CarModel": "Civic"},
        {"CarMake": "Honda", "CarModel": "Accord"},
        {"CarMake": "BMW", "CarModel": "3 Series"},
        {"CarMake": "BMW", "CarModel": "5 Series"},
    ]

    return JsonResponse({"CarModels": cars})
