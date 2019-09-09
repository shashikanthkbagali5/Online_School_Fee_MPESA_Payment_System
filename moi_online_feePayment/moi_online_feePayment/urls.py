"""moi_online_feePayment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from students.views import student_detail, student_create, log_out, log_in, students_list, search, edit_student, exam_card, ssd_test
from payment.views import fee_report, test, bill, statements

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(('rest_api.urls', 'rest_api'), namespace='api_')),
    path('', student_detail, name='student_home'),
    path('create/', student_create, name='create_'),
    path('logout/', log_out),
    path('billing/', bill, name='bill_'),
    path('search/', search, name='search_'),
    path('list/', students_list, name='students_'),
    path('fees/', fee_report, name='fees_'),
    path('edit/', edit_student, name='edit_'),
    path('card/', exam_card, name='card_'),
    # path('call/', call_back, name='call_'),
    path('ssd', ssd_test),
    # path('ticket/', get_token),
    path('statement/', statements, name='state'),
    # path('push/', stk_push, name='stk_'),
    path('payment/', test, name='payment_'),
    path('login/', log_in, name='log__in'),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
