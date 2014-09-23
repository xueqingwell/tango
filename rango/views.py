# Create your views here.
#coding:UTF-8
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from rango.models import Category,Page
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

def encode_url(str):
    return str.replace(' ','_')

def decode_url(str):
    return str.replace('_',' ')

@login_required
def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[0:5]
    page_list = Page.objects.order_by('-views')[0:5]
    context_dict = {'categories': category_list}
    context_dict['pages']=page_list
    for category in category_list:
        category.url = category.name.replace(' ','_')
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    return render_to_response('rango/about.html', context)

def category(request,category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_',' ')
    context_dict={'category_name':category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
        context_dict['category_name_url']=encode_url(category_name)
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html',context_dict,context)

def add_category(request):
    context = RequestContext(request)
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render_to_response('rango/add_category.html',{'form':form},context)

@login_required
def add_page(request,category_name_url):
    context= RequestContext(request)
    category_name=decode_url(category_name_url)

    if request.method == 'POST':
        form=PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            try:
                cat = Category.objects.get(name = category_name)
                page.category  = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html',{},context)
            page.views = 0
            page.save()
            return category(request,category_name_url)
        else:

            print form.errors
            return HttpResponse(form.errors)
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',{'category_name_url':category_name_url,'category_name':category_name,'form':form},context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method =='POST':

        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #处理用户账号信息
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #处理用户profile
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()

            registered=True

        else:
            print user_form.errors,profile_form.errors
    else:
        user_form = UserForm()
        profile_form=UserProfileForm()

    return render_to_response(
        'rango/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered},context
    )

def user_login(request):
    context = RequestContext(request)

    if request.method=='POST':
        print "login...."
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled')
        else:
            print 'Invalid login details:{0},{1}'.format(username,password)
            return HttpResponse('Invalid login details supplied')
    else:
        return render_to_response('rango/login.html',{},context)

@login_required
def restricated(request):
    context=RequestContext(request)
    return render_to_response('rango/restricted.html',{},context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
























