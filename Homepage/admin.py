from django.contrib import admin
from .models import Profile_data,Contact_data,Blog_data,Comment_data,Learn_data,DonationData

class Profile_dataAdmin(admin.ModelAdmin):
    list_display = ["full_name","email","mobile_no","account_type","business_category"]

class Contact_dataAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","email","message"]

class Blog_dataAdmin(admin.ModelAdmin):
    list_display = ["user_name","full_name","email_id","blog_category","business_category"]

class Comment_dataAdmin(admin.ModelAdmin):
    list_display = ["first_name","email_id","blog_id","comment"]

class Learn_dataAdmin(admin.ModelAdmin):
    list_display = ["name","email_id","content","fields"]

class DonationDataAdmin(admin.ModelAdmin):
    list_display = ["payment_id","amount"]

admin.site.register(Profile_data,Profile_dataAdmin)
admin.site.register(Contact_data,Contact_dataAdmin)
admin.site.register(Blog_data,Blog_dataAdmin)
admin.site.register(Comment_data,Comment_dataAdmin)
admin.site.register(Learn_data,Learn_dataAdmin)
admin.site.register(DonationData,DonationDataAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ["blog_id","blog_img"]