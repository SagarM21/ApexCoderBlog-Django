
from django import http
from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Blog,Contact,BlogComment
import math
# Create your views here.

def home(request):
    return render(request,'index.html')

def blog(request):
    no_of_posts = 3
    #if request.GET['pageno']:
    page = request.GET.get('page')
    if page is None:
        page=1
    else: 
        page=int(page)    
    #print(page)
    blogs = Blog.objects.all()
    length = len(blogs)
    #print(length)
    blogs = blogs[(page-1)*no_of_posts: page*no_of_posts]    #keeping 3 post on one page only[0,1,2 then 3,4,5]
    
    if page>1:
        prev = page-1
    else:
        prev=None
    
    if page<math.ceil(length/no_of_posts):  #page<last page number
        nxt = page+1
    else:
        nxt = None 
    #print(prev,nxt)                        
    context = {'blogs':blogs,'prev':prev,'nxt':nxt}
    return render(request,'bloghome.html',context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    comment = BlogComment.objects.filter(blog=blog,parent=None)
    replies = BlogComment.objects.filter(blog=blog).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)

    #print(comment,replies)
    #print(repDict)
    
    context={'blog':blog,'comment':comment,'user':request.user,'repDict':repDict}

    return render(request,'blogpost.html',context)

def search(request):
    query = request.GET['query']  
    if len(query)>80:
        blogs = Blog.objects.none()
    else:    
    #blogs=Blog.objects.all()
        blogsTitle=Blog.objects.filter(title__icontains=query)
        blogsContent=Blog.objects.filter(content__icontains=query)
        blogs = blogsTitle.union(blogsContent)

    if blogs.count() ==0:
        messages.warning(request, 'No search results found, Please refine your query.')   #this is not working..
    params = {'blogs':blogs,'query':query}
    return render(request,'search.html',params)

def contact(request):
    if request.method == 'POST':                 #if anybody enters the phone number his following details will be captured.
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        instance = Contact(name=name,email=email,phone=phone,desc=desc)
        instance.save()

    return render(request,'contact.html')

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']     #these '' names are taken from id of signup page in abse.html
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username)>10:
            messages.success(request,"Username must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.success(request,"Username should only contain letters and numbers")
            return redirect('home')

        if pass1!=pass2:
            messages.success(request,"Password's didn't matched.")
            return redirect('home')
        #create user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your ApexCoder account has been successfully created.")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']     #these '' names are taken from id of signup page in abse.html
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername,password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")   #messages are not working
            return redirect('home')
        else:    
            messages.error(request,"Invalid credentials")
            return redirect('home')
    return HttpResponse("404 - Not Found")


def handleLogout(request):
    
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('home')

def postComment(request,slug=None):
    if request.method=='POST':
        
        comment = request.POST.get("comment")
        user = request.user
        blogSno = request.POST.get("blogSno")
        blog = Blog.objects.get(sno=blogSno)
        parentSno = request.POST.get("parentSno")
       # blog = Blog.objects.get(sno=parentSno)    #parentsno is name tag of blogpost.html
       
        if parentSno == "":
            comment = BlogComment(comment=comment,user=user,blog=blog)
            comment.save()
            messages.success(request,"Your comment has been posted successfully!") 
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment,user=user,blog=blog,parent=parent)

            comment.save()
            messages.success(request,"Your reply has been posted successfully!") 
        return redirect(f"/blogpost/{blog.slug}")
    else:
        return HttpResponse("404 - Not Found")
        