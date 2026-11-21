from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "body"]
        widgets = {
            "rating": forms.Select(choices=[(n, f"{n}/10") for n in range(10, 0, -1)]),
            "title": forms.TextInput(attrs={"placeholder": "Give your review a title"}),
            "body": forms.Textarea(attrs={"rows": 5, "placeholder": "What did you think about this movie?"}),
        }
