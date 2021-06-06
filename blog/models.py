from math import trunc
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    desc = models.TextField()  
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    sno =models.AutoField(primary_key = True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "... " + "by " + self.user.username