from distutils.command.clean import clean
from xml.dom import ValidationErr
from django import forms

from .models import Category, Post, Comment


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


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        # exclude = ('author', 'created_date', 'published_date')

    def clean(self):
        categories = self.cleaned_data.get('categories')
        title = self.cleaned_data.get('title')
        text = self.cleaned_data.get('text')

        # category = "Sport"
        param = "Robotic"
        print(categories)
        for i in categories:

            if i.title == "Sport" and "olahraga" not in text or i.title == "Sport" and "olahraga" not in title:
                raise forms.ValidationError(
                    "Text and title must include Olahraga for Sport Category")
            elif i.title == param and param not in title:
                return self.add_error('title', "Title must include  'Robotic'")
                # return self.
            # elif  i.title in "Sport" and "olahraga" not in text :
            #     return self.add_error('text', "Text must include Olahraga")
            # elif  i.title in "Sport" and "olahraga"  not in title:
            #     return self.add_error('title', "Title must include Olahraga")

        return self.cleaned_data

        # print(categories, self.cleaned_data)

    # def clean_categories(self):
    #     categories = self.cleaned_data.get('categories')

    #     return categories

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
