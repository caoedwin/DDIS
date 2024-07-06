from django.db import models
import urllib

# Create your models here.
import mongoengine
from mongoengine import *

# _MONGODB_USER = urllib.parse.quote_plus("edwin")#'edwin'
# _MONGODB_PASSWD = urllib.parse.quote_plus("DCT@2019")#'DCT@2019'
# _MONGODB_HOST = '127.0.0.1:27016'
# _MONGODB_NAME = 'admin'
# _MONGODB_DATABASE_HOST = 'mongodb://%s:%s@%s/%s' % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
# mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
#
class StudentModel(Document):
    name = mongoengine.StringField(max_length=32)
    age = mongoengine.IntField()
    password = mongoengine.StringField(max_length=32)

    # def __str__(self):
    #     return self.name
    meta = {'collection': 'StudentModel'}

    def __unicode__(self):
        return self.name

class data1(Document):
    siteid = IntField(max_length=45)
    title = StringField(max_length=45)
    lng = StringField(max_length=45)
    lat = StringField(max_length=45)
    # 指明连接的数据表名
    meta = {'collection':'raw_data1'}
    def __unicode__(self):
        return self.name

class ToolList_Mongo(Document):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Phase_choice =(
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('NPI', 'NPI'),
        ('OS refresh', 'OS refresh'),
        ('OOC', 'OOC'),
        ('INV', 'INV'),
    )
    Customer = StringField(max_length=20, choices=Customer_choice)
    Project = StringField(max_length=20)
    Phase0 = StringField(max_length=20, choices=Phase_choice)
    Vendor = StringField(max_length=150, blank=True, null=True)
    Version = StringField(max_length=150)
    ToolName = StringField(max_length=300)
    TestCase = StringField(max_length=100)
    editor = StringField(max_length=20)
    edit_time = DateTimeField(max_length=26)
    meta = {'collection': 'ToolList_M'}

    def __unicode__(self):
        return '{Project}-{Phase0}-{ToolName}'.format(Project=self.Project, Phase0=self.Phase0, Location=self.ToolName)
