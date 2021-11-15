import urllib
import os

import requests
from django.db import models
from django.core.files import File
from datetime import datetime
import uuid


class BaseModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    small_img = models.ImageField(
        upload_to="small_img", null=True, blank=True
    )
    description = models.TextField()
    img = models.ImageField(upload_to="img", null=True, blank=True)

    def cacheImg(self, url):
        print(url)
        url_name = url.split("/")[-1]
        with open("pict_parsed/" + url_name, "wb") as f:
            f.write(requests.get(url).content)
        da = datetime.now()
        self.img.save(
            os.path.basename(
                str(da.time()) + str(da.date()) + uuid.uuid4().hex + url_name
            ),
            File(open("pict_parsed/" + url_name, "rb")),
        )
        os.remove("pict_parsed/" + url_name)
        self.save()

    def cacheSmallImg(self, url):
        print(url)
        url_name = url.split("/")[-1]
        with open("pict_parsed/" + url_name, "wb") as f:
            f.write(requests.get(url).content)
        da = datetime.now()
        self.small_img.save(
            os.path.basename(
                str(da.time()) + str(da.date()) + uuid.uuid4().hex + url_name
            ),
            File(open("pict_parsed/" + url_name, "rb")),
        )
        self.save()

    class Meta:
        abstract = True
