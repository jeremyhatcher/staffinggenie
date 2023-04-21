from rest_framework import serializers
from .models import Opportunity

class OpportunitySerializer(serializers.ModelSerializer):
    reserved_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = '__all__'

    def get_reserved_by_names(self, obj):
        return ", ".join([f"{user.first_name} {user.last_name}" for user in obj.reserved_by.all()])
