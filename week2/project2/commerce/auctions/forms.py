from django import forms
    
class CategoryForm(forms.Form):
    template_name = "forms/custom_form.html"
    category = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )