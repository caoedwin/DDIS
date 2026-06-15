from rest_framework import serializers
from .models import (
    TestItemSW, TestProjectSW, TestPlanSW, RetestItemSW,
    FFRTByRD, TestProjectSWAIO, TestPlanSWAIO
)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TestItemSWOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestItemSW
        fields = '__all__'


class TestProjectSWOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestProjectSW
        fields = '__all__'


class TestPlanSWOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestPlanSW
        fields = '__all__'
        depth = 1


class RetestItemSWOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = RetestItemSW
        fields = '__all__'
        depth = 1


class FFRTByRDOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FFRTByRD
        fields = '__all__'


class TestProjectSWAIOOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestProjectSWAIO
        fields = '__all__'


class TestPlanSWAIOOSSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestPlanSWAIO
        fields = '__all__'
        depth = 1