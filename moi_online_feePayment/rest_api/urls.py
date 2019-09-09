from rest_framework import routers
from django.urls import path
from .views import StudentRudView, TransactionCreateView, StudentListView, CallbackView, WhatsappView #USSDView #StudentViewSet


# router = routers.DefaultRouter()
# router.register('students', StudentRudView, 'students')

# urlpatterns = router.urls
urlpatterns = [
	path('student/<pk>', StudentRudView.as_view(), name='s_detail'),
	path('create', TransactionCreateView.as_view(), name='t_create'),
	path('student/', StudentListView.as_view(), name='s_list'),
	path('call/', CallbackView.as_view(), name='call_'),
	path('ssup/', WhatsappView.as_view()),
]