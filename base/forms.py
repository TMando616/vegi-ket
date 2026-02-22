from django import forms
from django.contrib.auth import get_user_model

class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', )

    # clean_passwordをoverride
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.get_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
