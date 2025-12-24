from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'autocomplete': 'email'
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': '사용할 아이디를 입력하세요',
            'autocomplete': 'username'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': '비밀번호 (8자 이상)',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '비밀번호 확인',
            'autocomplete': 'new-password'
        })

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': '아이디',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': '비밀번호',
            'autocomplete': 'current-password'
        })


# 규리===========================================
# 마이페이지 이동시 비밀번호 확인 폼 추가(251222)
class PasswordConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력'}),
        label='비밀번호'
    )
# 규리===========================================