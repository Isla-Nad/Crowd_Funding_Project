from django.shortcuts import render, redirect, get_object_or_404
from categories.forms import CategoryForm, ReportForm, TagForm, DonationForm
#usersform
from .forms import UserForm
from categories.models import Category, Tag
from django.contrib.auth.decorators import user_passes_test
#to get list of all registered users
from django.contrib.auth.models import User
from projects.models import Donation, Report
from projects.models import Project
###
from accounts.views import *
def is_admin(user):
    return user.is_staff
##**********************counting*************************
#get number of all registerd users
total_users = User.objects.all().count()
total_categories = Category.objects.all().count()
total_tags = Tag.objects.all().count()
total_projects = Project.objects.all().count()

#********************************************************
@user_passes_test(is_admin)
def admin_home(request):
    counts ={'total_users':total_users, 
            'total_categories':total_categories,
            'total_tags':total_tags,
            'total_projects':total_projects,
            }
    return render(request, 'custom_admin/admin_home.html',counts)

#users list
def users_list(request):
    users = User.objects.all()
    return render(request, 'custom_admin/users/users_list.html', context={'users': users,'total_users':total_users})

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/categories/categories_list.html', context={'categories': categories})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'custom_admin/tags/tags_list.html', context={'tags': tags})


def category_create(request):
    category_form = CategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            return redirect('categories_list')
    return render(request, 'custom_admin/categories/category_create.html', context={'category_form': category_form})
#user create
def user_create(request):
    user_form = UserForm(request.POST)
    if request.method == "POST":
        if user_form.is_valid():
            user_form.save()
            return redirect('users_list')
    return render(request, 'custom_admin/users/user_create.html', context={'user_form': user_form})


def tag_create(request):
    tag_form = TagForm(request.POST, request.FILES)
    if request.method == "POST":
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    return render(request, 'custom_admin/tags/tag_create.html', context={'tag_form': tag_form})


def category_edit(request, id):
    category_to_edit = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category_form = CategoryForm(
            request.POST, request.FILES, instance=category_to_edit)
        if category_form.is_valid():
            category_form.save()
            return redirect('categories_list')
    else:
        category_form = CategoryForm(instance=category_to_edit)
    return render(request, 'custom_admin/categories/category_edit.html', context={'category_form': category_form})
#user_edit
def user_edit(request, id):
    user_to_edit = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(
            request.POST,instance=user_to_edit)
        if user_form.is_valid():
            user_form.save()
            return redirect('users_list')
    else:
        user_form = UserForm(instance=user_to_edit)
    return render(request, 'custom_admin/users/user_edit.html', context={'user_form': user_form})



def category_delete(request, id):
    category_to_delete = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category_to_delete.delete()
        return redirect('categories_list')
    return render(request, 'custom_admin/categories/category_delete.html')
#user delete
def user_delete(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('users_list')
    return render(request, 'custom_admin/users/user_delete.html')


def tag_edit(request, id):
    tag_to_edit = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        tag_form = TagForm(request.POST, request.FILES, instance=tag_to_edit)
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    else:
        tag_form = TagForm(instance=tag_to_edit)
    return render(request, 'custom_admin/tags/tag_edit.html', context={'tag_form': tag_form})


def tag_delete(request, id):
    tag_to_delete = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        tag_to_delete.delete()
        return redirect('tags_list')
    return render(request, 'custom_admin/tags/tag_delete.html')


@user_passes_test(is_admin)
def donation(request):
    donations = Donation.objects.all()
    return render(request, 'custom_admin/donations/donation.html', context={"donations": donations})


@user_passes_test(is_admin)
def edit_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect('donation')
    else:
        form = DonationForm(instance=donation)

    return render(request, 'custom_admin/donations/edit_donation.html', {'form': form})


@user_passes_test(is_admin)
def delete_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        donation.delete()
        return redirect('donation')

    return render(request, 'custom_admin/donations/delete_donation.html', {'donation': donation})


@user_passes_test(is_admin)
def create_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donation')
    else:
        form = DonationForm()

    return render(request, 'custom_admin/donations/create_donation.html', {'form': form})


@user_passes_test(is_admin)
def report(request):
    reports = Report.objects.all()
    return render(request, 'custom_admin/reports/report.html', context={"reports": reports})


@user_passes_test(is_admin)
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report')
    else:
        form = ReportForm(instance=report)

    return render(request, 'custom_admin/reports/edit_report.html', {'form': form})


@user_passes_test(is_admin)
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        report.delete()
        return redirect('report')

    return render(request, 'custom_admin/reports/delete_report.html', {'report': report})


@user_passes_test(is_admin)
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report')
    else:
        form = ReportForm()

    return render(request, 'custom_admin/reports/create_report.html', {'form': form})

##create new user
def create_user(request):
    return render(request, 'custom_admin/users/create_user.html')
