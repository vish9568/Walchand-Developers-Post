from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm, ImageUpload,AddProject
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import  HttpResponse
from django.shortcuts import redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random

def getRandom():
    return random.randint(1000, 9999)

l = []
def get_guides():
    l.clear()
    guides = Guide.objects.all()
    for guide in guides:
        l.append(guide.name)
    l.append("Other")

years = []
guides = []
project_sems = []
batches = []

def get_filters(params):
    project1 = Project.objects.order_by('year').values('year').distinct()
    years.clear()
    for i in project1:
        if(i['year']):
            years.append(i['year'])

    project2 = Project.objects.order_by('guide').values('guide').distinct()
    guides.clear()
    for i in project2:
        if(i['guide']):
            guides.append(i['guide'])

    project3 = Project.objects.order_by('sem').values('sem').distinct()
    project_sems.clear()
    for i in project3:
        if(i['sem']):
            project_sems.append(i['sem'])

    project4 = Project.objects.order_by('batch').values('batch').distinct()
    batches.clear()
    for i in project4:
        if(i['batch']):
            batches.append(i['batch'])

    params['years'] = years
    params['guides'] = guides
    params['batches'] = batches
    params['sems'] = project_sems








def display_projects(request):
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        tmp_dict ={}
        tmp_dict['id'] = project.id
        tmp_dict['name'] = project.name
        tmp_dict['tagline'] = project.tag_line
        tmp_dict['photo'] = project.photo
        project_list.append(tmp_dict)
    opt = 0
    params = {'projects' : project_list,'opt': opt,'info': 'top projects'}
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
        except:
            pass
    else:
        params['my_template'] = 'basic.html'
    # for p in params['projects']:
    #     print(p)
    get_filters(params)
    return render(request,"DisplayProjects.html",params)

def homepage(request):
    params = {}
    get_filters(params)
    print(years)
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)

        except:
            pass
        # print(params)
    else:
        params['my_template'] = 'basic.html'

    return render(request,'Homepage.html',params)


def single_project(request,id,slug):
    print(id)
    project = Project.objects.get(id = id)

    project_info = {}
    project_info['name'] = project.name.capitalize()
    project_info['tag_line'] = project.tag_line
    project_info['photo'] = project.photo
    project_info['year'] = project.year
    project_info['sem'] = project.sem
    project_info['batch'] = project.batch
    project_info['domain'] = project.domain
    project_info['guide'] =project.guide
    project_info['inspiration'] = project.inspiration
    project_info['what_it_does'] = project.what_it_does
    project_info['how_we_build'] = project.how_we_build
    project_info['challenges'] = project.challenges
    project_info['accomplishment'] = project.accomplishment
    project_info['we_learned'] = project.we_learned
    project_info['whats_next'] = project.whats_next
    project_info['github'] = project.github
    project_info['hosted'] = project.hosted
    # print(project_info)
    params = {'project' : project_info}
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
        except:
            pass


    else:
        params['my_template'] = 'basic.html'
    get_filters(params)
    return render(request,'Project.html',params)


def search(request):
    query = request.GET.get('search')
    query = query.lower()

    projects = Project.objects.all()
    # print(projects)



    project_list = []
    name = []
    year = []
    domain = []
    guide = []
    for project in projects:
        if query in project.name.lower() or query in project.domain.lower() or query == str(project.year).lower() or query in project.guide.lower():
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['name'] = project.name
            tmp_dict['tagline'] = project.tag_line
            tmp_dict['photo'] = project.photo
            tmp_dict['domain'] = project.domain
            tmp_dict['guide'] = project.guide

            if query in project.name.lower():
                name.append(tmp_dict)

            if query in project.domain.lower():
                domain.append(tmp_dict)

            if query == str(project.year).lower():
                year.append(tmp_dict)

            if query in project.guide.lower():
                guide.append(tmp_dict)


    if len(name) > 4:
        name = name[:4]

    if len(domain) > 4:
        domain = domain[:4]

    if len(year) > 4:
        year = year[:4]

    if len(guide) > 4:
        guide = guide[:4]





    params = {'name': name, 'domain': domain, 'year': year, 'guide' : guide, 'search': query}
    if len(name) is 0 and len(domain) is 0 and len(year) is 0 and len(guide) is 0:
        params['msg'] = 'no'

    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
        except:
            pass
    else:
        params['my_template'] = 'basic.html'
    # for p in params['projects']:
    #     print(p)
    get_filters(params)
    return render(request, "SearchResult.html", params)

def view_search(request,heading,search):
    projects = Project.objects.all()
    project_list = []
    print(heading,search)
    info = ''
    for project in projects:
        if heading == 'name' and search.lower() in project.name.lower():
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['name'] = project.name
            tmp_dict['tagline'] = project.tag_line
            tmp_dict['photo'] = project.photo
            project_list.append(tmp_dict)
            info = 'projects with name ' + search

        elif heading == 'domain' and search.lower() in project.domain.lower():
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['name'] = project.name
            tmp_dict['tagline'] = project.tag_line
            tmp_dict['photo'] = project.photo
            project_list.append(tmp_dict)
            info = 'projects built with ' + search

        elif heading == 'guide' and search.lower() in project.guide.lower():
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['name'] = project.name
            tmp_dict['tagline'] = project.tag_line
            tmp_dict['photo'] = project.photo
            project_list.append(tmp_dict)
            info = 'projects done under ' + search

        elif heading == 'year' and search.lower() == str(project.year).lower():
            tmp_dict = {}
            tmp_dict['id'] = project.id
            tmp_dict['name'] = project.name
            tmp_dict['tagline'] = project.tag_line
            tmp_dict['photo'] = project.photo
            project_list.append(tmp_dict)
            info = 'projects built in ' + search

    opt = 0
    params = {'projects': project_list, 'opt': opt, 'info':info}
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
        except:
            pass
    else:
        params['my_template'] = 'basic.html'
    # for p in params['projects']:
    #     print(p)
    get_filters(params)
    return render(request, "DisplayProjects.html", params)


def filters(request):
    params = {}
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                params['profile'] = student.photo
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                params['profile'] = guide.photo
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
        except:
            pass
        # print(params)
    else:
        params['my_template'] = 'basic.html'

    year = request.POST.getlist("year[]")
    sem = request.POST.getlist("sem[]")
    batch = request.POST.getlist("batch[]")
    guide = request.POST.getlist("guide[]")
    # print(type(year[0]))
    # print(year,sem,batch,guide)
    query = 'select * from demo_project where 1=1'
    if len(year) > 0:
        query += ' and year in ('
        for y in year:
            query += y + ','
        st = query[:-1] + ')'
        query = st

    if len(batch) > 0:
        query += ' and batch in ('
        for b in batch:
            query += "'" + b + "'" + ','
        st = query[:-1] + ')'
        query = st

    if len(guide) > 0:
        query += ' and guide in ('
        for g in guide:
            query +="'" + g + "'" + ','
        st = query[:-1] + ')'
        query = st

    if len(sem) > 0:
        query += ' and sem in ('
        for s in sem:
            query += "'" + s + "'" + ','
        st = query[:-1] + ')'
        query = st

    # print(query)



    projects = Project.objects.raw(query)
    project_list = []
    for project in projects:
        tmp_dict = {}
        tmp_dict['id'] = project.id
        tmp_dict['name'] = project.name
        tmp_dict['tagline'] = project.tag_line
        tmp_dict['photo'] = project.photo
        project_list.append(tmp_dict)


    params['projects'] = project_list
    if len(project_list) == 0:
        params['info'] = 'No records'
    else:
        params['info'] = 'Records'
    get_filters(params)
    return render(request, 'DisplayProjects.html', params)


# def login(request):
#     if request.method == 'POST':
#         return HttpResponse("Post")
#     return HttpResponse("Gandal")

# def sign_up(request):
#     if request.method=="POST":
#         fm=SignUpForm(request.POST)
#         if fm.is_valid():
#             messages.success(request,'Account Created Successfully !!')
#             fm.save()
#             email = fm.cleaned_data['email']
#             username = fm.cleaned_data['username']
#             password = fm.cleaned_data['password1']
#             first_name = fm.cleaned_data['first_name']
#             last_name = fm.cleaned_data['last_name']
#             # print(email,username,password,first_name,last_name)
#             student = Student(username = username,name = first_name+" "+last_name, mail = email, password = password)
#             student.save()
#     else:
#         fm=SignUpForm()
#
#     return render(request,'signup1.html',{'form':fm})
#
#
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    try:
                        student = Student.objects.get(username=uname)
                        if student is not None:
                            login(request, user)
                            messages.success(request,'Logged in successfully !!')
                            if(student.verified==False):
                                # updting otp
                                Student.objects.filter(username = uname).update(otp = getRandom())
                                return HttpResponseRedirect('/verification/')
                            else:
                                # return redirect(request.META['HTTP_REFERER'])
                                return HttpResponseRedirect('/profile/')
                    except:
                        pass
                    try:
                        guide = Guide.objects.get(username=uname)
                        if guide is not None:
                            login(request, user)
                            messages.success(request, 'Logged in successfully !!')
                            if (guide.verified == False):
                                # updting otp
                                Guide.objects.filter(username=uname).update(otp=getRandom())
                                return HttpResponseRedirect('/verification/')
                            else:
                                # return redirect(request.META['HTTP_REFERER'])
                                return HttpResponseRedirect('/profile/')
                    except:
                        pass
                else:
                    return HttpResponseRedirect('/sign_up/')
        else:
            fm=AuthenticationForm()
        #fm=AuthenticationForm()
        return render(request,'StuLogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')
#
# def stu_verification(request):
#     if request.user.is_authenticated:
#
#         student = Student.objects.get(username=request.user)
#
#         subject = 'Account Verification'
#         message = f'Hi ,Your OTP for verification is {student.otp}'
#         email_from = 'medicatorvs@gmail.com'
#         recipient_list = [str(request.user.email), ]
#         send_mail(subject, message, email_from, recipient_list)
#         print(student.otp)
#         return render(request,'verification.html',{'name':request.user,'email':request.user.email,'msg':None})
#     else:
#         return HttpResponseRedirect('/login/')

def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account Created Successfully !!')
            fm.save()
            email = fm.cleaned_data['email']
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password1']
            first_name = fm.cleaned_data['first_name']
            last_name = fm.cleaned_data['last_name']
            # print(email,username,password,first_name,last_name)
            # Remember to change to student
            student = Student(username = username,name = first_name+" "+last_name, mail = email, password = password)
            student.save()
    else:
        fm=SignUpForm()

    return render(request,'signup1.html',{'form':fm})


# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method=='POST':
#             fm=AuthenticationForm(request=request,data=request.POST)
#             if fm.is_valid():
#                 uname=fm.cleaned_data['username']
#                 upass=fm.cleaned_data['password']
#                 user = authenticate(username=uname,password=upass)
#                 if user is not None:
#                     guide = Guide.objects.get(username=uname)
#                     login(request, user)
#                     messages.success(request,'Logged in successfully !!')
#                     if(guide.verified==False):
#                         # updting otp
#                         Guide.objects.filter(username = uname).update(otp = getRandom())
#                         return HttpResponseRedirect('/verification/')
#                     else:
#                         # return redirect(request.META['HTTP_REFERER'])
#                         return HttpResponseRedirect('/profile/')
#         else:
#             fm=AuthenticationForm()
#         #fm=AuthenticationForm()
#         return render(request,'StuLogin.html',{'form':fm})
#     else:
#         return HttpResponseRedirect('/profile/')

def stu_verification(request):
    if request.user.is_authenticated:

        student = Guide.objects.get(username=request.user)

        # subject = 'Account Verification'
        # message = f'Hi ,Your OTP for verification is {student.otp}'
        # email_from = 'medicatorvs@gmail.com'
        # recipient_list = [str(request.user.email), ]
        # send_mail(subject, message, email_from, recipient_list)
        print(student.otp)
        return render(request,'verification.html',{'name':request.user,'email':request.user.email,'msg':None})
    else:
        return HttpResponseRedirect('/login/')

def verify_otp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            # print(otp)
            student = Student.objects.get(username = request.user)

            if(str(student.otp) == otp):
                # print("Jamal")
                Student.objects.filter(username = request.user).update(verified = True)
                return HttpResponseRedirect('/profile/')
            else:
                return render(request,'verification.html',{'name':request.user,'email':request.user.email,'msg':"Entered Wrong OTP ,please enter correct OTP"})
    else:
        return HttpResponseRedirect('/login/')

# def verify_otp(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             otp = request.POST.get('otp')
#             # print(otp)
#             student = Student.objects.get(username = request.user)
#
#             if(str(student.otp) == otp):
#                 # print("Jamal")
#                 Student.objects.filter(username = request.user).update(verified = True)
#                 return HttpResponseRedirect('/profile/')
#             else:
#                 return render(request,'verification.html',{'name':request.user,'email':request.user.email,'msg':"Entered Wrong OTP ,please enter correct OTP"})
#     else:
#         return HttpResponseRedirect('/login/')

def user_profile(request):

    if request.user.is_authenticated:
         try:
            student = Student.objects.get(username=request.user)
            if student is not None:
                if (student.verified == False):
                    Student.objects.filter(username=request.user).update(otp=getRandom())
                    return HttpResponseRedirect('/verification/')

                return render(request, 'profile.html', {'name': request.user, 'profile': student.photo,'my_template':'basic2.html'})
         except:
             pass
         try:
            guide = Guide.objects.get(username=request.user)

            if (guide.verified == False):
                Guide.objects.filter(username=request.user).update(otp=getRandom())
                return HttpResponseRedirect('/verification/')
            projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)

            return render(request, 'profile.html', {'name': request.user, 'profile': guide.photo,'my_template':'basic3.html','notification':len(projects)})
            # return render(request, 'profile.html', {'name': request.user, 'profile': guide.photo,'my_template':'basic3.html'})
         except:
             pass



    else:
        return HttpResponseRedirect('/login/')



def settings(request):
    params = {}
    # if request.method == 'POST':
    #     image_upload = ImageUpload(request.POST,request.FILES)
    #     if image_upload.is_valid():
    #         image_upload.save()
    #         photo = image_upload.cleaned_data['photo']
    #         print(photo)
    #         photo = '/media/tmp/' + str(photo)
    #         Student.objects.filter(username = request.user).update(photo = photo)
    #     else:
    #         image_upload = ImageUpload()

    if request.user.is_authenticated:
        # image_upload = ImageUpload()
        params['my_template'] = 'basic2.html'
        get_filters(params)
        try:
            student = Student.objects.get(username = request.user)
            if student is not  None:
                name = student.name
                li = name.split()
                first_name = li[0]
                last_name = li[1]
                params['profile'] = student.photo
                params['first_name'] = first_name
                params['last_name'] = last_name
                params['github'] = student.github
                params['linkedin'] = student.linked_in
                # params['form'] = image_upload
                return render(request, 'Settings.html', params)
        except:
            pass
        try:
            # params['my_template'] = 'basic3.html'
            params['my_template'] = 'basic3.html'
            guide = Guide.objects.get(username=request.user)
            print(guide)
            if guide is not None:
                name = guide.name
                li = name.split()
                first_name = li[0]
                last_name = li[1]
                params['profile'] = guide.photo
                params['first_name'] = first_name
                params['last_name'] = last_name
                # print(guide.github,guide.linked_in)
                # params['form'] = image_upload
                if guide.github is not None:
                    params['github'] = guide.github
                if guide.linked_in is not  None:
                    params['linkedin'] = guide.linked_in
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
                return render(request, 'Settings.html', params)



        except:
            pass


        # print(params)
    else:
        return HttpResponseRedirect('/login/')



def save_changes(request):
    params = {}
    get_filters(params)
    if request.user.is_authenticated:
        if request.method == 'POST':
            pic = request.POST.get("image")
            print("---------------------------------------",pic)
            name = request.POST.get('first_name')
            name += " " + request.POST.get('last_name')
            github = request.POST.get('github')
            linkedin = request.POST.get('linkedin')
            Student.objects.filter(username=request.user).update(name = name, github = github, linked_in = linkedin)
            return HttpResponseRedirect('/settings/')
        # print(params)
    else:
        return HttpResponseRedirect('/login/')

    return render(request, 'Settings.html', params)

def portfolio(request):
    params = {}
    get_filters(params)
    if request.user.is_authenticated:
        params['my_template'] = 'basic2.html'
        try:
            student = Student.objects.get(username=request.user)
            print(student)
            if student is not None:
                projects = Project.objects.filter(project_student__student_id=student)
                # print(projects)
                project_list = []

                for project in projects:
                    dict = {}

                    # print(p)
                    dict['id'] = project.id
                    dict['photo'] = project.photo
                    dict['name'] = project.name
                    dict['tag_line'] = project.tag_line
                    dict['verified'] = project.verified
                    project_list.append(dict)

                params['projects'] = project_list
                if student.photo:
                    params['profile'] = student.photo
                else:
                    params['profile'] = "../media/Profile1.jpg"
                params['name'] = student.name
                params['username'] = student.username
                params['len'] = len(projects)
                return render(request, 'Portfolio.html', params)
        except:
            pass
        try:
            guide = Guide.objects.get(username=request.user)
            if guide is not None:
                params['my_template'] = 'basic3.html'
                projects = Project.objects.filter(project_guide__guide_id=guide,project_guide__accept = True)
                # print(projects)
                project_list = []
                for project in projects:
                    dict = {}

                    # print(p)
                    dict['id'] = project.id
                    dict['photo'] = project.photo
                    dict['name'] = project.name
                    dict['tag_line'] = project.tag_line
                    project_list.append(dict)

                params['projects'] = project_list
                if guide.photo:
                    params['profile'] = guide.photo
                else:
                    params['profile'] = "../media/Profile1.jpg"
                params['name'] = guide.name
                params['username'] = guide.username
                projects = Project.objects.filter(project_guide__guide_id=guide, project_guide__accept=False)
                params['notifications'] = len(projects)
                # params['len'] = len(projects)
                return render(request, 'Portfolio.html', params)
        except:
            pass

        # print(params)
    else:
        return HttpResponseRedirect('/login/')






def add_project(request):
    get_guides()
    if request.method=="POST":
        fm=AddProject(request.POST,request.FILES)
        if fm.is_valid():
            messages.success(request,'Successfully Added')
            fm.save()
            student = Student.objects.get(username=request.user)
            #
            project = Project.objects.filter(name = fm.cleaned_data['name'], tag_line = fm.cleaned_data['tag_line'])[0]

            pro = Project_Student(project_id=project, student_id=student)
            pro.save()
            teacher_name = fm.cleaned_data['guide']
            batch = fm.cleaned_data['batch']
            # print(teacher_name,batch)
            # teacher = request.POST.get(teacher_name)
            # if teacher == "Other":
            #     (Project.objects.filter(name = fm.cleaned_data['name'], tag_line = fm.cleaned_data['tag_line'])[0]).update(verified = True)
            #     return HttpResponseRedirect('/portfolio/')
            guide = Guide.objects.get(name = teacher_name)
            # project.guide = teacher_name
            # project.save()
            # print(type(guide))
            pro_gui = Project_Guide(project_id = project, guide_id = guide)
            pro_gui.save()
            # mail to teacher


            return HttpResponseRedirect('/portfolio/')

    else:
        messages.success(request, 'Error !!')
        fm=AddProject()
        # return HttpResponseRedirect('/settings/')

    params = {}
    if request.user.is_authenticated:
        params['my_template'] = 'basic4.html'
        student = Student.objects.get(username=request.user)
        params['profile'] = student.photo
        params['name'] = student.name
        params['username'] = student.username
        params['form'] = fm
        params['guides'] = l
    else:
        return HttpResponseRedirect('/login/')
    return render(request,'Addproject.html',params)
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect('/login/')
    #
    # fm=AddProject(request.POST)
    #
    # if request.method == "POST":
    #     fm = AddProject(request.POST)
    #     if fm.is_valid():
    #         messages.success(request, 'Account Created Successfully !!')
    #         fm.save()
    #         return HttpResponse("Success")
    #
    # else:
    #     return HttpResponse("Failure")
    #     fm = AddProject()
    # if fm.is_valid():
    #     messages.success(request,'Account Created Successfully !!')
    #     fm.save()
    #     return HttpResponse("Success")
    # else:
    #     return HttpResponse("Failure")


    return render(request,'signup.html',{'form':fm})
    # #pass
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect('/login/')
    # fm = AddProject(request.POST)
    # if fm.is_valid():
    #     messages.success(request, 'Added Successfully !!')
    #     fm.save()
    #     return HttpResponseRedirect('/portfolio/')
    # # if request.method=="POST":
    # #
    # #
    # #         # student = Student.objects.get(username = request.user)
    # #         # s_id = student.id
    # #         # project_name = Project.objects.get(name = fm.cleaned_data['name'])
    # #         # p_id = project_name.id
    # #         # pro = Project_Student(project_id = p_id, student_id = s_id)
    # #         #
    # #         # pro.save()
    #
    # else:
    #     print("Gandal")
    #     fm = AddProject()
    #
    # params = {}
    # project = AddProject(request.POST)
    # params['my_template'] = 'basic2.html'
    # student = Student.objects.get(username=request.user)
    # params['profile'] = student.photo
    # params['form'] = project
    #
    # return render(request,'Addproject.html',params)



    # params = {}
    # project = AddProject(request.POST)
    # params['my_template'] = 'basic2.html'
    # student = Student.objects.get(username = request.user)
    # params['profile'] = student.photo
    # params['form'] = project

    # if project.is_valid():
    #     return HttpResponseRedirect('/settings/')
    # if request.method == 'POST':
    #     print("post")
    # return render(request, 'Addproject.html', params)
    # if request.method == 'POST':
    #     project = AddProject(request.POST)
    #     params = {}
    #
    #     params['my_template'] = 'basic2.html'
    #     student = Student.objects.get(username = request.user)
    #     params['profile'] = student.photo
    #     params['form'] = project
    #
    #
    #     if project.is_valid():
    #         print('project',project)
    #         project.save()
    #         student = Student.objects.get(username = request.user)
    #         s_id = student.id
    #         project_name = Project.objects.get(name = project.cleaned_data['name'])
    #         p_id = project_name.id
    #         pro = Project_Student(project_id = p_id, student_id = s_id)
    #
    #         pro.save()
    #         return HttpResponseRedirect('/portfolio/')
    #     else:
    #         print('not valid')
    #
    #
    #
    #     # print(params)
    # else:
    #     return HttpResponseRedirect('/login/')
    #
    # return render(request,'Addproject.html',params)

def guide_project_notification(request):
    if request.user.is_authenticated:
        params = {}
        get_filters(params)
        if request.method == 'POST':
            # print("POST")
            project_id = request.POST.get('project_id')
            # print(project_id)
            status = request.POST.get('status')
            # print(status)
            project = Project.objects.get(id = project_id)
            # print(project)
            # student = Student.objects.filter(Project_Student__Project_id = project)[0]
            student = Student.objects.filter(project_student__project_id=project)
            # print(student)
            guide = Guide.objects.get(username = request.user)
            if status == 'accept':
                Project_Guide.objects.filter(project_id = project, guide_id = guide).update(accept = True)
                project.verified = True
                project.guide = guide.name
                project.save()
            else:
                Project_Guide.objects.filter(project_id=project, guide_id=guide).delete()
            # print(guide)

        try:
            guide = Guide.objects.get(username = request.user)
            if guide is None:
                return HttpResponseRedirect('/login/')
            projects = Project.objects.filter(project_guide__guide_id=guide,project_guide__accept=False)
            # print(projects)
            project_list = []

            for project in projects:
                dict = {}

                # print(p)
                dict['id'] = project.id
                dict['photo'] = project.photo
                dict['name'] = project.name
                dict['tag_line'] = project.tag_line
                if project.verified:
                    dict['verified'] = "Accepted"
                else:
                    dict['verified'] = "Pending"
                project_list.append(dict)

            params['projects'] = project_list
            params['notifications'] = len(projects)
            if guide.photo:
                params['profile'] = guide.photo
            else:
                params['profile'] = "../media/Profile1.jpg"
            params['name'] = guide.name
            params['username'] = guide.username
            params['my_template'] = 'basic3.html'

            return render(request,'Notifications.html',params)

        except:
            return HttpResponseRedirect('/login/')






def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


