from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import OpportunitySerializer
from .models import Opportunity

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

class OpportunitiesView(ListCreateAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class SingleOpportunityView(RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer



