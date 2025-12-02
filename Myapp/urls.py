from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import add_comment


urlpatterns = [
    path('', views.login_user, name='login'), 
    path('register/', views.register_user, name='register'),
    path('home/', views.home, name='home'),
    path('contact/',views.contact,name='contact'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/report/<int:post_id>/', views.report_post, name='report_post'),
    path("comment/<int:post_id>/", add_comment, name="add_comment"),
    path("profile/", views.profile, name="profile"),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
   path("follow/<int:user_id>/", views.follow_toggle, name="follow_toggle"),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
