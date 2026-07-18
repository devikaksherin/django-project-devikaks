from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    path("add_question/", views.add_question, name="add_question"),
    path("quiz_list/", views.quiz_list, name="quiz_list"),
    path("start_quiz/<int:quiz_id>/", views.start_quiz, name="start_quiz"),
    path("result/", views.result, name="result"),
    path("reports/", views.reports, name="reports"),
    

    
]
