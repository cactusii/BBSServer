from django.db import models

# Create your models here.

# 通常一个model对应数据库中的一张表
# Django中的model是以类的形式表现的
# 包含一些基本字段和行为

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.



from django.db import models

class Image(models.Model):
    img_name = models.CharField(max_length=250,primary_key=True,default='user_photo')
    img = models.ImageField(upload_to='image',height_field='url_height',width_field='url_width',default="user_photo.jpg")

    class Meta:

        db_table = 'Image'

class Dianzan(models.Model):
    tp_id = models.CharField(max_length=255,primary_key=True)
    sch_id = models.CharField(max_length=20)
    type = models.CharField(max_length=1)

    class Meta:
        db_table = 'Dianzan'
        unique_together = (('tp_id', 'sch_id', 'type'),)


class Guanzhu(models.Model):
    sch_id = models.CharField(primary_key=True,max_length=20)
    b_sch_id = models.CharField(max_length=20)

    class Meta:

        db_table = 'Guanzhu'
        unique_together = (('sch_id', 'b_sch_id'),)


class Pinglun(models.Model):
    id = models.CharField(max_length=255,primary_key=True)
    tiezi_id = models.CharField(max_length=255, blank=True, null=True)
    sch_id = models.CharField(max_length=20, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    dianzan_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Pinglun'


class Id(models.Model):
    sch_id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2)

    class Meta:

        db_table = 'ID'


class Picture(models.Model):
    pic_id = models.CharField(primary_key=True, max_length=255)
    tiezi_id = models.CharField(max_length=255)
    uri = models.CharField(max_length=255, blank=True, null=True)
    index = models.SmallIntegerField()

    class Meta:

        db_table = 'Picture'
        unique_together = (('pic_id', 'tiezi_id'),)


class Shoucang(models.Model):
    sch_id = models.CharField(primary_key=True, max_length=20)
    tiezi_id = models.IntegerField()

    class Meta:

        db_table = 'Shoucang'
        unique_together = (('sch_id', 'tiezi_id'),)


class Tiezi(models.Model):
    tiezi_id = models.CharField(primary_key=True,max_length=255)
    sch_id = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)
    dianzan_num = models.IntegerField(blank=True, null=True)
    liulan_num = models.BigIntegerField(blank=True, null=True)

    class Meta:

        db_table = 'Tiezi'


class User(models.Model):
    sch = models.ForeignKey(Id, models.DO_NOTHING, primary_key=True)
    username = models.CharField(max_length=255)
    photo = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    grade = models.CharField(max_length=4, blank=True, null=True)
    academy = models.CharField(max_length=255, blank=True, null=True)
    fatie_num = models.IntegerField()
    guanzhu_num = models.IntegerField()
    shoucang_num = models.IntegerField()
    fensi_num = models.IntegerField()
    register_date = models.DateField()
    jianjie = models.CharField(max_length=255,null=True)


    class Meta:
        db_table = 'User'


