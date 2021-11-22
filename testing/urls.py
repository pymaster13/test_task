from django.urls import path

from .views import SelectTest, TestInfo, Testing, TestResult

urlpatterns = [
    path('<test_id>/<question_id>/', Testing , name='testing'),
    path('<test_id>/result/', TestResult , name='test_result'),
    path('<test_id>/', TestInfo , name='test_info'),
    path('', SelectTest , name='all_tests'),
]
