from .models import StudentModel
#SQL
#from rest_framework import serializers
#mongodb
from rest_framework_mongoengine import serializers
from . import models

#sql
# Serializers定义了API的表现形式
# class StudentSerializers(serializers.ModelSerializer):#是用ModelSerializer来序列化module层
#     class Meta:
#         module = StudentModel #指定要序列化的模型
#         # fields = ("name", "age", "password")#指定要序列化的字段
#         fields = "__all__"#表示所有字段
#mongodb
class StudentSerializers(serializers.DocumentSerializer):#是用ModelSerializer来序列化module层
    class Meta:
        model = StudentModel #指定要序列化的模型
        # fields = ("name", "age", "password")#指定要序列化的字段
        fields = "__all__"#表示所有字段
class data1Serializer(serializers.DocumentSerializer):
    class Meta:
        model = models.data1
        fields = '__all__' #这个是将所有的字段都序列化

class ToolSerializer(serializers.DocumentSerializer):
    class Meta:
        model = models.ToolList_Mongo
        fields = '__all__'