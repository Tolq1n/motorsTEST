from django.urls import path, include
from .views import DataMaker
from .views import BrandListAPIView, CarModelListAPIView, ModelListAPIVIew, GenerationListAPIVIew, CarCreateAPIView, FilteredCarsListAPIVIew, ImagePostAPIView

urlpatterns = [
    path('json-file', DataMaker.as_view()),
    path('brands/', BrandListAPIView.as_view()),
    path('models/', CarModelListAPIView.as_view()),
    path('models/<int:pk>/', ModelListAPIVIew.as_view()),
    path('models/generations/<int:pk>/', GenerationListAPIVIew.as_view()),
    path('filter-by-generation/<int:pk>', FilteredCarsListAPIVIew.as_view()),
    path('create', CarCreateAPIView.as_view()),

    path('image', ImagePostAPIView.as_view())
]