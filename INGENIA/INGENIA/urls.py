from django.contrib import admin
from django.urls import path
from App import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views


def admin_required(user):
    return user.is_superuser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', login_required(user_passes_test(admin_required)(views.create_event)), name='create_event'),
    path('events/', views.event_list, name='event_list'),
    path('events/register/<int:event_id>/', views.register, name='register'),
    path('check-in/', login_required(user_passes_test(admin_required)(views.check_in)), name='check_in'),
    path('export/<int:event_id>/', views.export_attendees, name='export_attended'),
    path('add-review/<int:event_id>/', views.add_review, name='add_review'),
    path('toggle-reviews/<int:event_id>/<str:action>/', views.toggle_reviews, name='toggle_reviews'), 

]
