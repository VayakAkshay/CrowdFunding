from django.contrib import admin
from django.urls import include, path, re_path
# from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Homepages,name="Homepages"),
    path('about/',views.Aboutpage,name="Aboutpage"),
    path('contact/',views.Contactpage,name="Contactpage"),
    path('profile/',views.Profilepage,name="profilepage"),
    path('logout/',views.logout_page,name="logout_page"),
    path("profile_type/",views.check_profile_type,name="check_profile_type"),
    path("about_me/",views.check_about_me,name="check_about_me"),
    path("plan_disc/",views.check_plan_disc,name="check_plan_disc"),
    path("business_field/",views.check_business_field,name="check_business_field"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("edit_desc/",views.edit_description,name="edit_description"),
    path("edit_plan/",views.edit_plan,name="edit_plan"),
    path("blogs/",views.Blog_page,name="Blog_page"),
    path("comment/",views.comment_handler,name="comment_handler"),
    path("learn/",views.Learn_page,name="Learn_page"),
    path("content-learn/",views.Learn_content,name="Learn_content"),
    path("blogs/borrower/",views.Borrower,name="Borrower"),
    path("blogs/investor/",views.Investor,name="Investor"),
    path("blogs/accouting/",views.Accounting,name="Accounting"),
    path("blogs/finance/",views.Finance,name="Finance"),
    path("blogs/economic/",views.Economic,name="Economic"),
    path("blogs/marketting/",views.Marketting,name="Marketting"),
    path("blogs/management/",views.Management,name="Management"),
    path("blogs/it/",views.IT,name="IT"),
    path("blogs/ib/",views.IB,name="IB"),
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)