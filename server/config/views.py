import json
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DATA_DIR = Path(__file__).resolve().parent.parent / "database" / "data"


def load_data(filename, key):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)[key]


def dealers_data():
    return load_data("dealerships.json", "dealerships")


def cars_data():
    return load_data("car_records.json", "cars")


def reviews_data():
    return load_data("reviews.json", "reviews")


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
        password=data.get("password", ""),
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid username or password"}, status=401
        )

    login(request, user)
    return JsonResponse({
        "userName": user.username,
        "status": "Authenticated",
    })


@csrf_exempt
def logout_user(request):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "GET or POST required"}, status=405)

    logout(request)
    return JsonResponse({"userName": ""})


def get_dealers(request, dealer_id=None, state=None):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    dealers = dealers_data()

    if dealer_id is not None:
        for dealer in dealers:
            if int(dealer["id"]) == dealer_id:
                return JsonResponse({"status": 200, "dealer": dealer})
        return JsonResponse({"error": "Dealer not found"}, status=404)

    selected_state = state or request.GET.get("state")

    if selected_state:
        selected_state = selected_state.strip().lower()
        dealers = [
            dealer for dealer in dealers
            if dealer.get("state", "").lower() == selected_state
            or dealer.get("st", "").lower() == selected_state
        ]

    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_by_id(request, dealer_id):
    return get_dealers(request, dealer_id=dealer_id)


def get_dealer_reviews(request, dealer_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    reviews = [
        review for review in reviews_data()
        if int(review.get("dealership", -1)) == dealer_id
    ]
    return JsonResponse({"status": 200, "reviews": reviews})


def get_cars(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    cars = cars_data()
    unique_cars = []
    seen = set()

    for car in cars:
        pair = (car.get("make", ""), car.get("model", ""))
        if pair not in seen:
            seen.add(pair)
            unique_cars.append({
                "CarMake": pair[0],
                "CarModel": pair[1],
            })

    return JsonResponse({"CarModels": unique_cars})


def analyze_review(request, review_text):
    if request.method != "GET":
        return JsonResponse({"error": "GET required"}, status=405)

    words = set(
        review_text.lower()
        .replace("!", " ")
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )

    positive_words = {
        "fantastic", "excellent", "great", "good", "amazing",
        "wonderful", "helpful", "friendly", "love", "best",
        "satisfied", "awesome", "perfect", "happy", "fast",
        "services", "service",
    }
    negative_words = {
        "bad", "poor", "terrible", "awful", "worst", "hate",
        "slow", "rude", "broken", "disappointed", "horrible",
        "unhelpful", "dirty", "expensive",
    }

    positive_score = len(words & positive_words)
    negative_score = len(words & negative_words)

    if positive_score > negative_score:
        sentiment = "positive"
    elif negative_score > positive_score:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return JsonResponse({"sentiment": sentiment})
