from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify


class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(budget=self)
        total_expense_amount = 0

        for expense in expense_list:
            total_expense_amount += expense.amount

        return self.budget - total_expense_amount
    

    
class Users(models.Model):
    budget = models.ForeignKey(Budget, on_delete=CASCADE, related_name='users')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name   

    def user_total(self):
        expense_list = Expense.objects.filter(budget=self.budget)
        user_expense = 0
        user_total = self.budget.budget // 2

        for expense in expense_list:
            if self.id == expense.user.id:
                user_expense += expense.amount

        return user_total - user_expense


class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=CASCADE)
    date = models.DateField()
    # date = models.CharField(max_length=10)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.description
