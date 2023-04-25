from email.policy import default
from pyexpat import model
from statistics import mode
from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from PIL import Image

class Profile_data(models.Model):
    user_name = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 50,default = "")
    user_img = models.ImageField(upload_to="profile_images",default='static/images/user-icon.png')
    email = models.EmailField(max_length = 100,default = "")
    mobile_no = PhoneField(blank=True, help_text='Contact phone number',default=0)
    account_type = models.CharField(max_length=50,default="")
    description = models.CharField(max_length = 5000,default="")
    business_category = models.CharField(max_length = 200,default="")
    def __str__(self):
        return self.full_name + self.business_category


class Contact_data(models.Model):
    message_id = models.AutoField
    first_name = models.CharField(max_length = 50,default = "")
    last_name = models.CharField(max_length = 50,default="")
    email = models.EmailField(max_length = 50,default="")
    message  = models.CharField(max_length = 5000,default="")

    def __str__(self):
        return self.email
    
class Blog_data(models.Model):
    blog_id = models.AutoField
    user_name = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    full_name = models.TextField(max_length=50, default="")
    email_id = models.EmailField(max_length = 50,default="")
    blog_desc = models.CharField(max_length=5000,default="")
    blog_img = models.ImageField(upload_to="blog_img")
    blog_category = models.CharField(max_length=100,default="")
    business_category = models.CharField(max_length = 200,default="")

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.blog_img.path)


class Comment_data(models.Model):
    comment_id = models.AutoField
    first_name = models.CharField(max_length=50, default="")
    email_id = models.EmailField(max_length = 50,default="")
    blog_id = models.IntegerField(default=0)
    comment = models.CharField(max_length=500,default="")

    def __str__(self):
        return self.first_name + " - " + self.comment[:15] + "..."
    
class Learn_data(models.Model):
    learn_id = models.AutoField
    name = models.CharField(max_length=50, default="")
    email_id = models.EmailField(max_length = 50,default="")
    content = models.CharField(max_length=10000,default="")
    fields = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.name


class DonationData(models.Model):
    payment_id = models.TextField(max_length=500,default="")
    amount = models.IntegerField(default=0)