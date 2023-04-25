from django.contrib import admin
from django.urls import include, path, re_path
# from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.static import serve

urlpatterns = [
    path('',views.Homepages,name="Homepages"),
    path('about/',views.Aboutpage,name="Aboutpage"),
    path('contact/',views.Contactpage,name="Contactpage"),
    path('profile/',views.Profilepage,name="profilepage"),
    path('logout/',views.logout_page,name="logout_page"),
    path("business_field/",views.check_business_field,name="check_business_field"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
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
    path("profiles/",views.all_profile,name = "all_profile"),
    path("all_blogs/",views.all_blogs,name="all_blogs"),
    path("profile-completion-1/",views.ProfileCompletion1,name="NewProfile"),
    path("profile-completion-2/",views.ProfileCompletion2,name="NewProfile"),
    path("profile-completion-3/",views.ProfileCompletion3,name="NewProfile"),
    path('donate/',views.DonatePage,name="DonatePage"),
    path('success/',views.SuccessPage,name="SuccessPage"),
    path('cancle/',views.CanclePage,name="CanclePage"),
    path('complete-profile/',views.CompleteProfile,name="CompleteProfile"),
    path('filter-blog/',views.FilterData,name="FilterData"),
    path('search-blog/',views.BlogSearch,name="BlogSearch"),
    path('confirm-payment/',views.ConfirmPage,name="ConfirmPage"),
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)