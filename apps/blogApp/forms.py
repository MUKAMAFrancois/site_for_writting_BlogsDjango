from django import forms
from .models import BlogCategory


class BlogPostForm(forms.Form):
    title=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    category=forms.ModelMultipleChoiceField(queryset=BlogCategory.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

    

class UpdateBlogForm(forms.Form):
    title=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    category=forms.ModelMultipleChoiceField(queryset=BlogCategory.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(UpdateBlogForm,self).__init__(*args,**kwargs)

        if self.instance:
            self.initial['title'] = self.instance.title
            self.initial['content'] = self.instance.content
            self.initial['category'] = self.instance.category.all()
            self.initial['image'] = self.instance.image


class CommentForm(forms.Form):
    comment=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))



class ReactionForm(forms.Form):
    reaction = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

