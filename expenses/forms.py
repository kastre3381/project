from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    """Date from field"""
    date_from = forms.DateField(required=False, 
                                widget=forms.DateInput(attrs={'type': 'date'}))
    
    """Date to field"""
    date_to = forms.DateField(required=False, 
                              widget=forms.DateInput(attrs={'type': 'date'}))
    
    """Multiple choice fiels for filtering by category"""
    categories = forms.MultipleChoiceField(
        choices=[(category.id, category.name) for category in Category.objects.all()], 
        required=False, 
        widget=forms.CheckboxSelectMultiple)
    
    
    
    class Meta:
        model = Expense
        """Added fields"""
        fields = ('name', 'date_from', 'date_to', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
