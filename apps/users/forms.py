from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, required=True, error_messages=dict(max_length='用户名过长',
                                                                                               min_length='用户名过短'))
    password = forms.CharField(max_length=20, min_length=8, required=True)
    password2 = forms.CharField(max_length=20, min_length=8, required=True)

    email = forms.CharField(max_length=32, required=True)
    email_code = forms.CharField(max_length=32)

    # 图形验证码不能再form表单验证，是在发送短信验证吗时候验证

    # sms_code = forms.CharField(max_length=6, min_length=6, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("两次密码不一致")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)
    checkbox = forms.BooleanField(required=False)
