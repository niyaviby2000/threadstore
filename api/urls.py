from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter


router=DefaultRouter()

router.register("product",views.ProductViewSetView,basename="product")

urlpatterns=[

    path('register/',views.UserCreationView.as_view()),

    path('token/',ObtainAuthToken.as_view()),


]+router.urls