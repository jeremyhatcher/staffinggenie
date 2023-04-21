from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='opportunities/', permanent=True)),
    path('home/', views.index, name='index'),
    path('opportunities/', views.OpportunitiesView.as_view(), name='opportunities-list'),
    path('opportunities/<int:pk>/', views.SingleOpportunityView.as_view(), name='opportunity-detail'),
    path('opportunities/<int:pk>/reserve/', views.reserve_opportunity, name='reserve_opportunity'),
]