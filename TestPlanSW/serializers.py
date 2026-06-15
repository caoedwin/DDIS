from rest_framework import serializers
from .models import (
    TestItemSW, TestProjectSW, TestPlanSW, RetestItemSW,
    FFRTByRD, TestProjectSWAIO, TestPlanSWAIO
)
from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    支持动态选择字段的 ModelSerializer
    使用方式：?fields=field1,field2
    """
    def __init__(self, *args, **kwargs):
        # 从 kwargs 中取出 fields 参数
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # 只保留请求中指定的字段
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class TestItemSWSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestItemSW
        fields = '__all__'

class TestProjectSWSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProjectSW
        fields = '__all__'

class TestPlanSWSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestPlanSW
        fields = '__all__'
        depth = 1   # 显示外键关联对象的详情

class RetestItemSWSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetestItemSW
        fields = '__all__'
        depth = 1

class FFRTByRDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FFRTByRD
        fields = '__all__'

class TestProjectSWAIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProjectSWAIO
        fields = '__all__'

class TestPlanSWAIOSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestPlanSWAIO
        fields = '__all__'
        depth = 1