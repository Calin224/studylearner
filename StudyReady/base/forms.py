from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants', 'host']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile','name','username','email','about']

class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1', 'password2']
