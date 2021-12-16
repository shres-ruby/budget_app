from budget.forms import ExpenseForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Budget, Category, Expense, Users
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm
import json


def project_list (request):
    return render(request, 'budget/project_list.html')

        

def project_detail (request, project_slug):
    budget = get_object_or_404(Budget, slug=project_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(budget=budget)
        users_list = Users.objects.filter(budget=budget)
        return render(request, 'budget/project_detail.html', {'budget':budget, 'expense_list': budget.expenses.all(), 'category_list': category_list, 'users_list': users_list})

    elif request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            user_name = form.cleaned_data['user']

            category = get_object_or_404(Category, budget=budget, name=category_name)
            user = get_object_or_404(Users, budget=budget, name=user_name)

            Expense.objects.create(
                budget = budget,    
                date = date,
                description = description,
                amount =  amount,
                category = category,
                user = user
    
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(project_slug)


class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'budget/add-budget.html'
    
    fields = ('name', 'budget')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                budget = Budget.objects.get(id=self.object.id),
                name = category
            ).save()
            

        users = self.request.POST['usersString'].split(',')
        for user in users:
            Users.objects.create(
                budget = Budget.objects.get(id=self.object.id),
                name = user
            ).save()   
    
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return slugify(self.request.POST['name'])

