from rest_framework import serializers
from .models import *

class INVGantserilizer(serializers.ModelSerializer):
    class Meta:
        model = INVGantt
        fields = "__all__"