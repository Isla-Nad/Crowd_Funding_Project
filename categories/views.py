from django.shortcuts import render, redirect, get_object_or_404
from categories.forms import CategoryForm, TagForm
from categories.models import Category, Tag
from django.contrib.auth.decorators import user_passes_test


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
