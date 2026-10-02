from django import forms

from .models import Comment, Subscriber


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "your@email.com"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your comment..."
            }),
        }


class SubscriberForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your Email to Subscribe"
        }),
    )

    # class Meta:
    #     model = Subscriber
    #     fields = ["email"]
    #     validate_unique = False

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        return email
