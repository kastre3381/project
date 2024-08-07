from collections import OrderedDict, defaultdict
"""Importing strftime in order to modify the date format"""
from time import strftime

from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce

"""Added count to dictionary"""
def summary_per_category(queryset):
    result = (
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'), c=Count('id'))
        .values_list('category_name', 's', 'c')
    )
    
    return OrderedDict((category_name, (s, c)) for category_name, s, c in result)

"""Function used in calculating the total amount spent"""
def total_amount_spent(queryset):
    return queryset.aggregate(total=Sum('amount'))['total'] or 0.0

"""Function used in summarizing the total month-year cost]"""
def summary_per_year_month(queryset):
    amount_dict = defaultdict(float)
    
    for record in queryset:
        year_month = record.date.strftime('%Y-%m')
        amount_dict[year_month] += float(record.amount)
        
    return OrderedDict(sorted(amount_dict.items()))