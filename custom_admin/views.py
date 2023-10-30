from django.shortcuts import render, redirect, get_object_or_404
from custom_admin.forms import CategoryForm, ReportCommentForm, ReportForm, ReviewForm, TagForm, DonationForm, UserChangeForm, UserForm, UserProfileForm
from categories.models import Category, Tag
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from accounts.models import UserProfile
from projects.models import Donation, Project, Report, ReportComment, Review


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_home(request):
    total_users = User.objects.all().count()
    total_users_profiles = UserProfile.objects.all().count()
    total_categories = Category.objects.all().count()
    total_tags = Tag.objects.all().count()
    total_projects = Project.objects.all().count()
    total_reviews = Review.objects.all().count()
    total_donations = Donation.objects.all().count()
    total_projects_reports = Report.objects.all().count()
    total_comments_reports = ReportComment.objects.all().count()
    counts = {
        'total_users': total_users,
        'total_users_profiles': total_users_profiles,
        'total_categories': total_categories,
        'total_tags': total_tags,
        'total_projects': total_projects,
        'total_reviews': total_reviews,
        'total_donations': total_donations,
        'total_projects_reports': total_projects_reports,
        'total_comments_reports': total_comments_reports,
    }
    return render(request, 'custom_admin/admin_home.html', counts)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# users


@user_passes_test(is_admin)
def users_list(request):
    total_users = User.objects.all().count()
    users = User.objects.all()
    return render(request, 'custom_admin/users/users_list.html', context={'users': users, 'total_users': total_users})


@user_passes_test(is_admin)
def user_create(request):
    user_form = UserForm(request.POST)
    if request.method == "POST":
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('users_list')
    return render(request, 'custom_admin/users/user_create.html', context={'user_form': user_form})


@user_passes_test(is_admin)
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
    return render(request, 'custom_admin/users/user_edit.html', context={'user_form': user_form})


@user_passes_test(is_admin)
def user_delete(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    if user_to_delete == request.user:
        return redirect('users_list')
    elif request.method == 'POST':
        user_to_delete.delete()
        return redirect('users_list')
    return render(request, 'custom_admin/users/user_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# user_profiles


def user_profiles_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'custom_admin/user_profiles/user_profiles_list.html', context={'user_profiles': user_profiles})


@user_passes_test(is_admin)
def user_profile_create(request):
    user_profile_form = UserProfileForm(request.POST, request.FILES)
    if request.method == "POST":
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('user_profiles_list')
    return render(request, 'custom_admin/user_profiles/user_profile_create.html', context={'user_profile_form': user_profile_form})


@user_passes_test(is_admin)
def user_profile_edit(request, id):
    user_profile_to_edit = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile_to_edit)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('user_profiles_list')
    else:
        user_profile_form = UserProfileForm(instance=user_profile_to_edit)
    return render(request, 'custom_admin/user_profiles/user_profile_edit.html', context={'user_profile_form': user_profile_form})


@user_passes_test(is_admin)
def user_profile_delete(request, id):
    user_profile_to_delete = get_object_or_404(UserProfile, id=id)
    if request.method == 'POST':
        user_profile_to_delete.delete()
        return redirect('user_profiles_list')
    return render(request, 'custom_admin/user_profiles/user_profile_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# categories


@user_passes_test(is_admin)
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/categories/categories_list.html', context={'categories': categories})


@user_passes_test(is_admin)
def category_create(request):
    category_form = CategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            return redirect('categories_list')
    return render(request, 'custom_admin/categories/category_create.html', context={'category_form': category_form})


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
def category_delete(request, id):
    category_to_delete = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category_to_delete.delete()
        return redirect('categories_list')
    return render(request, 'custom_admin/categories/category_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# tags


@user_passes_test(is_admin)
def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'custom_admin/tags/tags_list.html', context={'tags': tags})


@user_passes_test(is_admin)
def tag_create(request):
    tag_form = TagForm(request.POST, request.FILES)
    if request.method == "POST":
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    return render(request, 'custom_admin/tags/tag_create.html', context={'tag_form': tag_form})


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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# projects


@user_passes_test(is_admin)
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'custom_admin/projects/projects_list.html', context={"projects": projects})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# reviews


@user_passes_test(is_admin)
def reviews_list(request):
    reviews = Review.objects.all()
    return render(request, 'custom_admin/reviews/reviews_list.html', context={"reviews": reviews})


@user_passes_test(is_admin)
def review_create(request):
    review_form = ReviewForm(request.POST, request.FILES)
    if request.method == "POST":
        if review_form.is_valid():
            review_form.save()
            return redirect('reviews_list')
    return render(request, 'custom_admin/reviews/review_create.html', context={'review_form': review_form})


@user_passes_test(is_admin)
def review_edit(request, id):
    review_to_edit = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review_form = ReviewForm(
            request.POST, request.FILES, instance=review_to_edit)
        if review_form.is_valid():
            review_form.save()
            return redirect('reviews_list')
    else:
        review_form = ReviewForm(instance=review_to_edit)
    return render(request, 'custom_admin/reviews/review_edit.html', context={'review_form': review_form})


@user_passes_test(is_admin)
def review_delete(request, id):
    review_to_delete = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        review_to_delete.delete()
        return redirect('reviews_list')
    return render(request, 'custom_admin/reviews/review_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# donation


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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# report project


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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# report comments

@user_passes_test(is_admin)
def report_comments_list(request):
    report_comments = ReportComment.objects.all()
    return render(request, 'custom_admin/report_comments/report_comments_list.html', context={"report_comments": report_comments})


@user_passes_test(is_admin)
def report_comment_create(request):
    report_comment_form = ReportCommentForm(request.POST, request.FILES)
    if request.method == "POST":
        if report_comment_form.is_valid():
            report_comment_form.save()
            return redirect('report_comments_list')
    return render(request, 'custom_admin/report_comments/report_comment_create.html', context={'report_comment_form': report_comment_form})


@user_passes_test(is_admin)
def report_comment_edit(request, id):
    report_comment_to_edit = get_object_or_404(ReportComment, id=id)
    if request.method == 'POST':
        report_comment_form = ReportCommentForm(
            request.POST, request.FILES, instance=report_comment_to_edit)
        if report_comment_form.is_valid():
            report_comment_form.save()
            return redirect('report_comments_list')
    else:
        report_comment_form = ReportCommentForm(
            instance=report_comment_to_edit)
    return render(request, 'custom_admin/report_comments/report_comment_edit.html', context={'report_comment_form': report_comment_form})


@user_passes_test(is_admin)
def report_comment_delete(request, id):
    report_comment_to_delete = get_object_or_404(ReportComment, id=id)
    if request.method == 'POST':
        report_comment_to_delete.delete()
        return redirect('report_comments_list')
    return render(request, 'custom_admin/report_comments/report_comment_delete.html')
