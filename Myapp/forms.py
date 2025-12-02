from django import forms
from .models import Post14, profile,ContactMessage,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post14
        fields = ['caption', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['bio', 'profile_pic']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']