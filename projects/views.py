from django.shortcuts import render, redirect, HttpResponse
from projects.forms import Projectsform,Dontate
from projects.models import Projects, review
from django.contrib.auth.models import User



def index(request):
    return render(request, 'projects/index.html')


def projects(request):
    pro = Projects.objects.all()
    return render(request, 'projects/projects.html', context={"project": pro})


def Createform(request):
    form = Projectsform()


    if request.method == "POST":
        form = Projectsform(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            title = form.cleaned_data['title']
            details = form.cleaned_data['details']
            image1 = form.cleaned_data['image1']
            # image2 = form.cleaned_data['image2']
            # image3= form.cleaned_data['image3']
            total_target = form.cleaned_data['total_target']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            product = Projects()
            product.title = title
            product.details = details
            product.image = image1
            # product.image2 = image2
            # product.image3 = image3
            product.total_target = total_target
            product.start_time = start_time
            product.end_time = end_time
            product.save()
        return redirect('projects')
    return render(request, 'projects/createforum.html', context={'form': form})


def View(request, id):
    # filtered_Product= filter(lambda pro: pro['id'] == id, Product)
    filtered_Product = Projects.objects.filter(id=id)
    print(filtered_Product)
    filtered_Product = list(filtered_Product)
    print(filtered_Product)
    if filtered_Product:
        print(filtered_Product[0])
        return render(request, 'projects/view.html', context={"product": filtered_Product[0]})

    return HttpResponse("No such student Student ")


def review_page(request, id):

    item_details = Projects.objects.get(id=id)

    if request.method == 'POST':
        star_rating = request.POST.get('rating')
        item_review = request.POST.get('item_review')

        item_reviews = review(
            item=item_details, rating=star_rating, review_desp=item_review)
        item_reviews.save()

        rating_details = review.objects.filter(item=item_details)
        context = {'reviews': rating_details}
        return render(request, 'projects/addcomment.html', context)

    rating_details = review.objects.filter(item=item_details)
    context = {'reviews': rating_details}
    return render(request, 'projects/addcomment.html', context)
def Update(request,id):
    #  filtered_Product=Product.objects.filter(id=id)
     edited=Projects.objects.get(id=id)
     form =Dontate(request.POST ,request.FILES,instance=edited)
     if form.is_valid():
        total_target=form.cleaned_data['total_target']
        edited.total_target=total_target
        edited.save()
        return redirect("projects")

     return render(request,'projects/donate.html',context={"project":edited,"form":form}) 