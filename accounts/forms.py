from django import forms
from .models import Register as RegModel


class RegisterForm(forms.ModelForm):

    class Meta:

        model = RegModel
        fields = ['user_name', 'password']

"""  def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        # Validation code goes here.
        return user_name"""