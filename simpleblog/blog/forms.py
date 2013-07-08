from django import forms
from blog.models import *

class addblog(Forms.form):
	title = forms.CharField(max_length="30")
    description = forms.CharField(max_length = "200")
    blog = 