from rest_framework import serializers
from .models import Employee
import re

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'   

# .........Field-level validation...........

    def validate_email(self, value):
        
        if not value.endswith('@company.com'):
            raise serializers.ValidationError("Email must be from @company.com domain.")
        return value

    def validate_salary(self, value):
       
        if value <= 0:
            raise serializers.ValidationError("Salary must be a positive number.")
        return value

    def validate_emp_id(self, value):
        
        pattern = r"^EMP_\d+$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("emp_id must be in format 'EMP' followed by numbers. Example: EMP_101")
        return value

