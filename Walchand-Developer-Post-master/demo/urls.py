from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("",views.homepage,name='homepage'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path("projects/",views.display_projects,name = 'display_projects'),
    path("projects/<int:id>/<slug:slug>",views.single_project,name = 'single_project'),
    path("projects/<str:heading>/<str:search>",views.view_search, name = 'view_search'),
    path("search/",views.search,name = "search"),
    path("filters/",views.filters,name = "filters"),
    path('verification/',views.stu_verification,name='stu_verification'),
    path('verify_otp/',views.verify_otp,name= 'verify_otp'),
    path('settings/',views.settings,name = 'settings'),
    path('save_changes/',views.save_changes,name='save_changes'),
    path('portfolio/',views.portfolio,name = 'portfolio'),
    path('add_project/',views.add_project,name='add_project'),
    path('notifications',views.guide_project_notification, name = "guide_project_notification"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)