from django.db import models

# Create your models here.

class Employee(models.Model):

    DESIGNATION_CHOICES = [
        ('developer', 'Developer'),
        ('manager', 'Manager'), 
        ('designer', 'Designer'),
    ]

    DEPARTMENT_CHOICES = [
        ('it', 'IT'),
        ('hr', 'HR Department'),
        ('sales', 'Sales'),
    ]

    emp_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


