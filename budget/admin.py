from django.contrib import admin
from .models import Budget, Expense, Category, Users


admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Users)
