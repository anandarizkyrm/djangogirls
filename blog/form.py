from distutils.command.clean import clean
from xml.dom import ValidationErr
from django import forms
from django.contrib.auth import authenticate, login, logout
from .models import Category, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ChangePasswordForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']

        # exclude = ['password1', 'password2', 'password']


class AuthForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Invalid username or password")
        else:
            login(self.request, user)
        if not user.is_active:
            raise forms.ValidationError("User is not active")

        return self.cleaned_data


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]

    def clean(self):
        text = self.cleaned_data["text"]

        text = text.replace("hello", "*****")

        self.cleaned_data['text'] = text

        return self.cleaned_data


class CategoryForm(forms.Form):
    title = forms.CharField(max_length=30)

    def clean_title(self):
        title = self.cleaned_data['title']
        categories = Category.objects.filter(title__icontains=title)

        if categories:
            raise forms.ValidationError("Sorry Category Already Exists")

        return title

    def save(self, commit=True):
        title = self.cleaned_data['title']
        category = Category()
        category.title = title

        if commit:
            category.save()
        return title


class FilterPostForm(forms.Form):
    search = forms.CharField(required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False)
    date_from = forms.DateField(required=False,
                                widget=forms.SelectDateWidget())
    date_to = forms.DateField(required=False, widget=forms.SelectDateWidget())

    def clean(self):
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        if date_from and date_to and date_from > date_to:
            self.add_error('date_to', "Date to Must be after date from")
            self.add_error("date_from", "Date From must be before Date To")


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        # exclude = ('author', 'created_date', 'published_date')

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')

        print(categories)

        if categories and len(categories) > 3:
            return self.add_error('categories',
                                  "Sorry Cannot have more than 3 categories")
        return categories

    def clean_text(self):
        text = self.cleaned_data.get("text")

        if "saya" in text:
            return self.add_error('text', f"Text must not include saya")

        return text

    def clean_title(self):
        title = self.cleaned_data.get('title')

        x = "saya"
        if x in title:
            return self.add_error('title', f"Title must not include {x}")

        return title

    def clean(self):
        categories = self.cleaned_data.get('categories')
        title = self.cleaned_data.get('title')
        text = self.cleaned_data.get('text')

        # category = "Sport"
        param = "Robotic"
        if categories:
            for i in categories:

                if i.title == "Sport" and "olahraga" not in text or i.title == "Sport" and "olahraga" not in title:
                    raise forms.ValidationError(
                        "Text and title must include Olahraga for Sport Category"
                    )
                elif i.title == param and param not in title:
                    return self.add_error('title',
                                          "Title must include  'Robotic'")
                    # return self.
                # elif  i.title in "Sport" and "olahraga" not in text :
                #     return self.add_error('text', "Text must include Olahraga")
                # elif  i.title in "Sport" and "olahraga"  not in title:
                #     return self.add_error('title', "Title must include Olahraga")

        return self.cleaned_data

        # print(categories, self.cleaned_data)
