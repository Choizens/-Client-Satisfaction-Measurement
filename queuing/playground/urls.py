from django.urls import path
from . import views

urlpatterns = [
    path('', views.code, name='Code'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.manage_survey, name='manage_survey'),

    #amanage survey paths for msurvey1, msurvey2, msurvey3
    path("manage/msurvey1/", views.msurvey1, name="msurvey1"),
    path("manage/msurvey2/", views.msurvey2, name="msurvey2"),
    path("manage/msurvey3/", views.msurvey3, name="msurvey3"),
]