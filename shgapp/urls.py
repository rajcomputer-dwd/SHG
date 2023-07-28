from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),

    path('branch/', views.create_branch_view, name='create_branch_view'),
    path('branch/<int:branch_id>/', views.update_branch_view, name='update_branch'),

    path('society/' , views.create_society_view , name='create_society_view'),
    path('society/<int:soc_id>/', views.update_society_view, name='update_society'),
    path('upload_society/', views.upload_file_society, name='upload_file'),

    path('shgdetails_bank/', views.shg_details_bank_form , name='shg_details_bank_form'),
    path('get_group_bank_names/', views.get_group_bank_names, name='get_group_bank_names'),
    

    path('shgdetails_society/', views.shg_details_society_form , name='shg_details_society_form'),
    path('get_group_society_names/', views.get_group_society_names, name='get_group_society_names'),


    path('create_shgtransaction_bank/', views.create_shgtransaction_bank, name='create_shgtransaction_bank'),
    path('get_group_names_bank/<str:branchname>/', views.get_group_names_bank, name='get_group_names_bank'),

    path('create_shgtransaction_society/', views.create_shgtransaction_society, name='create_shgtransaction_society'),
    path('get_group_names_society/<str:society_name>/', views.get_group_names_society, name='get_group_names_society'),


]
    



