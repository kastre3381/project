from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
"""Imported needed functions"""
from .reports import summary_per_category, total_amount_spent, summary_per_year_month

"""Modified view - added filtering by date, category and sorting records based on passed order.
Also added parameters to html"""
class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            categories = form.cleaned_data.get('categories')

            if categories:
                queryset = queryset.filter(category__in=categories)
            if name:
                queryset = queryset.filter(name__icontains=name)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
            
                
        sort_by = self.request.GET.get('sort_by', '')
        if sort_by in ['category', '-category', 'date', '-date']:
            queryset = queryset.order_by(sort_by)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent = total_amount_spent(queryset),
            summary_per_month_year = summary_per_year_month(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

