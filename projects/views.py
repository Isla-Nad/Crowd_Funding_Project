from django.shortcuts import render,redirect,HttpResponse
from projects.forms import Projectsform
# from projects.forms import Project_Form
from projects.models import Projects,review
from django.contrib.auth.models import User
# from .forms import CommentForm


# Create your views here.
from projects.models import Projects
def projects(request):
    pro=Projects.objects.all()
    return render(request,'projects.html',context={"project":pro})
def Createform(request):
    form =Projectsform()
    
    if request.method=="POST":
        form=Projectsform(request.POST,request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            details=form.cleaned_data['details']
            image=form.cleaned_data['image']
            total_target=form.cleaned_data['total_target']
            start_time=form.cleaned_data['start_time']
            end_time=form.cleaned_data['end_time']
            product=Projects() 
            product.title=title
            product.details=details
            product.image=image
            product.total_target=total_target
            product.start_time=start_time
            product.end_time=end_time
            product.save()
        return redirect('projects')
    return render(request,'createforum.html',context={'form':form})
def View(request,id):
    # filtered_Product= filter(lambda pro: pro['id'] == id, Product)
    filtered_Product=Projects.objects.filter(id=id)
    print(filtered_Product)
    filtered_Product = list(filtered_Product)
    print(filtered_Product)
    if filtered_Product:
        print(filtered_Product[0])
        return render(request,'view.html',context={"product":filtered_Product[0]})

    return HttpResponse("No such student Student ")


    
def review_page(request,id):

    item_details = Projects.objects.get(id=id)
  
    if request.method == 'POST':
        star_rating = request.POST.get('rating')
        item_review = request.POST.get('item_review')

        item_reviews = review( item=item_details, rating=star_rating, review_desp = item_review)
        item_reviews.save()

        rating_details = review.objects.filter(item=item_details)
        context = {'reviews': rating_details}
        return render(request, 'addcomment.html', context)

    rating_details = review.objects.filter(item=item_details)
    context = {'reviews': rating_details}
    return render(request, 'addcomment.html', context)