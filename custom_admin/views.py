from django.shortcuts import render, redirect, get_object_or_404
from categories.forms import CategoryForm, TagForm
from categories.models import Category, Tag
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'custom_admin/admin_home.html')


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/categories_list.html', context={'categories': categories})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'custom_admin/tags_list.html', context={'tags': tags})


def category_create(request):
    category_form = CategoryForm(request.POST, request.FILES)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            return redirect('categories_list')
    return render(request, 'custom_admin/category_create.html', context={'category_form': category_form})


def tag_create(request):
    tag_form = TagForm(request.POST, request.FILES)
    if request.method == "POST":
        if tag_form.is_valid():
            tag_form.save()
            return redirect('tags_list')
    return render(request, 'custom_admin/tag_create.html', context={'tag_form': tag_form})


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
