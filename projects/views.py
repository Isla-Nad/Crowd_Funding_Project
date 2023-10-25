from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Sum
from projects.forms import DonationForm, ProjectForm,  ReviewForm 
from projects.models import Donation, ProjectImage, Project, Review
from django.contrib.auth.models import User


def index(request):
    allProjects = Project.objects.all()
    allReviews = Review.objects.all()
    allImages = ProjectImage.objects.all()
    RatedProjects = []
    
    for oneproject in allProjects:
        ProjectRatings = [0]
        for review in allReviews:
            if oneproject.id == review.project.id:
                ProjectRatings.append(review.rating)
        ProjectRating = sum(ProjectRatings)/len(ProjectRatings)
        RatedProjects.append({ProjectRating:oneproject})
    sorted_projects = sorted(RatedProjects, reverse=True, key=lambda x: list(x.keys())[0])
    HighRatedProjects = [list(project.values())[0] for project in sorted_projects[:5]]
    
    
    #to get the latest 6 projects 
    ordered_projects = Project.objects.all().order_by('created_at')
    latest_projects = ordered_projects.reverse()[0:6]
       
        
    
    # print(HighRatedProjects)
    # print(latest_objects)
    
    if 'find'in request.GET:
        find=request.GET['find']
        pro=Project.objects.filter(title__icontains=find)
        return render(request, 'projects/search_results.html',context={"projects":pro})

        
    else :   
        pro=Project.objects.all()
        return render(request, 'projects/index.html',context={"HighRatedProjects":HighRatedProjects,"latest_projects":latest_projects,"projects":pro})
    
        
        
    


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
            cover = form.cleaned_data['cover']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            project = Project(user=user, title=title, details=details, total_target=total_target, cover = cover, category=category,
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


