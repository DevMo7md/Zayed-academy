from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, UserAnswer
from django.contrib.auth.decorators import login_required
from LP_app.models import *
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def quizs_home (request, foo):

    try:
        quizs = Question.objects.all()
        categories = Category.objects.all()
        # dashboard

        context = {
            'quizs': quizs,
            'categories': categories,
        }
        return render(request, 'Quizs/quizs_home.html', context)
    except:
        messages.error(request, "الفيديو المطلوب غير موجود!")
        return redirect('quizs_home')  # Redirect to main page if video doesn't exist
    
@login_required
def take_quiz(request, foo):
    foo = foo.replace('-', ' ')
    # تحقق مما إذا كان المستخدم قد أجاب بالفعل على الامتحان
    if UserAnswer.objects.filter(user=request.user).exists():
        return redirect('quiz_results')  # إذا كان قد أجاب بالفعل، توجيهه إلى صفحة النتائج
    if request.user.is_superuser or request.user.is_staff:
        category = Category.objects.get(name=foo)
        questions = Question.objects.filter(category=category)
        categories = Category.objects.all()

        if request.method == "POST":
            for question in questions:
                selected_choice_id = request.POST.get(str(question.id))
                if selected_choice_id:
                    selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                    UserAnswer.objects.create(user=request.user, question=question, selected_choice=selected_choice)
            return redirect('quiz_results')
        context = {
            'category':category,
            'questions':questions,
            'categories':categories
        }
    else:
        student = Student.objects.get(user=request.user)
        category = Category.objects.get(name=foo)
        grade = student.alsaf
        questions = Question.objects.filter(Q(category=category)&Q(grade=grade))

        if request.method == "POST":
            for question in questions:
                selected_choice_id = request.POST.get(str(question.id))
                if selected_choice_id:
                    selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                    UserAnswer.objects.create(user=request.user, question=question, selected_choice=selected_choice)
            return redirect('quiz_results')
        
    return render(request, 'quiz/take_quiz.html', context)


@login_required
def quiz_results(request):
    user_answers = UserAnswer.objects.filter(user=request.user)
    total_questions = user_answers.count()
    correct_answers = user_answers.filter(selected_choice__is_correct=True).count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    return render(request, 'Quizs/quiz_results.html', {
        'score': score,
        'total_questions': total_questions,
        'correct_answers': correct_answers
    })
