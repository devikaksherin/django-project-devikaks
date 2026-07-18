
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import QuizForm
from .forms import QuestionForm

from .models import Quiz,Question,Result,CustomUser

from .models import Quiz, Result, CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def reports(request):

    total_quizzes = Quiz.objects.count()
    total_students = CustomUser.objects.filter(role="student").count()
    total_attempts = Result.objects.count()

    results = Result.objects.select_related("student", "quiz")

    context = {
        "total_quizzes": total_quizzes,
        "total_students": total_students,
        "total_attempts": total_attempts,
        "results": results,
    }

    return render(request, "reports.html", context)

@login_required
def manage_quizzes(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, "manage_quizzes.html", {"quizzes": quizzes})
@login_required
def result(request):

    latest_result = Result.objects.filter(
        student=request.user
    ).latest('submitted_at')

    return render(request, "result.html", {
        "result": latest_result
    })

@login_required
def start_quiz(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == "POST":

        score = 0

        for question in questions:

            selected_answer = request.POST.get(str(question.id))

            if selected_answer == question.correct_answer:
                score += 1

        Result.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            
            total_marks=len(questions)
        )

        return redirect("result")

    return render(request, "start_quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "duration": quiz.duration,
    })
@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_list.html", {"quizzes": quizzes})


@login_required
def add_question(request):

    if request.user.role != "admin":
        return redirect("student_dashboard")

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")

    else:
        form = QuestionForm()

    return render(request, "add_question.html", {"form": form})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):

    role = request.GET.get("role")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if role == "admin" and user.role != "admin":
                messages.error(request, "Only admins can login here.")
                return redirect("login")

            if role == "student" and user.role != "student":
                messages.error(request, "Only students can login here.")
                return redirect("login")

            login(request, user)

            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html", {"role": role})


@login_required
def admin_dashboard(request):

    if request.user.role != "admin":
        return redirect("student_dashboard")

    context = {
        "students": CustomUser.objects.filter(role="student").count(),
        "quizzes": Quiz.objects.count(),
        "questions": Question.objects.count(),
        "results": Result.objects.all(),
    }

    return render(request, "admin_dashboard.html", context)


def student_dashboard(request):
    return render(request, "student_dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def create_quiz(request):

    if request.user.role != "admin":
        return redirect("student_dashboard")

    if request.method == "POST":

        form = QuizForm(request.POST)

        if form.is_valid():

            quiz = form.save(commit=False)

            quiz.created_by = request.user

            quiz.save()

            return redirect("admin_dashboard")

    else:

        form = QuizForm()

    return render(request, "create_quiz.html", {"form": form})

