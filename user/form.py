from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from comment.form import CommentForm

class ChangeNameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新昵称',
        max_length=24,
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'请输入新的昵称'}
        )
    )
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.use = kwargs.pop('user')
            super(ChangeNameForm,self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()#去除所有空格
        if nickname_new == '':
            raise ValidationError("新的昵称不能为空")
        return nickname_new

