from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email-Address'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your FirstName'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your LastName'}))
    # birth_date=forms.DateField(label='Birthdate',widget=forms.TextInput(attrs={'placeholder': 'B-date in (yyyy-mm-dd) Format'}))
    # mobile_number=forms.RegexField(regex=r'^\+?1?\d{9,15}$',error_messages=("Enter Valid Number"))
    # mobile_number=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number Here'}),label='Mobile No.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None 
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Your Unique Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Your Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Re-Enter Your Password'})
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class ProfileForm(forms.Form):
    picture = forms.ImageField()

