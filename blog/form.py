from django import forms

from .models import Category, Post


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


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.Textarea)
    # title = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        # exclude = ('author', 'created_date', 'published_date')


    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        title = self.cleaned_data.get('title')
        for i in categories:
            toStr = str(i)
            if toStr == "Robotic" and "Robotic" not in title:
                self.add_error('title',
                               "The Title Must Include 'Robotic' for Robotic Category")

            # print(i)

        return categories

    def clean_text(self):
        text = self.cleaned_data.get("text")

        if len(text) < 10:
            print(self.cleaned_data)

            raise forms.ValidationError("Minimal 10 Form TExt")
        return text

    def clean_title(self):
        title = self.cleaned_data.get('title')

        # if len(title) < 10:
        #     raise forms.ValidationError("Minimal 10 ")
        return title
