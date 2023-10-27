from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from accounts.forms import AccountCreationForm, EmailAuthenticationForm, UserProfileForm, UserChangeForm
from accounts.models import UserProfile
from projects.models import Donation, Project, ProjectImage


def register(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data['email']

            plain_text_message = strip_tags(message)

            send_mail(mail_subject, plain_text_message,
                      'islamnady95@hotmail.com', [to_email], html_message=message)

            return render(request, 'accounts/register_confirm.html')
    else:
        form = AccountCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'accounts/activation_success.html')
        else:
            return render(request, 'accounts/activation_failure.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'accounts/activation_failure.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page or do what's needed upon successful login
            return HttpResponseRedirect(reverse('accounts.profile', args=[user.pk]))
        else:
            # Authentication failed, you can return an error message or redirect to a login page with an error message
            return render(request, 'accounts/login.html', {'error_message': 'Email or password is incorrect.'})
    else:
        # Display the login form for GET requests
        return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def profile(request, pk):
    user = User.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    projects = Project.objects.filter(user=user)
    donations = Donation.objects.filter(user=user)
    first_images = []

    for project in projects:
        first_image = ProjectImage.objects.filter(project=project).first()
        first_images.append(first_image)

    project_with_first_images = []

    for donation in donations:
        project = donation.project
        first_image = ProjectImage.objects.filter(project=project).first()
        project_with_first_images.append((project, first_image, donation))

    context = {
        'user': user,
        'user_profile': user_profile,
        'projects': projects,
        'donations': donations,
        'first_images': first_images,
        'project_with_first_images': project_with_first_images,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts.profile', args=[pk]))
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts.profile', args=[user.pk]))
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'accounts/edit_user.html', {'form': form, })


@login_required
def delete_account(request):
    if request.method == 'POST':
        if request.user.check_password(request.POST['password']):
            request.user.delete()
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Incorrect password. Please try again.')
    return render(request, 'accounts/delete_confirm.html')
