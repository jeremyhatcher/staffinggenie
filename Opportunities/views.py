from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .serializers import OpportunitySerializer
from .models import Opportunity, CustomUser
from django.contrib import messages
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def index(request):
    return render(request, 'index.html', {})

class OpportunitiesView(ListCreateAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class SingleOpportunityView(RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

    def get_object(self):
        opportunity_id = self.kwargs.get('pk')
        return get_object_or_404(Opportunity, pk=opportunity_id)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reserve_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    print(f"Opportunity ID: {opportunity.id}")

    # check if opportunity is fully booked
    if opportunity.is_fully_booked():
        messages.error(request, 'This overtime opportunity is already fully booked.')
        return Response({'success': False, 'message': 'This overtime opportunity is already fully booked.'})

    # get the user associated with the token
    user = request.user
    print(f"User ID: {user.id}")

     # check if the user has already reserved a slot for the same opportunity
    if opportunity.reserved_by.filter(pk=user.pk).exists():
        messages.error(request, 'You have already reserved a slot for this overtime opportunity.')
        return Response({'success': False, 'message': 'You have already reserved a slot for this overtime opportunity.'})
    
    # check if the user has already reserved an opportunity on the same day
    if Opportunity.objects.filter(date=opportunity.date, reserved_by=user).exclude(pk=pk).exists():
        messages.error(request, 'You have already reserved an overtime opportunity on this day.')
        return Response({'success': False, 'message': 'You have already reserved an overtime opportunity on this day.'})

    # reserve opportunity and update reserved_by and available_slots fields
    if opportunity.available_slots > 0:
        opportunity.reserved_by.add(user)
        opportunity.available_slots -= 1

        # update reserved_by_names field
        if opportunity.reserved_by.count() == 1:
            opportunity.reserved_by_names = f"{user.first_name} {user.last_name}"
        else:
            opportunity.reserved_by_names += f", {user.first_name} {user.last_name}"
        opportunity.save()

        print("opportunity reserved successfully.")
        message = f'Overtime opportunity on {opportunity.date} from {opportunity.start_time} to {opportunity.end_time} reserved successfully.'
        messages.success(request, message)
        return Response({'success': True, 'message': message})
    else:
        messages.error(request, 'This overtime opportunity is already fully booked.')
        message = 'This overtime opportunity is already fully booked.'
        return Response({'success': False, 'message': message})
