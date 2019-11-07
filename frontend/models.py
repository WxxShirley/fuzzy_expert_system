from django.db import models

# Create your models here.

class computer(models.Model):
    id = models.PositiveIntegerField(primary_key = True)
    branch = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    type_choice = (
        ('G','高端本'),
        ('K','开发本'),
        ('S','商务本'),
        ('Q','轻薄本'),
        ('Y','游戏本'),
    )
    type = models.CharField(max_length=2,choices = type_choice,default = 'Q')
    year = models.IntegerField()
    colors = models.CharField(max_length=64)
    price = models.PositiveIntegerField()
    battery_score = models.FloatField()
    beauty_score = models.FloatField()
    disk_score = models.FloatField()
    price_score = models.FloatField()
    processor_score = models.FloatField()
    screen_score = models.FloatField()
    size_score = models.FloatField()
    weight = models.FloatField()

class computerImage(models.Model):
    name = models.CharField(max_length=64)
    src = models.CharField(max_length=128)

class computer_rawdata(models.Model):
    id = models.PositiveIntegerField(primary_key = True)
    memory = models.PositiveIntegerField()
    card = models.IntegerField()
    disk = models.PositiveIntegerField()
    cores = models.PositiveIntegerField()
    processor = models.CharField(max_length=16)
    screen = models.CharField(max_length=32)
    battery = models.FloatField()


#保存所有笔记本电脑数据的代码
"""
for i in range(2,159):
    id_ = booksheet.cell(row=i,column = 1).value
    memory = booksheet.cell(row=i,column = 8).value
    card = booksheet.cell(row=i,column = 9).value
    disk = booksheet.cell(row=i, column= 10).value
    cores = booksheet.cell(row=i,column = 11).value
    processor = booksheet.cell(row=i,column = 12).value
    screen = booksheet.cell(row=i,column = 14).value
    battery = booksheet.cell(row=i,column = 19).value
    data = models.computer_rawdata(id = id_,memory=memory,card=card,disk=disk,cores=cores,processor = processor,screen=screen,battery=battery)
    data.save()


"../../static/imgs/"

image = models.computerImage(name="技嘉 AERO15",src = "../../static/imgs/技嘉 AERO15.jpg")
image.save()
"""


class score_buffer(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    routine_score = models.FloatField()
    professional_score = models.FloatField()
    price_score = models.FloatField()
    enjoyment_score = models.FloatField()
    year_score = models.FloatField()
    battery_score = models.FloatField()
    beauty_score = models.FloatField()
    disk_score = models.FloatField()
    processor_score = models.FloatField()
    screen_score = models.FloatField()
    size_score = models.FloatField()
    overall_score = models.FloatField()
