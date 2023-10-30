from django.shortcuts import render, redirect, get_object_or_404
from custom_admin.forms import CategoryForm, ReportForm, TagForm, DonationForm, UserChangeForm, UserForm
from categories.models import Category, Tag
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from accounts.models import UserProfile
from projects.models import Donation, Project, Report, ReportComment, Review


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'custom_admin/admin_home.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# users


def users_list(request):
    users = User.objects.all()
    return render(request, 'custom_admin/users_list.html', context={'users': users})


def user_create(request):
    user_form = UserForm(request.POST)
    if request.method == "POST":
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('users_list')
    return render(request, 'custom_admin/user_create.html', context={'user_form': user_form})


def user_edit(request, id):
    user_to_edit = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserChangeForm(
            request.POST, request.FILES, instance=user_to_edit)
        if user_form.is_valid():
            user_form.save()
            return redirect('users_list')
    else:
        user_form = UserChangeForm(instance=user_to_edit)
    return render(request, 'custom_admin/user_edit.html', context={'user_form': user_form})


def user_delete(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('users_list')
    return render(request, 'custom_admin/user_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# user_profiles


def user_profiles_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'custom_admin/user_profiles_list.html', context={'user_profiles': user_profiles})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# categories


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/categories_list.html', context={'categories': categories})


def category_create(request):
    category_form = CategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            return redirect('categories_list')
    return render(request, 'custom_admin/category_create.html', context={'category_form': category_form})


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
    return render(request, 'custom_admin/category_edit.html', context={'category_form': category_form})


def category_delete(request, id):
    category_to_delete = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category_to_delete.delete()
        return redirect('categories_list')
    return render(request, 'custom_admin/category_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# tags


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'custom_admin/tags_list.html', context={'tags': tags})


def tag_create(request):
    tag_form = TagForm(request.POST, request.FILES)
    if request.method == "POST":
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    return render(request, 'custom_admin/tag_create.html', context={'tag_form': tag_form})


def tag_edit(request, id):
    tag_to_edit = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        tag_form = TagForm(request.POST, request.FILES, instance=tag_to_edit)
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    else:
        tag_form = TagForm(instance=tag_to_edit)
    return render(request, 'custom_admin/tag_edit.html', context={'tag_form': tag_form})


def tag_delete(request, id):
    tag_to_delete = get_object_or_404(Tag, id=id)
    if request.method == 'POST':
        tag_to_delete.delete()
        return redirect('tags_list')
    return render(request, 'custom_admin/tag_delete.html')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# projects


@user_passes_test(is_admin)
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'custom_admin/projects_list.html', context={"projects": projects})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# reviews


@user_passes_test(is_admin)
def reviews_list(request):
    reviews = Review.objects.all()
    return render(request, 'custom_admin/reviews_list.html', context={"reviews": reviews})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# donation


@user_passes_test(is_admin)
def donation(request):
    donations = Donation.objects.all()
    return render(request, 'custom_admin/donation.html', context={"donations": donations})


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

    return render(request, 'custom_admin/edit_donation.html', {'form': form})


@user_passes_test(is_admin)
def delete_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        donation.delete()
        return redirect('donation')

    return render(request, 'custom_admin/delete_donation.html', {'donation': donation})


@user_passes_test(is_admin)
def create_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donation')
    else:
        form = DonationForm()

    return render(request, 'custom_admin/create_donation.html', {'form': form})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# report project


@user_passes_test(is_admin)
def report(request):
    reports = Report.objects.all()
    return render(request, 'custom_admin/report.html', context={"reports": reports})


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

    return render(request, 'custom_admin/edit_report.html', {'form': form})


@user_passes_test(is_admin)
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        report.delete()
        return redirect('report')

    return render(request, 'custom_admin/delete_report.html', {'report': report})


@user_passes_test(is_admin)
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report')
    else:
        form = ReportForm()

    return render(request, 'custom_admin/create_report.html', {'form': form})


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# report comments

@user_passes_test(is_admin)
def report_comments_list(request):
    report_comments = ReportComment.objects.all()
    return render(request, 'custom_admin/report_comments_list.html', context={"report_comments": report_comments})
