from rest_framework import serializers
from .models import *

class PersonalInfoserilizer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = "__all__"