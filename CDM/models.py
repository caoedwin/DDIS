from django.db import models

# Create your models here.
class CDM(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)
    # Phase = models.CharField(max_length=20)
    SS_Data = models.CharField(max_length=20)
    A_cover_Material = models.CharField(max_length=50,default='')
    C_cover_Material = models.CharField(max_length=50)
    D_cover_Material = models.CharField(max_length=50)
    SKU_NO = models.CharField(max_length=10)
    Point1=models.FloatField()
    Point2 = models.FloatField()
    Point3 = models.FloatField()
    Point4 = models.FloatField()
    Point5 = models.FloatField()
    Point6 = models.FloatField()
    Point7 = models.FloatField()
    Ave = models.FloatField()
    # Point1 = models.CharField(max_length=20)
    # Point2 = models.CharField(max_length=20)
    # Point3 = models.CharField(max_length=20)
    # Point4 = models.CharField(max_length=20)
    # Point5 = models.CharField(max_length=20)
    # Point6 = models.CharField(max_length=20)
    # Point7 = models.CharField(max_length=20)
    # Ave = models.CharField(max_length=20)
    Conclusion = models.CharField(max_length=1000)
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'CDM'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    # def toJSON(self):
    #     import json
    #     return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    #可读性强
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        data=[]
        for attr in fields:
            d[attr] = getattr(self, attr)
            data.append(getattr(self, attr))

        import json
        return json.dumps(d)
        # return json.dumps(data)