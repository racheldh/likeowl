from django import forms
from .models import Post, Comment

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'diary_date')
        #date를 선택하게 할 건가? my page에서만 작성하게 할 건가?
        widgets = {
            'diary_date': DateInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
