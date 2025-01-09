from django.urls import path
from . import views

from cars import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_price, name='predict_price'),
    path('get-models/', views.get_models, name='get_models'),
    path('trend-analysis/', views.trend_analysis, name='trend_analysis'),
    path('collected-data/', views.collected_data, name='collected_data'),
    path('start-data-collection/', views.start_data_collection, name='start_data_collection'),
]

