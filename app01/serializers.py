from rest_framework import serializers
from .models import *

class PersonalInfoserilizer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = "__all__"

class Departmentsserilizer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"

class Positionsserilizer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = "__all__"