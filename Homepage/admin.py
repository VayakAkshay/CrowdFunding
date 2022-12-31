from django.contrib import admin
from .models import Profile_data,Contact_data,Blog_data,Comment_data,Learn_data
admin.site.register(Profile_data)
admin.site.register(Contact_data)
admin.site.register(Blog_data)
admin.site.register(Comment_data)
admin.site.register(Learn_data)

class ImageAdmin(admin.ModelAdmin):
    list_display = ["blog_id","blog_img"]