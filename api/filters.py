import django_filters
from django.db.models import IntegerField, F, Value
from django.db.models.functions import Replace, Upper, Cast
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')

    id_min = django_filters.CharFilter(method='filter_by_id_range', label="From EMP ID")
    id_max = django_filters.CharFilter(method='filter_by_id_range', label="To EMP ID")

    class Meta:
        model = Employee
        fields = ['designation', 'name', 'salary_min', 'salary_max', 'id_min', 'id_max']


    
    def get_initial(self):
        return {key: "" for key in super().get_initial().keys()}

    def _annotate_emp_number(self, qs):
        cleaned = Upper(F("emp_id"))
        cleaned = Replace(cleaned, Value("EMP"), Value(""))
        cleaned = Replace(cleaned, Value("-"), Value(""))
        cleaned = Replace(cleaned, Value("_"), Value(""))

        return qs.annotate(emp_num=Cast(cleaned, IntegerField()))

    def filter_by_id_range(self, qs, name, value):
        qs = self._annotate_emp_number(qs)

        def num(v):
            digits = "".join(filter(str.isdigit, str(v)))
            return int(digits) if digits else None

        id_min = num(self.data.get("id_min"))
        id_max = num(self.data.get("id_max"))

        if id_min is not None:
            qs = qs.filter(emp_num__gte=id_min)

        if id_max is not None:
            qs = qs.filter(emp_num__lte=id_max)

        return qs



