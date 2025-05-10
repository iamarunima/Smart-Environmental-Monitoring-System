"""djenvironment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from. import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('staffHome', views.staffHome, name="staffHome"),
    path('check_notification', views.check_notification, name="check_notification"),

path('selectReplyStaff', views.selectReplyStaff, name="selectReplyStaff"),

path('linkReplyComplaintSt/<int:id>', views.linkReplyComplaintSt, name="linkReplyComplaintSt"),
    path('login', views.login, name="login"),
    path('LogOut', views.LogOut, name="LogOut"),
    path('adminHome', views.adminHome, name="adminHome"),

path('check_notification_staff', views.check_notification_staff, name="check_notification_staff"),
    path('login1', views.login1, name="login1"),
    path('viewStaff', views.viewStaff, name="viewStaff"),
    path('linkaddStaff', views.linkaddStaff, name="linkaddStaff"),
    path('linkeditStaff/<str:id>/<str:email>', views.linkeditStaff, name="linkeditStaff"),
    path('addStaff', views.addStaff, name="addStaff"),
    path('editStaff', views.editStaff, name="editStaff"),
    path('linkDeleteStaff/<str:id>', views.linkDeleteStaff, name="linkDeleteStaff"),
    path('linkAddDevice', views.linkAddDevice, name="linkAddDevice"),
    path('addDevice', views.addDevice, name="addDevice"),
    path('viewDevice', views.viewDevice, name="viewDevice"),
    path('linkEditDevice/<str:id>', views.linkEditDevice, name="linkEditDevice"),
    path('editDevice', views.editDevice, name="editDevice"),
    path('linkDeleteDevice/<str:id>', views.linkDeleteDevice, name="linkDeleteDevice"),
    path('linkViewStaff/<str:id>', views.linkViewStaff, name="linkViewStaff"),
    path('linkUnAssign/<str:id>', views.linkUnAssign, name="linkUnAssign"),
    path('linkAssignStaffDevice/<str:id>', views.linkAssignStaffDevice, name="linkAssignStaffDevice"),
    path('staffAssign/<str:id>', views.staffAssign, name="staffAssign"),
    path('viewAllStaffAssignedDevice', views.viewAllStaffAssignedDevice, name="viewAllStaffAssignedDevice"),
    path('viewAirPollutionDetails', views.viewAirPollutionDetails, name="viewAirPollutionDetails"),
    path('viewWaterPollutionDetails', views.viewWaterPollutionDetails, name="viewWaterPollutionDetails"),
    path('viewLocation/<str:lat>/<str:lon>', views.viewLocation, name="viewLocation"),
    path('viewLocationS/<str:lat>/<str:lon>', views.viewLocationS, name="viewLocationS"),
    path('view_complaints_staff', views.view_complaints_staff, name="view_complaints_staff"),
    path('LinkAddDisease', views.LinkAddDisease, name ="LinkAddDisease"),
    path('addDiseases', views.addDiseases, name="addDiseases"),
    path('viewDisease', views.viewDisease, name="viewDisease"),
    path('linkDeleteDisease/<str:id>', views.linkDeleteDisease, name="linkDeleteDisease"),
    path('linkEditDisease/<str:id>', views.linkEditDisease, name="linkEditDisease"),
    path('viewWaterPollutionDisease', views.viewWaterPollutionDisease, name="viewWaterPollutionDisease"),
    path('linkEditDisease/<str:id>', views.viewWaterPollutionDisease, name="viewWaterPollutionDisease"),
    path('editDiseases', views.editDiseases, name="editDiseases"),
    path('deleteDiseases/<str:id>', views.deleteDiseases, name="deleteDiseases"),
    path('viewComplaint', views.viewComplaint, name="viewComplaint"),
    path('viewComplaintReport', views.viewComplaintReport, name="viewComplaintReport"),
    path('LinkviewPollutionDetailsDate', views.LinkviewPollutionDetailsDate, name="LinkviewPollutionDetailsDate"),
    path('linkviewWaterPolutionDate', views.linkviewWaterPolutionDate, name="linkviewWaterPolutionDate"),
    path('searchWaterPollutionDetails', views.searchWaterPollutionDetails, name="searchWaterPollutionDetails"),
    path('searchPollutionDetails', views.searchPollutionDetails, name="searchPollutionDetails"),
    path('linkReplyComplaint/<int:id>', views.linkReplyComplaint, name="linkReplyComplaint"),
    path('linkViewWaterPollutionDetailsMonth', views.linkViewWaterPollutionDetailsMonth, name="linkViewWaterPollutionDetailsMonth"),
    path('searchWaterPollutionMonth', views.searchWaterPollutionMonth, name="searchWaterPollutionMonth"),
    path('linkViewAirPollutionDetails', views.linkViewAirPollutionDetails, name="linkViewAirPollutionDetails"),
    path('selectReply', views.selectReply, name="selectReply"),
    path('chart', views.chart, name= "Chart"),
    path('chart2', views.chart2, name= "Chart2"),
    path('chart3', views.chart3, name="Chart3"),
    path('water_chart', views.water_chart, name= "water_chart"),
    path('water_chart2', views.water_chart2, name= "water_chart2"),
    path('water_chart3', views.water_chart3, name= "water_chart3"),
    path('random_air_pollution_link', views.random_air_pollution_link, name = "random_air_pollution_link"),
    path('random_air_pollution', views.random_air_pollution, name = "random_air_pollution"),
    path('random_water_pollution_link', views.random_water_pollution_link, name="random_water_pollution_link"),
    path('random_water_pollution', views.random_water_pollution, name="random_water_pollution"),
    path('viewWaterProblemDetails', views.viewWaterProblemDetails, name = "viewWaterProblemDetails"),
    path('viewAirProblemDetails', views.viewAirProblemDetails, name = "viewAirProblemDetails"),

    path('viewDeviceDetails', views.viewDeviceDetails, name="viewDeviceDetails"),




]
