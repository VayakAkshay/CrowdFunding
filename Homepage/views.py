from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ImageForm
from .models import Profile_data, Contact_data,Blog_data,Comment_data,Learn_data,DonationData
import razorpay

def Homepages(request):
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
        messages.success(request,"You message successfully sent!!")
        return render(request,'Homepage/contact.html',{"username":user_name})
    try:
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,'Homepage/contact.html',{"username":user_name})
    except:
        return render(request,'Homepage/contact.html')

def Profilepage(request):
    if request.user.is_authenticated:
        profiles_datas = Profile_data.objects.filter(user_name = request.user).values()[0]
        if request.method == "POST":
            fields = request.POST.get("checkbox_val")
            user = request.user
            Profile_data.objects.filter(user_name = request.user).update(business_category = fields)
            return redirect("/profile/")
        if len(profiles_datas["account_type"])==0:
            return redirect("/profile-completion-1/")
        elif len(profiles_datas["description"]) == 0:
            return redirect("/profile-completion-2/")
        elif len(profiles_datas["business_category"])==0:
            return redirect("/profile-completion-3/")
        else:
            more_btn = 1
            user = request.user
            profile_data_cat = Profile_data.objects.filter(user_name = request.user).values()[0]["business_category"]
            fields_list = str(profile_data_cat).split(",")
            user_name = User.objects.get(username = user).first_name
            last_name = User.objects.get(username = user).last_name
            user_mobile = User.objects.get(username = user).email
            profile_data = Profile_data.objects.filter(email = user).values()
            blog_data = Blog_data.objects.filter(email_id = user).values()
            limited_blog_data = Blog_data.objects.filter(email_id = user).all()[:3]
            comment_data = Comment_data.objects.all().values()
            return render(request,"Homepage/profile.html",{"username":user_name,"last_name":last_name,"email":user,"mobile_number":user_mobile,"profile_data":profile_data,"fields_list":fields_list,"blog_data":blog_data,"limited_blog_data":limited_blog_data,"more_btn":more_btn,"comment_data":comment_data})
    else:
        return redirect("/login/")
    

def all_profile(request):
    user = request.user
    try:
        if request.method == "POST":
            email_id = request.POST.get("email_id")
            profile_data = Profile_data.objects.filter(email = email_id).values()
            user = request.user
            profile_data_cat = Profile_data.objects.filter(email = email_id).values()[0]["business_category"]
            fields_list = str(profile_data_cat).split(",")
            user_name = User.objects.get(username = user).first_name
            last_name = User.objects.get(username = user).last_name
            user_mobile = User.objects.get(username = user).email
            blog_data = Blog_data.objects.filter(email_id = email_id).values()
            mydata = []
            for i in blog_data:
                mydic = {}
                user_name = i["user_name_id"]
                mydic["id"] = i["id"]
                mydic["user_img"] = Profile_data.objects.filter(user_name = user_name).values()[0]["user_img"]
                mydic["full_name"] = i["full_name"]
                mydic["blog_desc"] = i["blog_desc"]
                mydic["blog_img"] = i["blog_img"]
                mydic["blog_category"] = i['blog_category']
                mydic["business_category"] = i["business_category"]
                mydic["email_id"] = i["email_id"]
                mydata.append(mydic)
            limited_blog_data = Blog_data.objects.filter(email_id = user).all()[:3]
            comment_data = Comment_data.objects.all().values()
            return render(request,"Homepage/profiles.html",{"username":user_name,"last_name":last_name,"email":user,"mobile_number":user_mobile,"profile_data":profile_data,"fields_list":fields_list,"blog_data":mydata,"limited_blog_data":limited_blog_data,"comment_data":comment_data})
    except:
        messages.warning(request,"Something went wrong")
        return redirect("/blogs/")


def ProfileCompletion1(request):
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
            user = authenticate(username = email,password = password)
            login(request,user)
            full_name = fname + " " + lname
            profile_data = Profile_data(user_name = request.user,full_name = full_name,email = email,mobile_no = mobile)
            profile_data.save()
            return render(request,"Homepage/profile-completion-1.html")
        else:
            messages.warning(request,"Password is not matched ")
            return redirect("/password/")
    return render(request,"Homepage/profile-completion-1.html")

def ProfileCompletion2(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            profile_type = request.POST.get("profile_ans")
            user = request.user
            Profile_data.objects.filter(email = user).update(account_type = profile_type)
            return redirect("/profile-completion-2/")
        return render(request,"Homepage/profile-completion-2.html")
    else:
        return redirect("/regester/")

def ProfileCompletion3(request):
    if request.user.is_authenticated:
        user = request.user
        profile_datas = Profile_data.objects.filter(user_name = request.user).values()[0]
        full_name = profile_datas["full_name"]
        email = profile_datas['email']
        mobile_no = profile_datas["mobile_no"]
        account_type = profile_datas["account_type"]
        if request.method == "POST":
            Profile_data.objects.filter(user_name = request.user).delete()
            my_profile_data = Profile_data()
            my_profile_data.user_name = request.user
            my_profile_data.full_name = full_name
            my_profile_data.email = email
            my_profile_data.mobile_no = mobile_no
            my_profile_data.account_type = account_type
            if len(request.FILES) != 0:
                my_profile_data.user_img = request.FILES['profile-img']
            about_text = request.POST.get("about_text")
            my_profile_data.description = about_text
            my_profile_data.save()
            return redirect("/profile-completion-3/")
        return render(request,"Homepage/profile-completion-3.html")
    else:
        return redirect('/regester/')

def CompleteProfile(request):
    return render(request,"Homepage/complete-profile.html")

def check_business_field(request):
    if request.method == "POST":
        fields = request.POST.get("checkbox_val")
        user = request.user
        Profile_data.objects.filter(email = user).update(business_category = fields)
        return redirect("/profile/")
    return render(request,"Homepage/profile.html")

def edit_profile(request):
    user = request.user
    desc = Profile_data.objects.filter(email = user).values()[0]["description"]
    if request.method == "POST":
        user = request.user
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        full_name = fname + lname
        mobile = request.POST.get("mnumber")
        email = request.POST.get("email")
        aboutme = request.POST.get("aboutme")
        Profile_data.objects.filter(email = user).update(full_name = full_name)
        Profile_data.objects.filter(email = user).update(mobile_no = mobile)
        Profile_data.objects.filter(email = user).update(description = aboutme)
        User.objects.filter(username = user).update(first_name = fname)
        User.objects.filter(username = user).update(last_name = lname)
        User.objects.filter(username = user).update(email = mobile)
        Profile_data.objects.filter(email = user).update(email = email)
        User.objects.filter(username = user).update(username = email)
        return redirect("/profile/")
    return render(request,"Homepage/edit_profile.html",{"desc":desc})


def Blog_page(request):
    if request.user.is_authenticated:
        try:
            form = ImageForm()
            user = request.user
            comment_data = Comment_data.objects.all().values()
            blog_data = Blog_data.objects.all().values()
            profile_data = list(Profile_data.objects.filter(email = user).values())[0]["account_type"]
            business_category = list(Profile_data.objects.filter(email = user).values())[0]["business_category"]
            if profile_data != "" and business_category != "":
                blog = Blog_data()
                if request.method == "POST":
                    blog.blog_desc = request.POST.get("description")
                    blog.full_name = request.user.first_name + " " + request.user.last_name
                    blog.email_id = user
                    blog.blog_category = profile_data
                    blog.business_category = business_category
                    blog.user_name = request.user
                    if len(request.FILES) != 0:
                        blog.blog_img = request.FILES['blog_img']
                    blog.save()
                    messages.success(request,"Your post successfully added")
                    return redirect("/blogs/")
                form = ImageForm()
                mydata = []
                for i in blog_data:
                    mydic = {}
                    user_name = i["user_name_id"]
                    mydic["id"] = i["id"]
                    mydic["user_img"] = Profile_data.objects.filter(user_name = user_name).values()[0]["user_img"]
                    mydic["full_name"] = i["full_name"]
                    mydic["blog_desc"] = i["blog_desc"]
                    mydic["blog_img"] = i["blog_img"]
                    mydic["blog_category"] = i['blog_category']
                    mydic["business_category"] = i["business_category"]
                    mydic["email_id"] = i["email_id"]
                    mydata.append(mydic)
                profile_img = Profile_data.objects.filter(user_name = request.user).values()[0]["user_img"]
                user_name = User.objects.get(username = user).first_name
                return render(request,"Homepage/blog.html",{"form":form,"blog_data":mydata,"comment_data":comment_data,"profile_img":profile_img})
            else:
                user_name = User.objects.get(username = user).first_name
                profile_img = Profile_data.objects.filter(user_name = request.user).values()[0]["user_img"]
                messages.warning(request,"Please first complete your profile then start the blog")
                return render(request,"Homepage/blog.html",{"form":form,"blog_data":blog_data,"comment_data":comment_data,"profile_img":profile_img})
        except:
            form = ImageForm()
            user = request.user
            user_name = User.objects.get(username = user).first_name
            comment_data = Comment_data.objects.all().values()
            blog_data = Blog_data.objects.all().values()
            profile_img = Profile_data.objects.filter(user_name = request.user).values()[0]["user_img"]
            return render(request, "Homepage/blog.html",{"form":form,"blog_data":blog_data,"comment_data":comment_data,"profile_img":profile_img})
    else:
        return render(request, "Homepage/blog.html")
    
from django.db.models import Q

def FilterData(request):
    if request.method == "POST":
        categories = request.POST.get("categories")
        cat_list = categories.split(",")[1:]
        new_list = [a for a in cat_list if a != ""]
        if "All" in new_list:
            filtered_objects = Blog_data.objects.all().values()
        else:
            filtered_objects = [Blog_data.objects.filter(Q(blog_category__contains=term) | Q(business_category__contains=term)).all().values() for term in new_list]
            filtered_objects = filtered_objects[0]

        user = request.user
        form = ImageForm()
        user_name = User.objects.get(username = user).first_name
        comment_data = Comment_data.objects.all().values()
        profile_img = Profile_data.objects.filter(user_name = request.user).values()[0]["user_img"]

        if filtered_objects.exists():
            mydata = []
            for i in filtered_objects:
                mydic = {}
                user_name = i["user_name_id"]
                mydic["id"] = i["id"]
                mydic["user_img"] = Profile_data.objects.filter(user_name = user_name).values()[0]["user_img"]
                mydic["full_name"] = i["full_name"]
                mydic["blog_desc"] = i["blog_desc"]
                mydic["blog_img"] = i["blog_img"]
                mydic["blog_category"] = i['blog_category']
                mydic["business_category"] = i["business_category"]
                mydic["email_id"] = i["email_id"]
                mydata.append(mydic)

            return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":mydata,"comment_data":comment_data,"profile_img":profile_img})
        else:
            messages.warning(request,"Not Found")
            return redirect("/blogs/")
    return redirect("/blogs/")


def BlogSearch(request):
    if request.method == "POST":
        search_data = request.POST.get("search_data")
        filtered_objects = Blog_data.objects.filter(Q(full_name__contains=search_data) | Q(blog_desc__contains=search_data)).all().values()
        user = request.user
        form = ImageForm()
        user_name = User.objects.get(username = user).first_name
        comment_data = Comment_data.objects.all().values()
        profile_img = Profile_data.objects.filter(user_name = request.user).values()[0]["user_img"]
        mydata = []
        for i in filtered_objects:
            mydic = {}
            user_name = i["user_name_id"]
            mydic["id"] = i["id"]
            mydic["user_img"] = Profile_data.objects.filter(user_name = user_name).values()[0]["user_img"]
            mydic["full_name"] = i["full_name"]
            mydic["blog_desc"] = i["blog_desc"]
            mydic["blog_img"] = i["blog_img"]
            mydic["blog_category"] = i['blog_category']
            mydic["business_category"] = i["business_category"]
            mydic["email_id"] = i["email_id"]
            mydata.append(mydic)
        return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":mydata,"comment_data":comment_data,"profile_img":profile_img}) 
    return redirect("/blogs/")


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
        messages.success(request,"Learn Data Added Successfully")
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

KEY = "rzp_test_97C8g6tQO77gec"
SECRET = "NwqOGIJaaAN45lHmGyrOAClO"

def DonatePage(request):
    amount = 500 * 100
    clint = razorpay.Client(auth=(KEY,SECRET))
    payment_order = clint.order.create({'amount':amount,"currency":"INR","payment_capture":'1'})
    order_id = payment_order["id"]
    return render(request,"Homepage/donate.html",{"api_key":KEY,"order_id":order_id})


def ConfirmPage(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100
        normal_amount = request.POST.get("amount")
        clint = razorpay.Client(auth=(KEY,SECRET))
        payment_order = clint.order.create({'amount':amount,"currency":"INR","payment_capture":'1'})
        order_id = payment_order["id"]
        return render(request,"Homepage/confirm_payment.html",{"api_key":KEY,"order_id":order_id,"normal_amount":normal_amount,"amount":amount})
    else:
        return redirect("/donate/")

def SuccessPage(request):
    amount = request.POST.get("amount")
    client = razorpay.Client(auth=(KEY, SECRET))
    payment = client.payment.fetch(request.POST.get("razorpay_payment_id"))
    order_id = request.POST.get("razorpay_payment_id")
    print(order_id)

    if payment["amount"]:
        donatedata = DonationData(payment_id = order_id,amount = amount)
        donatedata.save()
        return render(request,"Homepage/success.html")
    else:
        messages.warning(request,"Payment is not successfull")
        return redirect("/donate/")

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
    user = request.user
    form = ImageForm()
    comment_data = Comment_data.objects.all()
    user_name = User.objects.get(username = user).first_name
    blogs = Blog_data.objects.filter(id__in = id_set).values()
    return render(request,"Homepage/blog.html",{"username":user_name,"form":form,"blog_data":blogs,"comment_data":comment_data})


def all_blogs(request):
    try:
        more_btn = 1
        if request.method == "POST":
            more_btn = 0
            email = request.POST.get("email")
            limited_blog_data = Blog_data.objects.filter(email_id = email).all()
            user = request.user
            profile_data_cat = Profile_data.objects.filter(email = user).first()
            fields_list = str(profile_data_cat).split(",")
            fields_list.pop(0)
            user_name = User.objects.get(username = user).first_name
            last_name = User.objects.get(username = user).last_name
            user_mobile = User.objects.get(username = user).email
            profile_data = Profile_data.objects.filter(email = user).values()
            blog_data = Blog_data.objects.filter(email_id = user).values()
            limited_blog_data = Blog_data.objects.filter(email_id = user).all()
            return render(request,"Homepage/profile.html",{"username":user_name,"last_name":last_name,"email":user,"mobile_number":user_mobile,"profile_data":profile_data,"fields_list":fields_list,"blog_data":blog_data,"limited_blog_data":limited_blog_data,"more_btn":more_btn})
    except:
        return redirect("/profile/")



def CanclePage(request):
    return render(request,"Homepage/cancle.html")


def logout_page(request):
    logout(request)
    messages.success(request,"You are logged out successfully!!")
    return redirect("/")