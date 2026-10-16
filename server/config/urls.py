from django.contrib import admin
from django.urls import path

from config.views import (
    login_user,
    logout_user,
    get_dealers,
    get_dealer_by_id,
    get_dealer_reviews,
    get_cars,
    analyze_review,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Existing frontend routes
    path("djangoapp/login", login_user),
    path("djangoapp/logout", logout_user),
    path("djangoapp/get_dealers", get_dealers),
    path("djangoapp/get_dealers/<int:dealer_id>", get_dealers),
    path("djangoapp/get_cars", get_cars),

    # Capstone API routes
    path("fetchDealers", get_dealers),
    path("fetchDealers/<str:state>", get_dealers),
    path("fetchDealer/<int:dealer_id>", get_dealer_by_id),
    path("fetchReviews/dealer/<int:dealer_id>", get_dealer_reviews),
    path("analyze/<path:review_text>", analyze_review),
]
