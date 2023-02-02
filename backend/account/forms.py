from django import forms


class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    middle_name = forms.CharField(max_length=200)
    parent_id = forms.CharField(max_length=200, required=False)
    class_id = forms.CharField(max_length=200, required=False)
    roles = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    gender = forms.CharField(max_length=200)
    image = forms.ImageField(required=False)


class AddClassForm(forms.Form):
    name = forms.CharField(max_length=200)
    section = forms.CharField(max_length=200)
    teacher_id = forms.CharField(max_length=200)