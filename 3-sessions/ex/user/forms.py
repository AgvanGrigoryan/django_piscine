from django.forms import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.PasswordInput(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def __is_user_already_registered(self, username):
        pass
        return False

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # if self.__is_user_already_registered(username):
        #     raise forms.ValidationError(
        #         "User with the same name already exists!"
        #     )
        if password != password_confirm:
            raise forms.ValidationError(
                "Passwords do not match"
            )
        return cleaned_data
