from django import forms



class RegisterForm(forms.Form):
    user_name = forms.fields.CharField(max_length=256)
    password = forms.fields.CharField(widget=forms.PasswordInput())
    # TODO: Add password verification field pw2
    class Meta:

        fields = ['user_name', 'password']

    # def clean_user_name(self):
    #     user_name = self.cleaned_data.get('user_name')
    #     # Validation code goes here.
    #     return user_name


class LoginForm(forms.Form):
    user_name = forms.fields.CharField(max_length=256)
    password = forms.fields.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['user_name', 'password']
