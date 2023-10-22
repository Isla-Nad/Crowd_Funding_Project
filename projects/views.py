from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Sum
from projects.forms import DonationForm, ProjectForm,  ReviewForm
from projects.models import Donation, ProjectImage, Project, Review


def index(request):
    return render(request, 'projects/index.html')


def project_list(request):
    projects = Project.objects.all()
    first_images = []

    for project in projects:
        first_image = ProjectImage.objects.filter(project=project).first()
        first_images.append(first_image)

    return render(request, 'projects/projects.html', context={'projects': projects, 'first_images': first_images, })


def Createform(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            details = form.cleaned_data['details']
            category = form.cleaned_data['category']
            total_target = form.cleaned_data['total_target']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            project = Project(user=user, title=title, details=details, total_target=total_target, category=category,
                              start_time=start_time, end_time=end_time)
            project.save()
            tags = form.cleaned_data['tags']
            project.tags.set(tags)
            images = request.FILES.getlist('images')
            for image in images:
                project_image = ProjectImage(project=project, image=image)
                project_image.save()
            print(project)

            return redirect('projects')

    return render(request, 'projects/createforum.html', context={'form': form})


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    images = ProjectImage.objects.filter(project_id=id)
    reviews = Review.objects.filter(project_id=id)
    donations = Donation.objects.filter(project_id=id)

    total_donations = donations.aggregate(Sum('donation_amount'))[
        'donation_amount__sum'] or 0

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
                return redirect(reverse('view', args=[id]))

        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.user = request.user
                new_review.project = project
                new_review.save()
                return redirect(reverse('view', args=[id]))
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
    })


from projects.forms import ProjectReportForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

def send_report_notification(report):
    subject = f"New Report from {report.user} for Project: {report.project.title}"
    message = f'''A new report has been submitted for the project: {report.project}
                for reason {report.reason}
                and detials {report.description}.'''  
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['kadem73980@tutoreve.com',]  # List of admin email addresses

    send_mail(subject, message, from_email, recipient_list,fail_silently=False)

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
            return redirect('projects') 
    else:
        form = ProjectReportForm()
    
    context = {'reportform': form, 'project': project}
    return render(request, 'report/addreport.html', context)
