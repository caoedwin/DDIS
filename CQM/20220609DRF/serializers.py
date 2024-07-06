from rest_framework import serializers
from .models import *

class CQMserilizer(serializers.ModelSerializer):
    class Meta:
        model = CQM
        fields = "__all__"