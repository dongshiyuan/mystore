from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "用户名", "required": "required"
    }),max_length=50, error_messages={"required": "username不能为空"})
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "密码", "required": "required"
    }),max_length=20, error_messages={"required": "password不能为空"})


class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "用户名", "required": "required"
    }), max_length=50, error_messages={"required": "username不能为空"})

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "placeholder": "邮箱", "required": "required"
    }), max_length=50, error_messages={"required": "email不能为空"})

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "密码", "required": "required"
    }), max_length=20, error_messages={"required": "password不能为空"})

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "确认密码", "required": "required"
    }), max_length=20, error_messages={"required": "password不能为空"})

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("所有项都为必填项")
        elif self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise forms.ValidationError("两次密码输入不一致")
        else:
            cleaned_data = super(RegForm, self).clean()
            return cleaned_data

