from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from . import views
urlpatterns = [
    path('login/',views.hendel_login,name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('newrequest/',views.new_request,name='new_request'),
    path('approv/<int:req_id>/', views.approv, name='approv'),
    path('rejected/<int:req_id>/',views.rejected,name='rejected'),
    path('request_form/',views.request_form,name='request_form'),
    path('base/',views.base,name='base'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

