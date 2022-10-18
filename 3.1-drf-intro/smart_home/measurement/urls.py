from django.urls import path

from .views import SensorListView, SensorView, MeasurementView

urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<pk>/', SensorView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]
