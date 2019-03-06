from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, AdminForm, EventsForm
from .models import Organization, org_Admin,Employee,Survey,SurveyEmployee,SurveyQuestion,SurveyResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import logging
import datetime


# Create your views here.
def index(request):
    return render(request, 'newsurvey/index.html')


@csrf_exempt
def login(request):
    print("calling post method")
    form = LoginForm()
    context = {'form': form}

    if request.method == "POST":
        print("Entering into post method")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username", username)
        print("password", password)

    try:
        Usersdata = User.objects.filter(username=username, password=password)
        print(str(Usersdata))

        if (User.objects.filter(username=username).exists()):
            # User.objects.create_user(username, password)
            user = authenticate(username=username, password=password)

            return redirect('index')
        elif org_Admin.objects.get(admin_username=username, password=password):
            print("hello else iff")
            m = request.session['username'] = username
            # m1 = {'session': m}

            print("Session Name = " + m)
            return redirect('index')

    except Exception as e:
        print('Exception ', e)
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
        return render(request, "newsurvey/login.html", context)

    return render(request, "newsurvey/login.html", context)


@csrf_exempt
def admin_register(request):
    form = AdminForm()
    context = {'form': form}
    if request.method == "POST":
        ad_username = request.POST.get("adminname")
        ad_password = request.POST.get("ad_password")

        m = request.POST.get('OrgnisationName')
        print("mm",m)
        Org_names = Organization.objects.get(company_name=m)

        print("ad_username", ad_username)
        print("ad_password", ad_password, request.POST.get('email'), request.POST.get('OrgnisationName'),
              request.POST.get('password'))
        print("Entering into post method")

        if request.POST.get('adminname') and request.POST.get('username') and request.POST.get(
                'email') and request.POST.get('OrgnisationName') and request.POST.get('password'):
            registerObject = org_Admin()
            registerObject.admin_name = request.POST.get('adminname')
            registerObject.admin_username = request.POST.get('username')
            registerObject.admin_email = request.POST.get('email')
            registerObject.company = Org_names
            registerObject.password = request.POST.get('password')
            registerObject.save()

        else:
            return redirect('admin_register')

    return render(request, "newsurvey/Org_adminlogin.html")


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')


def add_org(request):
    if request.method == "POST":
        print("Entering into post method")

        if request.POST.get('org_name') and request.POST.get('org_loc') and request.POST.get('org_desc'):
            OrgnizationObject = Organization()
            OrgnizationObject.company_name = request.POST.get('org_name')
            OrgnizationObject.location = request.POST.get('org_loc')
            OrgnizationObject.description = request.POST.get('org_desc')
            OrgnizationObject.save()
            return redirect("add_org")
        else:
            return redirect('index')

    return render(request, "newsurvey/org.html")


def getorgdata(request):
    org = list()
    total_record = 0
    orgDetails1 = Organization.objects.all()
    org.append(orgDetails1)

    i = 0
    temp_list = []
    data = {}
    for org1 in orgDetails1:
        i = i + 1
        temp_list = [i, str(org1.company_name), str(org1.location), str(org1.description)]


    data = {'completeData': temp_list}
    print("mydata", data)

    return HttpResponse(json.dumps(data), content_type="application/json")


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "newsurvey/emplist.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            print("lines*************",line != "")
            if line != "":
                fields = line.split(",")
                data_dict = {}
                data_dict["emp_name"] = fields[0]
                data_dict["emp_username"] = fields[1]
                data_dict["emp_password"] = fields[2]
                data_dict["emp_designation"] = fields[3]
                data_dict["emp_address"] = fields[4]
                data_dict["company"] = fields[5]
                m = (data_dict["company"]).strip()
                print("m===>", m)
                print("compare", m == "abc")
                Org_names = Organization.objects.get(company_name=m)
                print("Org_names===>", Org_names)
                try:
                    form = EventsForm(data_dict)
                    # OrgEmployeeObj = Employee()
                    OrgEmployeeObj = Employee()
                    OrgEmployeeObj.emp_name = data_dict["emp_name"]
                    OrgEmployeeObj.emp_username = data_dict["emp_username"]
                    OrgEmployeeObj.emp_password = data_dict["emp_password"]
                    OrgEmployeeObj.emp_designation = data_dict["emp_designation"]
                    OrgEmployeeObj.emp_address = data_dict["emp_address"]
                    OrgEmployeeObj.company = Org_names

                    OrgEmployeeObj.save()
                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        # import traceback
        # traceback.print_exc()
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))

def Add_Survey(request):
    if request.method == "POST":
        print("Entering into post method")

        if request.POST.get('sur_name') and request.POST.get('sur_desc'):
            print("add Survey")
            SurveyObj1 = Survey()
            SurveyObj1.survey_name = request.POST.get('sur_name')
            SurveyObj1.description = request.POST.get('sur_desc')
            SurveyObj1.date = datetime.datetime.now()
            SurveyObj1.save()
            return redirect("Add_Survey")
        else:
            return redirect('index')
    return render(request, 'newsurvey/addsurveypage.html')
