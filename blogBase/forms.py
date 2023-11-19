from django import forms
from .models import Comment

class CommentForm(forms.Form):
    text = forms.CharField(label='Comment',widget=forms.Textarea(attrs={'rows':3,'class':'form-control','placeholder':'评论'}))

    def save(self,article,user):
        comment = Comment.objects.create(text=self.cleaned_data.get('text',None),article=article,user=user)