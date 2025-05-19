from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import assigned_tickets, respond_ticket, view_progress_pathway, admin_insightboard, dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('ticket/mine/', views.my_tickets, name='my_tickets'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('ticket/mine/', views.my_tickets, name='my_tickets'),

    path('admin-tickets/', views.assigned_tickets, name='assigned_tickets'),
    path('admin-tickets/respond/<int:ticket_id>/', views.respond_ticket, name='respond_ticket'),
    path('track-timeline/<int:ticket_id>/', views.view_progress_pathway, name='ticket_timeline'),
    path('admin-insightboard/', views.admin_insightboard, name='admin_insightboard'),
    path('progress/', views.view_progress_pathway, name='view_progress_pathway'),
    
    path('custom-admin/departments/', views.admin_departments, name='admin_departments'),
    path('custom-admin/departments/add/', views.add_department, name='add_department'),
    path('custom-admin/departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),
    path('custom-admin/departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    
    path('custom-admin/categories/', views.admin_categories, name='admin_categories'),
    path('custom-admin/categories/add/', views.add_category, name='add_category'),
    path('custom-admin/categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('custom-admin/categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin-users/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin-users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
]
