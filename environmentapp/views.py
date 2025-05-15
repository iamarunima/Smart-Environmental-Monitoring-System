import random

from django.db import connection, IntegrityError
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def homepage(request):
    return render(request, "HomePage.html")


def login(request):
    return render(request, "login.html")


def LogOut(request):
    return render(request, "logout.html")


def adminHome(request):
    return render(request, "AdminHome.html")


def staffHome(request):
    return render(request, "StaffHome.html")


def log(request):
    return render(request, "login.html")


# Updated login1 view function 
def login1(request):
    if request.method == 'POST':
        name = request.POST['un']
        password = request.POST['pass']
        request.session['lid'] = name
        
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id='" + name + "' and password='" + password + "'")
        res = cursor.fetchone()
        if res is not None:
            return redirect("/adminHome")
            
        cursor = connection.cursor()
        cursor.execute("select * from monitoring_staff where staff_id='" + name + "' and password='" + password + "'")
        print("select * from monitoring_staff where staff_id='" + name + "' and password='" + password + "'")
        res = cursor.fetchone()
        if res is not None:
            return redirect("/staffHome")
        else:
            # Instead of returning an alert script, render the login page with an error message
            return render(request, 'login.html', {'error_message': 'Invalid username or password. Please try again.'})
    else:
        return render(request, 'login.html')


# #----------------------------------------------Admin---------------------------------------------------------------------------#

# def value(request):reg


def linkaddStaff(request):
    return render(request, "Admin/AddStaff.html" )


def addStaff(request):
    if request.method == "POST":
        staff_id  = request.POST['staff_id']
        name      = request.POST['TxtName']
        address   = request.POST['TxtAddress']
        phone     = request.POST['TxtPhone']
        email     = request.POST['TxtEmail']
        password  = request.POST['TxtPassword']

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO monitoring_staff
                    (staff_id, name, phone, email, address, password)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    [staff_id, name, phone, email, address, password]
                )
        except IntegrityError as e:
            messages.error(request, f"A staff member with ID '{staff_id}' already exists.")
            return redirect('addStaff')   # or render(request, "Admin/AddStaff.html")

        messages.success(request, "Staff registered successfully!")
        return redirect('adminHome')

    return render(request, "Admin/AddStaff.html")


def viewStaff(request):
    cursor = connection.cursor()
    cursor.execute("select * from monitoring_staff")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewStaff.html", {'data': res})


def linkeditStaff(request, id, email):
    request.session['email'] = email
    cursor = connection.cursor()
    cursor.execute("select * from monitoring_staff where staff_id='" + str(id) + "'")
    res = cursor.fetchone()
    return render(request, "Admin/SelectStaff.html", {'data': res})


def editStaff(request):
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['TxtName']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        password = request.POST['TxtPassword']
        oemail = request.session['email']
        if oemail == email:
            cursor = connection.cursor()
            cursor.execute(
                "update monitoring_staff set name='" + name + "',address='" + address + "',phone='" + phone + "',password='" + password + "' where staff_id='" + str(
                    id) + "'")
            return HttpResponse("<script>alert('Updated succesfully');window.location='/viewStaff';</script>")
        cursor = connection.cursor()
        cursor.execute("select * from monitoring_staff where email='" + email + "'")
        res = cursor.fetchone()
        if res == None:
            cursor = connection.cursor()
            cursor.execute(
                "update monitoring_staff set name='" + name + "',address='" + address + "',phone='" + phone + "',email='" + email + "',password='" + password + "' where staff_id='" + id + "'")
            return HttpResponse("<script>alert('Updated succesfully');window.location='/viewStaff';</script>")
        return HttpResponse("<script>alert('Email id Already Exist');window.location='/viewStaff';</script>")


def linkDeleteStaff(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from monitoring_staff where staff_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted succesfully');window.location='/viewStaff';</script>")


def linkAddDevice(request):
    return render(request, "Admin/AddDevice.html")


def addDevice(request):
    if request.method == "POST":
        id = request.POST['id']
        address = request.POST['TxtAddress']
        pincode = request.POST['TxtPincode']
        latitude = request.POST['TxtLatitude']
        longitude = request.POST['TxtLongitude']

        device_type = request.POST['device_type']
        cursor = connection.cursor()
        cursor.execute("insert into device_register values('" + str(
            id) + "','" + address + "','" + pincode + "',curdate(),'" + latitude + "','" + longitude + "','" + device_type + "')")
        return HttpResponse("<script>alert('Simulater Added succesfully');window.location='/adminHome';</script>")


def viewDevice(request):
    cursor = connection.cursor()
    cursor.execute("select * from device_register")
    res = cursor.fetchall()
    return render(request, "Admin/ViewDevice.html", {'data': res})


def linkEditDevice(request, id):
    request.session["edit_session"] = id
    cursor = connection.cursor()
    cursor.execute("select * from device_register where device_id='"+id+"' ")
    res = cursor.fetchone()
    return render(request, "Admin/SelectDevice.html", {'data': res})


def editDevice(request):
    if request.method == "POST":
        id = request.session["edit_session"]
        address = request.POST['TxtAddress']
        pincode = request.POST['TxtPincode']
        latitude = request.POST['TxtLatitude']
        longitude = request.POST['TxtLongitude']
        device_type = request.POST['device_type']
        cursor = connection.cursor()
        cursor.execute(
            "update device_register set address='" + address + "',pincode='" + pincode + "',latitude='" + latitude + "',longitude='" + longitude + "',device_type='"+device_type+"' where device_id='" + id + "'")
    return HttpResponse("<script>alert('Updated succesfully');window.location='/viewDevice';</script>")


def linkDeleteDevice(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from device_register where device_id='" + id + "'")
    return HttpResponse("<script>alert('Deleted succesfully');window.location='/viewDevice';</script>")


def linkViewStaff(request, id):
    request.session['did'] = id
    cursor = connection.cursor()
    cursor.execute("select * from assign_staff_device where device_id='" + str(id) + "'")
    res = cursor.fetchall()
    if res is not None:
        cursor = connection.cursor()
        cursor.execute("select * from monitoring_staff")
        res = cursor.fetchall()
        if res is not None:
            if res is None:
                return render(request, "Admin/NoDataFound.html")
        return render(request, "Admin/ViewStaffAss.html", {'data': res})
    else:
        return render(request, "Admin/DeviceAlready.html")


def linkUnAssign(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from assign_staff_device where staff_device_id='" + id + "'")
    return HttpResponse("<script>alert('Unassigned');window.location='/viewDevice';</script>")


def linkAssignStaffDevice(request, id):
    request.session['staffid'] = id
    cursor = connection.cursor()
    cursor.execute(
        "select a.*,d.* from assign_staff_device as a join device_register as d on d.device_id=a.device_id where a.staff_id='" + str(id) + "'")
    res = cursor.fetchall()
    if res is None:
        return render("Admin/Assign.html")
    return render(request, "Admin/AssignStaffDevice.html", {'data': res})


def staffAssign(request,id):

    deviceid = request.session['did']
    cursor = connection.cursor()
    print("insert into assign_staff_device values(null,'" + id + "','" + deviceid + "',curdate())")
    cursor.execute("insert into assign_staff_device values(null,'" + id + "','" + deviceid + "',curdate())")
    return HttpResponse("<script>alert('Assigned successfully');window.location='../adminHome';</script>")


def viewAllStaffAssignedDevice(request):
    cursor = connection.cursor()
    #cursor.execute("select a.*,d.*,ms.name from assign_staff_device as a join device_register as d join monitoring_staff as ms on a.device_id=d.device_id  ")
    cursor.execute("select  a.staff_device_id,a.device_id,d.address,ms.name from assign_staff_device as a join device_register as d join monitoring_staff as ms on a.device_id=d.device_id  AND a.staff_id=ms.staff_id")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewAllStaffAssignedDevice.html", {'data': res})


def viewAirPollutionDetails(request):
    cursor = connection.cursor()
    cursor.execute("SELECT device_register.address,device_register.latitude,device_register.longitude,  air_pollution_from_device.* FROM air_pollution_from_device JOIN device_register ON air_pollution_from_device.device_id=device_register.device_id ")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewAirPollutionDetails.html", {'data': res})


def random_air_pollution_link(request):
    num1 = random.randint(21, 35)
    num2 = random.randint(21, 35)
    num3 = random.randint(21, 35)
    num4 = random.randint(21, 35)
    num5 = random.randint(21, 35)
    request.session['num1'] = num1
    request.session['num2'] = num2
    request.session['num3'] = num3
    request.session['num4'] = num4
    request.session['num5'] = num5
    return render(request, "Admin/random_air_pollution_link.html")


def random_air_pollution(request):


    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    num3 = int(request.POST['num3'])
    num4 = int(request.POST['num4'])
    num5 = int(request.POST['num5'])

    device_id = request.POST['id']
    cursor = connection.cursor()
    cursor.execute("select distinct device_id from air_pollution_monitoring")
    data = cursor.fetchall()
    print(data)

    if num1 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into air_pollution_monitoring values(null, curdate(), '" + str(device_id) + "','" + str(
            num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "','" + str(num5) + "') ")
    if num2 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into air_pollution_monitoring values(null, curdate(), '" + str(device_id) + "','" + str(
            num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "','" + str(num5) + "') ")

    if num3 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into air_pollution_monitoring values(null, curdate(), '" + str(device_id) + "','" + str(
            num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "','" + str(num5) + "') ")

    if num4 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into air_pollution_monitoring values(null, curdate(), '" + str(device_id) + "','" + str(
            num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "','" + str(num5) + "') ")

    if num5 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into air_pollution_monitoring values(null, curdate(), '" + str(device_id) + "','" + str(
            num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "','" + str(num5) + "') ")
    num1 = random.randint(21, 35)
    num2 = random.randint(21, 35)
    num3 = random.randint(21, 35)
    num4 = random.randint(21, 35)
    num5 = random.randint(21, 35)
    request.session['num1'] = num1
    request.session['num2'] = num2
    request.session['num3'] = num3
    request.session['num4'] = num4
    request.session['num5'] = num5
    return render(request, "Admin/random_air_pollution_link.html", {'data': data})


def random_water_pollution_link(request):
    num1 = random.randint(21, 35)
    num2 = random.randint(21, 35)
    num3 = random.randint(21, 35)
    num4 = random.randint(21, 35)
    num5 = random.randint(21, 35)



    request.session['num1'] = num1
    request.session['num2'] = num2
    request.session['num3'] = num3
    request.session['num4'] = num4
    request.session['num5'] = num5
    return render(request, "Admin/random_water_pollution_link.html")


def random_water_pollution(request):
    num1 = random.randint(21, 35)
    num2 = random.randint(21, 35)
    num3 = random.randint(21, 35)
    num4 = random.randint(21, 35)


    request.session['num1'] = num1
    request.session['num2'] = num2
    request.session['num3'] = num3
    request.session['num4'] = num4


    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    num3 = int(request.POST['num3'])
    num4 = int(request.POST['num4'])

    device_id = request.POST['id']
    cursor = connection.cursor()
    cursor.execute("select distinct device_id from water_pollution_monitoring")
    data = cursor.fetchall()
    print(data)

    if num1 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into water_pollution_monitoring values(null,'" + str(device_id) + "','" + str(num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "',curdate()) ")
    if num2 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into water_pollution_monitoring values(null,'" + str(device_id) + "','" + str(num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "',curdate()) ")

    if num3 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into water_pollution_monitoring values(null,'" + str(device_id) + "','" + str(num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "',curdate()) ")
    if num4 > 20:
        cursor = connection.cursor()
        cursor.execute("insert into water_pollution_monitoring values(null,'" + str(device_id) + "','" + str(num1) + "','" + str(num2) + "','" + str(num3) + "','" + str(num4) + "',curdate()) ")


    return render(request, "Admin/random_water_pollution_link.html", {'data': data})


def water_chart3(request):
    import sys
    import matplotlib
    matplotlib.use('TkAgg')
    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from water_pollution_monitoring group by device_id")
    data = cursor.fetchall()

    import matplotlib.pyplot as plt
    import numpy as np

    x = []
    values = []
    for row in data:
        x.append(row[1])
        # print(row[0])
    values.clear()

    for row in data:
        values.append(row[0])

    plt.plot(values, x, marker='o')
    plt.show()

    # Two  lines to make our compiler able to draw:
    plt.savefig(sys.stdout.buffer)
    plt.xlabel("Problem Details")
    plt.ylabel("Water Pollution Pyplot Chart")
    sys.stdout.flush()
    plt.close()
    return redirect( "/viewWaterPollutionDetails")



def water_chart2(request):
    import matplotlib.pyplot as plt
    import numpy as np
    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from water_pollution_monitoring group by device_id")
    data = cursor.fetchall()
    # create data
    x = []
    values = []
    for row in data:
        x.append(row[1])
        # print(row[0])
    values.clear()

    for row in data:
        values.append(row[0])
    # stem function
    plt.stem(x, values)
    plt.ylim(0, 1.2)
    # stem function: If x is not provided, a sequence of numbers is created by python:
    plt.stem(values)
    plt.xlabel("Problem Details")
    plt.ylabel("Water Pollution Pyplot")
    plt.show()
    plt.close()
    return redirect( "/viewWaterPollutionDetails")


def water_chart(request):
    import sys
    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    import numpy as np

    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from water_pollution_monitoring group by device_id")
    data = cursor.fetchall()
    # print(data)
    y = []
    mylabels = []
    i = 0
    for row in data:
        y.append(row[1])
        # print(row[0])
    mylabels.clear()

    for row in data:
        mylabels.append(row[0])
        # print(row[1])

    print(mylabels)
    print(y)
    plt.pie(y, labels=mylabels)
    plt.xlabel("Problem Details")
    plt.ylabel("Water Pollution Pyplot")
    plt.show()
    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush()
    plt.close()
    return redirect( "/viewWaterPollutionDetails")


def chart(request):
    import sys
    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
    import numpy as np

    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from air_pollution_monitoring group by device_id")
    data = cursor.fetchall()
    # print(data)
    y = []
    mylabels = []
    i = 0
    for row in data:
        y.append(row[1])
        # print(row[0])
    mylabels.clear()

    for row in data:
        mylabels.append(row[0])
        # print(row[1])

    print(mylabels)
    print(y)
    plt.pie(y, labels=mylabels)

    plt.savefig(sys.stdout.buffer)
    mylabels.clear()
    plt.xlabel("Problem Details")
    plt.ylabel("Air Pollution Pyplot")
    plt.show()
    plt.close()
    sys.stdout.flush()
    return redirect( "/viewAirPollutionDetails")


def chart2(request):
    import matplotlib.pyplot as plt
    import numpy as np
    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from air_pollution_monitoring group by device_id")
    data = cursor.fetchall()
    # create data
    x = []
    values = []
    for row in data:
        x.append(row[1])
        # print(row[0])
    values.clear()

    for row in data:
        values.append(row[0])
    # stem function
    plt.stem(x, values)
    plt.ylim(0, 1.2)
    plt.show()

    # stem function: If x is not provided, a sequence of numbers is created by python:
    plt.stem(values)
    plt.xlabel("Problem Details")
    plt.ylabel("Air Pollution")
    plt.show()
    plt.close()

    return redirect( "/viewAirPollutionDetails")


def chart3(request):
    import sys
    import matplotlib
    matplotlib.use('TkAgg')
    cursor = connection.cursor()
    cursor.execute("select device_id, count(device_id) from air_pollution_monitoring group by device_id")
    data = cursor.fetchall()

    import matplotlib.pyplot as plt
    import numpy as np

    x = []
    values = []
    for row in data:
        x.append(row[1])
        # print(row[0])
    values.clear()

    for row in data:
        values.append(row[0])
    plt.xlabel("Problem Details")
    plt.ylabel("Air Pollution")
    plt.plot(values, x, marker='o')
    plt.show()

    # Two  lines to make our compiler able to draw:
    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush()

    return redirect( "/viewAirPollutionDetails")


def viewWaterPollutionDetails(request):
    cursor = connection.cursor()
    cursor.execute(
        "select a.*,d.* from water_pollution_monitoring as a join device_register as d on d.device_id=a.device_id order by a.water_pollution_id desc")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewWaterPollutionDetails.html", {'data': res})


def viewLocation(request, lat, lon):
    lat = str(lat)
    lon = str(lon)
    return render(request, 'Admin/ViewLocation.html', {'lat':lat,'lon':lon})


def LinkAddDisease(request):
    return render(request, "Admin/AddDiseases.html")


def addDiseases(request):
    if request.method == "POST":
        name = request.POST['TxtName']
        desc = request.POST['TxtDescription']
        type = request.POST['TxtType']
        cursor = connection.cursor()
        cursor.execute("insert into disease_details values(null,'" + name + "','" + desc + "','" + type + "')")
    return HttpResponse("<script>alert('Inserted succesfully');window.location='/adminHome';</script>")


def viewDisease(request):
    cursor = connection.cursor()
    cursor.execute("select * from disease_details where pollution_type='Air'")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewDisease.html", {'data': res})


def viewWaterPollutionDisease(request):
    cursor = connection.cursor()
    cursor.execute("select * from disease_details where pollution_type='Water'")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewWaterPollutionDisease.html", {'data': res})


def linkDeleteDisease(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from disease_details where disease_detail_id='" + str(id) + "'")
    return HttpResponse("<script>alert('deleted');window.location='/adminHome';</script>")


def linkEditDisease(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from disease_details where disease_detail_id='" + str(id) + "'")
    res = cursor.fetchone()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/SelectDisease.html", {'data': res})


def editDiseases(request):
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['TxtName']
        desc = request.POST['TxtDesc']
        cursor = connection.cursor()
        cursor.execute(
            "update disease_details set name='" + name + "',disease_desc='" + desc + "' where disease_detail_id='" + str(
                id) + "'")
    return HttpResponse("<script>alert('updated succesfully');window.location='/adminHome';</script>")


def deleteDiseases(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from disease_details where disease_detail_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted succesfully');window.location='/AdminHome';</script>")


def viewComplaint(request):
    cursor = connection.cursor()
    cursor.execute("select * from complaint")
    res = cursor.fetchall()
    if res is not None:
        if res == None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/viewComplaint.html", {'data': res})


def viewComplaintReport(request):
    cursor = connection.cursor()
    cursor.execute("select * from complaint")
    res = cursor.fetchall()
    if res:
        data = res
    if res == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/viewComplaintReport.html", {'data': res})


def LinkviewPollutionDetailsDate(request):
    return render(request, "Admin/searchPolutionDate.html")


def linkviewWaterPolutionDate(request):
    return render(request, "Admin/searchWaterPolutionDate.html")


def searchWaterPollutionDetails(request):
    if request.method == "POST":
        dfrom = request.POST['TxtFrom']
        dto = request.POST['TxtTo']
        cursor = connection.cursor()
        cursor.execute(
            "select w.*,d.latitude,d.longitude from water_pollution_monitoring as w join device_register as d where d.device_id=w.device_id and w.detected_date between '" + dfrom + "' and '" + dto + "'")
        res = cursor.fetchall()
        if res is not None:
            if res == None:
                return render(request, "Admin/NoDataFound.html")
        return render(request, "Admin/SearchWaterPollutionDetails.html", {'data': res})


def searchPollutionDetails(request):
    if request.method == "POST":
        dfrom = request.POST['TxtFrom']
        dto = request.POST['TxtTo']
        cursor = connection.cursor()
        cursor.execute(
            "select a.*,d.latitude,d.longitude from air_pollution_from_device as a join device_register as d where d.device_id=a.device_id and a.report_date between '" + dfrom + "' and '" + dto + "'")
        res = cursor.fetchall()
        if res is not None:
            if res is None:
                return render(request, "Admin/NoDataFound.html")
        return render(request, "Admin/SearchAirPollutionDetails.html", {'data': res})


def linkViewWaterPollutionDetailsMonth(request):
    return render(request, "Admin/ViewWaterPollutionDetailsMonth.html")


def searchWaterPollutionMonth(request):
    if request.method == "POST":
        month = request.POST['TxtMonth']
        year = request.POST['TxtYear']
        a = year + "-" + month
        print(a)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT w.*,d.latitude,d.longitude FROM water_pollution_monitoring as w join device_register as d where d.device_id=w.device_id and w.detected_date like '" + a + "%' ")
        res = cursor.fetchall()
        if res is not None:
            if res == None:
                return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewWaterPollutionMonthDetails.html", {'data': res})


def linkViewAirPollutionDetails(request):
    return render(request, "Admin/ViewAirPollutionDetailsMonth.html")


def searchAirPolluMonth(request):
    if request.method == "POST":
        month = request.POST['TxtMonth']
        year = request.POST['TxtYear']
        a = year + "-" + month
        cursor = connection.cursor()
        cursor.execute(
            "SELECT a.*,d.latitude,d.longitude FROM air_pollution_monitoring as a join device_register as d where d.device_id=a.device_id and a.pollution_date like '" + a + "%' ")
        res = cursor.fetchall()
        if res is not None:
            return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewAirPollutionMonthDetails.html", {'data': res})


# #---------------------------------------------------------Staff--------------------------------------------------#

def viewDeviceDetails(request):
    staffid = request.session['lid']
    cursor = connection.cursor()
    cursor.execute(
        "select d.* from device_register as d join assign_staff_device as a on d.device_id=a.device_id where a.staff_id='" + staffid + "'")
    data = cursor.fetchall()
    if data is not None:
        return render(request, "Staff/Viewdevicedetails.html", {'data': data})
    return render(request, "Staff/NoDataFound.html")


def view_complaints_staff(request):
    staffid = request.session['lid']
    cursor = connection.cursor()
    cursor.execute("SELECT  * from complaint  ")
    data = cursor.fetchall()
    if data is not None:
        return render(request, "Staff/ViewComplaintStaff.html", {'data': data})
    return render(request, "Staff/NoDataFound.html")



def viewAirProblemDetails(request):
    staffid = request.session['lid']
    cursor = connection.cursor()
    cursor.execute(" SELECT device_register.address,device_register.latitude,device_register.longitude,  air_pollution_from_device.* FROM air_pollution_from_device JOIN device_register ON air_pollution_from_device.device_id=device_register.device_id  WHERE air_pollution_from_device.device_id='1'")
    data = cursor.fetchall()
    if data is not None:
        return render(request, "Staff/ViewAirProblemDetails.html", {'data': data})
    return render(request, "Staff/NoDataFound.html")



def viewWaterProblemDetails(request):
    staffid = request.session['lid']
    cursor = connection.cursor()
    print("select w.* from water_pollution_monitoring as w join assign_staff_device as a on a.device_id=w.device_id where a.staff_id='" + staffid + "' and w.lead>10 order by w.water_pollution_id desc ")
    #cursor.execute("select w.* from water_pollution_monitoring as w join assign_staff_device as a join device_register on a.device_id=w.device_id and device_register.device_id=w.device_id where a.staff_id='" + staffid + "' and device_register.device_type='water' and w.lead>10 order by w.water_pollution_id desc")
    cursor.execute(
        "select w.* from water_pollution_monitoring as w join assign_staff_device as a on a.device_id=w.device_id where a.staff_id='" + staffid + "' and w.lead>10 order by w.water_pollution_id desc ")
    data = cursor.fetchall()
    if data is not None:
        return render(request, "Staff/ViewWaterProblemDetails.html", {'data': data})
    return render(request, "Staff/NoDataFound.html")



def linkReplyComplaint(request, id):
    request.session['aaid'] = id
    return render(request, "Admin/ReplyComplaint.html")


def linkReplyComplaintSt(request, id):
    request.session['aaid'] = id
    return render(request, "Staff/ReplyComplaint.html")


def selectReply(request):
    id = request.session['aaid']
    reply = request.POST['TxtReply']
    cursor = connection.cursor()
    cursor.execute("update complaint set reply='" + reply + "' where complaint_id='" + str(id) + "' ")
    return HttpResponse("<script>alert('Update successfully');window.location='/viewComplaint';</script>")

def selectReplyStaff(request):
    id = request.session['aaid']
    reply = request.POST['TxtReply']
    cursor = connection.cursor()
    cursor.execute("update complaint set reply='" + reply + "' where complaint_id='" + str(id) + "' ")
    return HttpResponse("<script>alert('Update successfully');window.location='/view_complaints_staff';</script>")



def viewLocationS(request, lat, lon):
    lat = str(lat)
    lon = str(lon)
    return render(request, 'Staff/ViewLocation.html', {'lat':lat,'lon':lon})



def check_notification(request):
    cursor = connection.cursor()
    cursor.execute("select * from admin_notification ")
    data = cursor.fetchall()
    st=0
    if len(data) > 0:
        st=1
        cursor.execute("delete from admin_notification ")
    else:
        st = 0

    cursor.close()
    print(st)
    return render(request, "Admin/ViewAlert.html",{'sta':st})


def check_notification_staff(request):
    cursor = connection.cursor()
    cursor.execute("select * from admin_notification ")
    data = cursor.fetchall()
    st=0
    if len(data) > 0:
        st=1
        cursor.execute("delete from admin_notification ")
    else:
        st = 0

    cursor.close()
    print(st)
    return render(request, "Staff/ViewAlert.html",{'sta':st})
