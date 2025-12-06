import django_filters
from django.db.models import IntegerField, F, Value
from django.db.models.functions import Replace, Upper, Cast
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    id_min = django_filters.CharFilter(method='filter_by_id_range', label="From EMP ID")
    id_max = django_filters.CharFilter(method='filter_by_id_range', label="To EMP ID")

    class Meta:
        model = Employee
        fields = ['designation', 'name', 'id_min', 'id_max']

    def get_initial(self):
        initial = super().get_initial()
        for key in initial.keys():
            initial[key] = ''  
        return initial

    def _annotate_emp_number(self, queryset):
       
        cleaned = Replace(
                        Replace(
                            Replace(Upper(F("emp_id")), Value("EMP"), Value("")),
                        Value("-"), Value("")),
                    Value("_"), Value(""))

        return queryset.annotate(
            emp_number=Cast(cleaned, IntegerField())
        )

    def filter_by_id_range(self, queryset, name, value):
        queryset = self._annotate_emp_number(queryset)

        def extract(v):
            digits = ''.join(filter(str.isdigit, str(v)))
            return int(digits) if digits else None

        id_min = self.data.get("id_min")
        id_max = self.data.get("id_max")

        if id_min:
            n = extract(id_min)
            if n is not None:
                queryset = queryset.filter(emp_number__gte=n)

        if id_max:
            n = extract(id_max)
            if n is not None:
                queryset = queryset.filter(emp_number__lte=n)

        return queryset



