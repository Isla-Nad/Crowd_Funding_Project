from django.shortcuts import render, redirect, get_object_or_404
from categories.forms import CategoryForm, TagForm ,DonationForm,ReportForm
from categories.models import Category, Tag 
from django.contrib.auth.decorators import user_passes_test
from projects.models import Donation,Report


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_home(request):
    category_form = CategoryForm()
    tag_form = TagForm()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        if 'category' in request.POST:
            category_form = CategoryForm(request.POST, request.FILES)
            if category_form.is_valid():
                category_form.save()
        elif 'tag' in request.POST:
            tag_form = TagForm(request.POST, request.FILES)
            if tag_form.is_valid():
                tag_form.save()
        else:
            for category in categories:
                category_id = category.id
                if f'edit_category_{category_id}' in request.POST:
                    category_to_edit = get_object_or_404(
                        Category, id=category_id)
                    category_form = CategoryForm(instance=category_to_edit)
                    if category_form.is_valid():
                        category_form.save()
                elif f'delete_category_{category_id}' in request.POST:
                    category_to_delete = get_object_or_404(
                        Category, id=category_id)
                    category_to_delete.delete()
                    return redirect('admin_home')

            for tag in tags:
                tag_id = tag.id
                if f'edit_tag_{tag_id}' in request.POST:
                    tag_to_edit = get_object_or_404(Tag, id=tag_id)
                    tag_form = TagForm(instance=tag_to_edit)
                    if tag_form.is_valid():
                        tag_form.save()
                elif f'delete_tag_{tag_id}' in request.POST:
                    tag_to_delete = get_object_or_404(Tag, id=tag_id)
                    tag_to_delete.delete()
                    return redirect('admin_home')

    return render(request, 'categories/admin_home.html', {'category_form': category_form, 'tag_form': tag_form, 'categories': categories, 'tags': tags})


########################################## donation admin ##################################################
@user_passes_test(is_admin)
def donation (request):
    donations = Donation.objects.all()
    return render(request,'categories/donation.html',context={"donations":donations})

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

    return render(request, 'categories/edit_donation.html', {'form': form})

@user_passes_test(is_admin)
def delete_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        donation.delete()
        return redirect('donation')  

    return render(request, 'categories/delete_donation.html', {'donation': donation})

@user_passes_test(is_admin)
def create_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donation')  
    else:
        form = DonationForm()

    return render(request, 'categories/create_donation.html', {'form': form})


###########################################################################################################


######################################### Report Admin #####################################################
@user_passes_test(is_admin)
def report (request):
    reports = Report.objects.all()
    return render(request,'categories/report.html',context={"reports":reports})


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

    return render(request, 'categories/edit_report.html', {'form': form})


@user_passes_test(is_admin)
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        report.delete()
        return redirect('report')  

    return render(request, 'categories/delete_report.html', {'report': report})



@user_passes_test(is_admin)
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report')  
    else:
        form = ReportForm()

    return render(request, 'categories/create_report.html', {'form': form})