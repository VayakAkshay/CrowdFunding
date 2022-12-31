from ast import Try
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ImageForm
from .models import Profile_data, Contact_data,Blog_data,Comment_data,Learn_data

def Homepages(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("pass")
        cpass = request.POST.get("cpass")
        if password == cpass:
            myuser = User.objects.create_user(email,mobile,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            full_name = fname + lname
            profile_data = Profile_data(full_name = full_name,email = email,mobile_no = mobile)
            profile_data.save()
            user = authenticate(username = email,password = password)
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/profile/")
        else:
            messages.warning(request,"Password is not matched ")
            return redirect("/password/")
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,'Homepage/index.html',{"username":user_name})
    except:
        return render(request,'Homepage/index.html')

def Aboutpage(request):
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,'Homepage/About.html',{"username":user_name})
    except:
        return render(request,'Homepage/About.html')

def Contactpage(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        message = request.POST.get("message")
        contact_data = Contact_data(first_name = fname,last_name = lname,email = email,message = message)
        contact_data.save()
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,'Homepage/contact.html',{"username":user_name})
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,'Homepage/contact.html',{"username":user_name})
    except:
        return render(request,'Homepage/contact.html')

def Profilepage(request):
    user = request.user
    profile_data_cat = Profile_data.objects.filter(email = user).first()
    fields_list = str(profile_data_cat).split(",")
    fields_list.pop(0)
    user_name = User.objects.get(username = user).first_name
    last_name = User.objects.get(username = user).last_name
    user_mobile = User.objects.get(username = user).email
    profile_data = Profile_data.objects.filter(email = user).values()
    blog_data = Blog_data.objects.filter(email_id = user).values()
    return render(request,"Homepage/profile.html",{"username":user_name,"last_name":last_name,"email":user,"mobile_number":user_mobile,"profile_data":profile_data,"fields_list":fields_list,"blog_data":blog_data})
    
def logout_page(request):
    logout(request)
    return redirect("/")

def check_profile_type(request):
    if request.method == "POST":
        profile_type = request.POST.get("profile_ans")
        user = request.user
        Profile_data.objects.filter(email = user).update(account_type = profile_type)
        return redirect("/profile/")
    return render(request, "Homepage/profile.html")


def check_about_me(request):
    if request.method == "POST":
        user = request.user
        about_text = request.POST.get("about_text")
        Profile_data.objects.filter(email = user).update(description = about_text)
        return redirect("/profile/")
    return render(request,"Homepage/profile.html")

def check_plan_disc(request):
    if request.method == "POST":
        user = request.user
        plan_disc = request.POST.get("plan_disc")
        Profile_data.objects.filter(email = user).update(business_plan = plan_disc)
        return redirect("/profile/")
    return render(request,"Homepage/profile.html")

def check_business_field(request):
    if request.method == "POST":
        fields = request.POST.get("checkbox_val")
        user = request.user
        Profile_data.objects.filter(email = user).update(business_category = fields)
        return redirect("/profile/")
    
    return render(request,"Homepage/profile.html")


def edit_profile(request):
    if request.method == "POST":
        user = request.user
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        full_name = fname + lname
        mobile = request.POST.get("mnumber")
        email = request.POST.get("email")
        Profile_data.objects.filter(email = user).update(full_name = full_name)
        Profile_data.objects.filter(email = user).update(mobile_no = mobile)
        User.objects.filter(username = user).update(first_name = fname)
        User.objects.filter(username = user).update(last_name = lname)
        User.objects.filter(username = user).update(email = mobile)
        Profile_data.objects.filter(email = user).update(email = email)
        User.objects.filter(username = user).update(username = email)
    return render(request,"Homepage/edit_profile.html")

def edit_description(request):
    if request.method == "GET":
        user = request.user
        Profile_data.objects.filter(email = user).update(description = "")
        return redirect("/profile/")
    return redirect("/profile/")

def edit_plan(request):
    if request.method == "GET":
        user = request.user
        Profile_data.objects.filter(email = user).update(business_plan = "")
        return redirect("/profile/")
    return redirect("/profile/")

def Blog_page(request):
    try:
        form = ImageForm()
        user = request.user
        comment_data = Comment_data.objects.all().values()
        blog_data = Blog_data.objects.all().values()
        profile_data = list(Profile_data.objects.filter(email = user).values())[0]["account_type"]
        business_category = list(Profile_data.objects.filter(email = user).values())[0]["business_category"]
        if profile_data != "" and business_category != "":
            blog = Blog_data()
            blog.blog_desc = request.POST.get("description")
            user_name = User.objects.get(username = user).first_name
            if request.method == "POST":
                blog.first_name = user_name
                blog.email_id = user
                blog.blog_category = profile_data
                blog.business_category = business_category
                if len(request.FILES) != 0:
                    blog.blog_img = request.FILES['blog_img']
                blog.save()
            form = ImageForm()
            return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blog_data,"comment_data":comment_data})
        else:
            user_name = User.objects.get(username = user).first_name
            messages.warning(request,"Please first complete your profile then start the blog")
            return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blog_data,"comment_data":comment_data})
    except:
        return render(request, "Homepage/blog.html")
def comment_handler(request):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment_data")
        blog_id = request.POST.get("post_id")
        user_name = User.objects.get(username = user).first_name
        comment_data = Comment_data(first_name = user_name,email_id = user,blog_id = blog_id, comment = comment)
        comment_data.save()
        return redirect("/blogs/")
    form = ImageForm()
    comment_data = Comment_data.objects.all().values()
    user = request.user
    user_name = User.objects.get(username = user).first_name
    blog_data = Blog_data.objects.all().values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blog_data,"comment_data":comment_data})

def Learn_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        content = request.POST.get("content")
        categories = request.POST.get("categories")
        learn_data = Learn_data(name = name,email_id = email,content = content,fields = categories)
        learn_data.save()
        return redirect("/learn/")
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        learn_data = Learn_data.objects.all().values()
        return render(request,"Homepage/learn.html",{"username":user_name,"learn_data":learn_data})
    except:
        learn_data = Learn_data.objects.all().values()
        return render(request,"Homepage/learn.html",{"learn_data":learn_data})

def Learn_content(request):
    if request.method == "POST":
        id = request.POST.get("id")
        learn_data = Learn_data.objects.filter(id = id).values()
        return render(request,"Homepage/learn_content.html",{"learn_data":learn_data})
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,"Homepage/learn_content.html",{"username":user_name})
    except:
        return redirect("/learn/")

def Borrower(request):
    blog_data = Blog_data.objects.filter(blog_category = "Borrower").values()
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all().values()
    user_name = User.objects.get(username = user).first_name
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blog_data,"comment_data":comment_data})

def Investor(request):
    blog_data = Blog_data.objects.filter(blog_category = "Investor").values()
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all().values()
    user_name = User.objects.get(username = user).first_name
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blog_data,"comment_data":comment_data})

def Management(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Management")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def Accounting(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Accounting")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def Economic(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Economic")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def Finance(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Finance")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def Marketting(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Marketting")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def IT(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("Information Technology")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})

def IB(request):
    blog_data = Blog_data.objects.all().values()
    business_cate = list(blog_data)
    id_set = set()
    for i in range(len(business_cate)):
        business_category = business_cate[i]["business_category"]
        finds = business_category.find("International Business")
        if(finds>=0):
            blogs = Blog_data.objects.filter(business_category = business_category).values()
            for i in range(len(list(blogs))):
                ids = list(blogs)[i]['id']
                id_set.add(ids)
    id_set = list(id_set)
    print(id_set)
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})