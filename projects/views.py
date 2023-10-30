from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.forms import ProjectReportForm, CommentReportForm
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from django.db.models import Sum, Avg, Count
from projects.forms import DonationForm, ProjectForm,  ReviewForm
from projects.models import Donation, ProjectImage, Project, Review
from categories.models import Category


def index(request):
    allProjects = Project.objects.all()
    allReviews = Review.objects.all()
    RatedProjects = []

    for oneproject in allProjects:
        ProjectRatings = [0]
        for review in allReviews:
            if oneproject.id == review.project.id:
                ProjectRatings.append(review.rating)
        ProjectRating = sum(ProjectRatings)/len(ProjectRatings)
        RatedProjects.append({ProjectRating: oneproject})
    sorted_projects = sorted(RatedProjects, reverse=True,
                             key=lambda x: list(x.keys())[0])
    HighRatedProjects = [list(project.values())[0]
                         for project in sorted_projects[:5]]

    ordered_projects = Project.objects.all().order_by('created_at')
    latest_projects = ordered_projects.reverse()[0:6]

    categories = Category.objects.all()

    pro = Project.objects.all()
    return render(request, 'projects/index.html', context={"HighRatedProjects": HighRatedProjects, "latest_projects": latest_projects, "projects": pro, "categories": categories})


def projects_search(request):
    find = request.GET.get('find', '')
    projects = Project.objects.filter(title__icontains=find)
    return render(request, 'projects/search_results.html', context={"projects": projects, 'search_term': find})


def category_details(request, category):
    mycategory = Category.objects.get(name=category)
    return render(request, 'projects/category_details.html', context={'mycategory': mycategory})


def project_list(request):
    projects = Project.objects.all()
    first_images = []

    for project in projects:
        first_image = ProjectImage.objects.filter(project=project).first()
        first_images.append(first_image)

    return render(request, 'projects/projects.html', context={'projects': projects, 'first_images': first_images, })


@login_required
def createform(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            details = form.cleaned_data['details']
            category = form.cleaned_data['category']
            total_target = form.cleaned_data['total_target']
            cover = form.cleaned_data['cover']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            project = Project(user=user, title=title, details=details, total_target=total_target, cover=cover, category=category,
                              start_time=start_time, end_time=end_time)
            project.save()
            tags = form.cleaned_data['tags']
            project.tags.set(tags)
            images = request.FILES.getlist('images')
            for image in images:
                project_image = ProjectImage(project=project, image=image)
                project_image.save()

            return redirect('projects.list')

    return render(request, 'projects/createforum.html', context={'form': form})


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    images = ProjectImage.objects.filter(project_id=id)
    reviews = Review.objects.filter(project_id=id)
    donations = Donation.objects.filter(project_id=id)
    overall_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    total_donations = donations.aggregate(Sum('donation_amount'))[
        'donation_amount__sum'] or 0
    similar_projects = Project.objects.filter(tags__in=project.tags.all()) \
        .exclude(id=project.id) \
        .annotate(tag_count=Count('tags')) \
        .order_by('-tag_count')[:4]

    if request.method == 'POST':
        if 'donate' in request.POST:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation_amount = donation_form.cleaned_data['donation_amount']
                if total_donations + donation_amount <= project.total_target:
                    donation = donation_form.save(commit=False)
                    donation.user = request.user
                    donation.project = project
                    donation.save()
                return redirect(reverse('project.view', args=[id]))

        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.user = request.user
                new_review.project = project
                new_review.save()
                return redirect(reverse('project.view', args=[id]))
    else:
        form = ReviewForm()
        donation_form = DonationForm()

    return render(request, 'projects/view.html', {
        'project': project,
        'images': images,
        'reviews': reviews,
        'form': form,
        'donation_form': donation_form,
        'total_donations': total_donations,
        'overall_rating': overall_rating,
        'similar_projects': similar_projects,
    })


@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if project.user == request.user:
        donations = Donation.objects.filter(project=project)
        total_donations = donations.aggregate(Sum('donation_amount'))[
            'donation_amount__sum'] or 0
        if total_donations < 0.25 * float(project.total_target):
            if request.method == 'POST':
                project.delete()
                return redirect(reverse('projects.list'))
            return render(request, 'projects/delete_project.html')
        else:
            messages.error(
                request, "You cannot delete this project as total donations exceed 25% of the target.")
            return redirect(reverse('project.view', args=[id]))
    else:
        messages.error(
            request, "Permission denied: You are not the creator of this project.")
        return redirect(reverse('project.view', args=[id]))


@login_required
def send_report_notification(report):
    subject = f"New Report from {report.user} for Project: {report.project.title}"
    message = f'''A new report has been submitted for the project: {report.project}
                for reason {report.reason}
                and detials {report.description}.'''
    from_email = settings.EMAIL_HOST_USER
    # from_email = 'islamnady95@hotmail.com'
    # List of admin email addresses
    recipient_list = ['kadem73980@tutoreve.com',]
    # recipient_list = ['islamnady95@gmail.com',]

    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


@login_required
def add_report(request, id):
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        # Create the report form instance with data from the request
        form = ProjectReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.project = project
            report.user = request.user
            report.save()
            send_report_notification(report)
            return redirect('projects.list')
    else:
        form = ProjectReportForm()

    context = {'reportform': form, 'project': project}
    return render(request, 'report/addreport.html', context)

#! Report comment view


def send_report_notification_comment(report):
    subject = f"New Report from {report.user} for user's comment: {report.review.user}"
    message = f'''A new report has been submitted for the Comment: {report.review.review_desp}
                for reason {report.reason}
                and detials {report.description}.'''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['kadem73980@tutoreve.com',]

    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


@login_required
def report_comment_view(request, id):
    review = Review.objects.get(id=id)

    if request.method == 'POST':
        form = CommentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.review = review
            report.save()
            send_report_notification_comment(report)
            return redirect('projects.list')
    else:
        form = CommentReportForm()

    context = {'reportform': form, 'review': review}
    return render(request, 'report/reportcomment.html', context)
