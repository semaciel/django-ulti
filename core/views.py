from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.contrib import messages
# messages.add_message(request, messages.SUCCESS, "{}".format('Message!'))
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from core.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class HomePageView(TemplateView):
    template_name = "core/home.html"

class AboutPageView(TemplateView):
    template_name = "core/about.html"

class ContactPageView(TemplateView):
    template_name = "core/contact.html"

def handle_not_found(request, exception):
    return render(request, 'not-found.html')

def handle_server_error(request):
    return render(request, 'server-error.html')

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_custom_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


# @auth_user_should_not_access
# def register(request):
#     if request.method == "POST":
#         context = {'has_error': False, 'data': request.POST}
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#
#         if len(password) < 6:
#             messages.add_message(request, messages.ERROR,
#                                  'Password should be at least 6 characters')
#             context['has_error'] = True
#
#         if password != password2:
#             messages.add_message(request, messages.ERROR,
#                                  'Password mismatch')
#             context['has_error'] = True
#
#         if not validate_email(email):
#             messages.add_message(request, messages.ERROR,
#                                  'Enter a valid email address')
#             context['has_error'] = True
#
#         if not username:
#             messages.add_message(request, messages.ERROR,
#                                  'Username is required')
#             context['has_error'] = True
#
#         if User.objects.filter(username=username).exists():
#             messages.add_message(request, messages.ERROR,
#                                  'Username is taken, choose another one')
#             context['has_error'] = True
#
#             return render(request, 'authentication/register.html', context, status=409)
#
#         if User.objects.filter(email=email).exists():
#             messages.add_message(request, messages.ERROR,
#                                  'Email is taken, choose another one')
#             context['has_error'] = True
#
#             return render(request, 'authentication/register.html', context, status=409)
#
#         if context['has_error']:
#             return render(request, 'authentication/register.html', context)
#
#         user = User.objects.create_user(username=username, email=email)
#         user.set_password(password)
#         user.save()
#
#         if not context['has_error']:
#
#             send_activation_email(user, request)
#
#             messages.add_message(request, messages.SUCCESS,
#                                  'We sent you an email to verify your account')
#             return redirect('login')
#
#     return render(request, 'authentication/register.html')
#
#
# @auth_user_should_not_access
# def login_user(request):
#
#     if request.method == 'POST':
#         context = {'data': request.POST}
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user and not user.is_email_verified:
#             messages.add_message(request, messages.ERROR,
#                                  'Email is not verified, please check your email inbox')
#             return render(request, 'authentication/login.html', context, status=401)
#
#         if not user:
#             messages.add_message(request, messages.ERROR,
#                                  'Invalid credentials, try again')
#             return render(request, 'authentication/login.html', context, status=401)
#
#         login(request, user)
#
#         messages.add_message(request, messages.SUCCESS,
#                              f'Welcome {user.username}')
#
#         return redirect(reverse('home'))
#
#     return render(request, 'authentication/login.html')
#
#
# def logout_user(request):
#
#     logout(request)
#
#     messages.add_message(request, messages.SUCCESS,
#                          'Successfully logged out')
#
#     return redirect(reverse('login'))
#
#
# def activate_user(request, uidb64, token):
#
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#
#         user = User.objects.get(pk=uid)
#
#     except Exception as e:
#         user = None
#
#     if user and generate_token.check_token(user, token):
#         user.is_email_verified = True
#         user.save()
#
#         messages.add_message(request, messages.SUCCESS,
#                              'Email verified, you can now login')
#         return redirect(reverse('login'))
#
#     return render(request, 'authentication/activate-failed.html', {"user": user})







'''
class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
):
    template_name = "account/signup." + app_settings.TEMPLATE_EXTENSION
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "signup", self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(
            self.request, reverse("account_login"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret

'''
