from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .serializers import OpportunitySerializer
from .models import Opportunity
from django.contrib import messages
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime
import pytz
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

class OpportunitiesView(ListCreateAPIView):
    serializer_class = OpportunitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # admin users see all opportunities
            queryset = Opportunity.objects.all().order_by('-date')
            opportunities = None
        else:
            job_functions = []
            if user.is_unloader:
                job_functions.append('Unloading')
            if user.is_loader:
                job_functions.append('Loading')
            if user.is_pallet_picker:
                job_functions.append('Pallet Picking')
            if user.is_reserve_picker:
                job_functions.append('Reserve Picking')
            if user.is_receiver:
                job_functions.append('Receiving')
            if user.is_yard_driver:
                job_functions.append('Yard Driving')
            if user.is_desk_clerk:
                job_functions.append('Desk Clerking')
            if user.is_QA:
                job_functions.append('QA')
            if user.is_office_admin:
                job_functions.append('Office Admin')
            if user.is_AP:
                job_functions.append('AP')

            filters = Q()
            for jf in job_functions:
                filters |= Q(job_functions__iexact=jf)

            timezone = pytz.timezone('America/Los_Angeles')
            current_time = timezone.localize(datetime.now())

            # Only show opportunities that haven't passed yet
            filters &= Q(date__gte=current_time.date())

            queryset = Opportunity.objects.filter(filters).order_by('-date')
            
            opportunities = []
            for opp in queryset:
                if not opp.is_fully_booked():
                    opportunities.append(opp)

        if opportunities is not None:
            return opportunities
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            # only admin users can create opportunities
            raise PermissionDenied("You don't have the necessary permissions to create an opportunity.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SingleOpportunityView(RetrieveUpdateDestroyAPIView):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        return [IsAdminUser()]

    def get_object(self):
        opportunity_id = self.kwargs.get('pk')
        return get_object_or_404(Opportunity, pk=opportunity_id)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reserve_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    # check if the opportunity date has already passed
    timezone = pytz.timezone('America/Los_Angeles')
    current_time = timezone.localize(datetime.now())

    if opportunity.date < current_time.date():
        messages.error(request, 'This overtime opportunity has already passed.')
        return Response({'success': False, 'message': 'The date of this overtime opportunity has already passed.'})

    # get the user associated with the token
    user = request.user

    # create a hash map of job functions and corresponding boolean values for the user
    user_job_functions = {
        'Unloading': user.is_unloader,
        'Loading': user.is_loader,
        'Pallet Picking': user.is_pallet_picker,
        'Reserve Picking': user.is_reserve_picker,
        'Receiving': user.is_receiver,
        'Yard Driving': user.is_yard_driver,
        'Desk Clerking': user.is_desk_clerk,
        'QA': user.is_QA,
        'Office Admin': user.is_office_admin,
        'AP': user.is_AP,
    }
    print(user_job_functions)
    # check if the user is trained for the job functions required by the opportunity
    job_functions = opportunity.job_functions.split(',')
    print(job_functions)
    for jf in job_functions:
        if not user_job_functions.get(jf, False):
            raise PermissionDenied(f"The system is showing that you do not have the training required for the job function required by this overtime opportunity.")

        # check if the user has already reserved a slot for the same opportunity
        if opportunity.reserved_by.filter(pk=user.pk).exists():
            messages.error(request, 'You have already reserved a slot for this overtime opportunity.')
            return Response({'success': False, 'message': 'You have already reserved a slot for this overtime opportunity.'})
        
    # check if the user has already reserved an opportunity on the same day
    if Opportunity.objects.filter(date=opportunity.date, reserved_by=user).exclude(pk=pk).exists():
        messages.error(request, 'You have already reserved an overtime opportunity on this day.')
        return Response({'success': False, 'message': 'You have already reserved an overtime opportunity on this day.'})

    # check if opportunity is fully booked
    if opportunity.is_fully_booked():
        messages.error(request, 'This overtime opportunity is already fully booked.')
        return Response({'success': False, 'message': 'This overtime opportunity is already fully booked.'})

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

        message = f'Overtime opportunity on {opportunity.date} from {opportunity.start_time} to {opportunity.end_time} reserved successfully.'
        messages.success(request, message)
        return Response({'success': True, 'message': message})
    else:
        messages.error(request, 'This overtime opportunity is already fully booked.')
        message = 'This overtime opportunity is already fully booked.'
        return Response({'success': False, 'message': message})
