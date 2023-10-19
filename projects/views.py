from django.shortcuts import render, redirect
from projects.models import Projects
from projects.forms import Projectsform


def index(request):
    return render(request, 'projects/index.html')


def projects(request):
    pro = Projects.objects.all()
    return render(request, 'projects/projects.html', context={"project": pro})


def Createform(request):
    form = Projectsform()

    if request.method == "POST":
        form = Projectsform(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            details = form.cleaned_data['details']
            image = form.cleaned_data['image']
            total_target = form.cleaned_data['total_target']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            product = Projects()
            product.title = title
            product.details = details
            product.image = image
            product.total_target = total_target
            product.start_time = start_time
            product.end_time = end_time
            product.save()
        return redirect('projects')
    return render(request, 'projects/createforum.html', context={'form': form})
