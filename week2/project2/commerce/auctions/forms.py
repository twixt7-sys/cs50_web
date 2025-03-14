from django import forms
    
class CategoryForm(forms.Form):
    template_name = "forms/categories_form.html"
    category = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    
# implement create form
class CreateForm(forms.Form):
    template_name = "forms/create_form.html"
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    description = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    start_bid = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    image_url = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    category = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category...'})
    )
    