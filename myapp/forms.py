from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Quiz
from .models import Question

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user
    from .models import Quiz

class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = [
            'title',
            'subject',
            'description',
            'duration',
            'total_marks'
        ]
class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            'quiz',
            'question',
            'option1',
            'option2',
            'option3',
            'option4',
            'correct_answer'
        ]
    