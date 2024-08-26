from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<str:foo>/', views.take_quiz, name='take_quiz'),
    path('quiz-results/<str:foo>', views.quiz_results, name='quiz_results'),
    path('quizs-home/', views.quizs_home, name='quizs_home'),
    path('teacher-quiz/', views.teacher_quiz, name='teacher_quiz'),
]
