from django.urls import path
from . import views
urlpatterns = [
    path('',views.system,name='index'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('add',views.add,name='add'),
    path('deduct_session/', views.deduct_session, name='deduct_session'),
    path('print_client/<int:client_id>/', views.print_client, name='print_client'),
    path('search_client/', views.search_client, name='search_client'), 
]
