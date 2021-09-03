from django.db import models
import os
# Create your models here.

class file_upload(models.Model):
    ids = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    up_file = models.FileField(upload_to='')

    def __str__(self):
        return self.file_name
