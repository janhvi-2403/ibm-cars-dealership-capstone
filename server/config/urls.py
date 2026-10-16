
from django.contrib import admin
from django.urls import path
from config.views import (
    login_user,
    logout_user,
    get_dealers,
    get_cars,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/login", login_user),
    path("djangoapp/logout", logout_user),
    path("djangoapp/get_dealers", get_dealers),
    path("djangoapp/get_dealers/<int:dealer_id>", get_dealers),
    path("djangoapp/get_cars", get_cars),
]
