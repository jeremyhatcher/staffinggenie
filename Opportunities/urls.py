from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('opportunities/', views.OpportunitiesView.as_view()),
    path('opportunities/<int:pk>', views.SingleOpportunityView.as_view()),
]