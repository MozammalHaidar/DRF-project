from django.urls import path
from .views import Employees, EmployeeDetail

# urlpatterns = [
#     path('employees/', Employees.as_view()),
#     path('employees/<int:pk>/', EmployeeDetail.as_view()),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewset

router = DefaultRouter()
router.register('employees', EmployeeViewset, basename='employees')

urlpatterns = [
    path('', include(router.urls)),
]
