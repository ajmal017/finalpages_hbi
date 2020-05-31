from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from members.models import account_activation_token
from members.models import MemberProfile
from django.views.generic import View
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from listings.models import Listing
import validate_email
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError

from documents.forms import ProposalForm
from documents.models import Proposal

from listings.forms import ListingForm


def index(request):
    if request.user.is_authenticated:
        my_qs = MemberProfile.objects.filter(username=request.user)
        context = {"title": "index.html", 'blog_list': my_qs}
        return render(request, 'hbi-dashboard/dashboard.html', context)
    else:
        qs = Listing.objects.all()
        context = {"title": "index.html", 'blog_list': qs}
        return render(request, "hbi-homepage/index.html", context)


def upload2(request):
    if request.method == 'POST':
        my_qs = MemberProfile.objects.filter(username=request.user)
        title = request.POST.get('title')
        description = request.POST.get('description')
        pdf = request.POST.get('pdf')
        cover = request.POST.get('cover')
        print('10. title =', title)
        print('20. author =', my_qs[0].username)
        print('30. description =', description)
        print('40. pdf=', pdf)
        print('50. cover=', cover)
        newdoc = Proposal()
        newdoc.title = title
        newdoc.author = my_qs[0]
        newdoc.description = description
        newdoc.pdf = pdf
        newdoc.cover = cover
        newdoc.save()
        return redirect('dashboard')
    else:
        my_qs = MemberProfile.objects.filter(username=request.user)
        print('1. firstname=', my_qs[0].first_name)
        context = {"title": "mysettings.html", 'blog_list': my_qs[0]}
        return render(request, 'hbi-dashboard/upload2.html', context)



class MySettingsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            print("At GET: MySettingsView")
            my_qs = MemberProfile.objects.filter(username=request.user)
            print('1. first_name=', my_qs[0].first_name)
            print('2. items_per_page=', my_qs[0].items_per_page)
            context = {"title": "mysettings.html", 'blog_list': my_qs}
            return render(request, 'hbi-dashboard/mysettings.html', context)
        else:
            return render(request, 'hbi-homepage/index.html')

    def post(self, request):
        if request.user.is_authenticated:
            print("At POST: MySettingsView")
            my_qs = MemberProfile.objects.filter(username=request.user).get()
            print('3. last_name=', my_qs.last_name)
            print('4. items_per_page=', my_qs.items_per_page)
            radioinline = request.POST.get('radio-inline')
            print('5. radioinline=', radioinline)
            my_qs.items_per_page = radioinline
            my_qs.save()
            return render(request, 'hbi-dashboard/dashboard.html')
        else:
            return render(request, 'hbi-homepage/index.html')

@login_required
def mysettings_OLD(request):
    print("here are mysettings")
    if request.user.is_authenticated:
        my_qs = MemberProfile.objects.filter(username=request.user)
        for item in my_qs:
            print('1. items_per_page=', item.items_per_page)
    context = {"title": "mysettings.html", 'blog_list': my_qs}
    return render(request, 'hbi-dashboard/mysettings.html', context)

@login_required
def blank(request):
    if request.user.is_authenticated:
        qs = BlogPost.objects.all()
        context = {"title": "blank.html", 'blog_list': qs}
        return render(request, "hbi-dashboard/blank.html", context)

@login_required
def updatedocs(request):
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        context = {"title": "updatedocs.html", 'blog_list': my_qs}
        return render(request, "hbi-dashboard/sortable-nestable-lists.html", context)

def testcard(request):
    qs = Listing.objects.all()
    context = {"title": "testcard.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/cards.html", context)

def forecast(request):
    qs = Listing.objects.all()
    context = {"title": "testcard.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/cards.html", context)


def signup(request):
    qs = BlogPost.objects.all()
    context = {"title": "signup.html", 'blog_list': qs}
    return render(request, "signup/signup.html", context)

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        context = {"title": "dashboard.html", 'blog_list': my_qs}
        return render(request, "hbi-dashboard/dashboard.html", context)

@login_required
def list(request):
    if request.user.is_authenticated:
        qs = Listing.objects.all()
        context = {"title": "list.html", 'blog_list': qs }
        return render(request, "hbi-dashboard/list.html", context)

@login_required
def myprofile(request):
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        context = {"title": "profile.html", 'blog_list': my_qs}
        return render(request, "hbi-dashboard/myprofile.html", context)

def okr(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/new-blank.html", context)



def po(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "conceptmaster/index.html", context)


def demo(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "demo/index.html", context)

def about_page(request):
    return render(request, "about.html", {"title": "About"})

def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact us",
        "form": form
    }
    return render(request, "form.html", context)

class LoginView(View):
    def get(self, request):
        return render(request, 'hbi-homepage/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'username are required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error'] = True
        checkmember0 = MemberProfile.objects.filter(username=username).count()
        #print("username=", username)
        #print("count checkmember0=",checkmember0)
        if checkmember0 != 0:
            #print ("Member EXIST!")
            checkmember = MemberProfile.objects.get(username=username)
            #print('checkmember = ', checkmember)
            #print('checkmember is_active = ', checkmember.is_active)
            # user = authenticate(request, username=username, password=password)
            if checkmember is not None and checkmember.is_active == True:  # member exist and is_active
                #print("Member exist, is_active")
                user = authenticate(request, username=username, password=password)
                if not context['has_error'] and not user:
                    messages.add_message(request, messages.ERROR, 'Incorrect Password, Please Re-try')
                    context['has_error'] = True
                    return render(request, 'hbi-homepage/login.html')
                else:
                    login(request, user)
                    return redirect('dashboard')
            elif checkmember is not None and checkmember.is_active == False:
                #print("Member exist but the account not active!")
                messages.info(request, mark_safe('Please check Email to activate your account.. <br> To re-send activation code, click <a href="http://127.0.0.1:8000/requestactivatecode/">HERE</a>'))

                #messages.add_message(request, messages.ERROR,'Your account is not yet activated.. Please check your Email to activate <a href="http://127.0.0.1:8000/members/password_change">Change Password  </a>')
                context['has_error'] = True
                return render(request, 'hbi-homepage/login.html')
            else:
                # the authentication system was unable to verify the username and password
                #print("Password is incorrect.")
                messages.add_message(request, messages.ERROR, 'Wrong Password, Please re-try')
                context['has_error'] = True
                return render(request, 'hbi-homepage/login.html')
        else:
            #print("Member DOES NOT EXIST!")
            messages.add_message(request, messages.ERROR, 'No Such Accounts, Please Re-Try')
            context['has_error'] = True
            return render(request, 'hbi-homepage/login.html')

class RegistrationView(View):
    def get(self, request):
        return render(request, 'hbi-homepage/signup.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if first_name == '':
            messages.add_message(request, messages.ERROR, 'please provide your first name')
            context['has_error'] = True
        if last_name == '':
            messages.add_message(request, messages.ERROR, 'please provide your last name')
            context['has_error'] = True
        #if email == '' or not validate_email(email):
        if email == '':
            messages.add_message(request, messages.ERROR, 'please provide a valid email')
            context['has_error'] = True
        if password == '' or password2 == '':
            messages.add_message(request, messages.ERROR, 'Passwords are required')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            context['has_error'] = True
        if MemberProfile.objects.filter(username=email).exists():
            messages.add_message(request, messages.ERROR, 'email is taken, use another one')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'hbi-homepage/signup.html', context, status=400)

        new_user = MemberProfile.objects.create_user(username=email, first_name=first_name, last_name=last_name, password=password2)
        #new_user.set_password(password)
        new_user.is_active = False
        new_user.save()

        current_site = get_current_site(request)
        mail_subject = 'HBI DigitalHub: Activate Your Account'
        message = render_to_string('hbi-homepage/acc_active_email.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token123': account_activation_token.make_token(new_user),
        })

        #to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'smilingideas@gmail.com', [email])

        #print("1. mail_subject=", mail_subject)
        #print("2. message=", message)
        #print("3. email=", [email])

        messages.add_message(request, messages.SUCCESS,'Please check your Email to activate your Account')
        return redirect('login')


class RequestActivationCode(View):
    def get(self, request):
        return render(request, "hbi-homepage/request_activation_code.html")

    def post(self, request):
        username = request.POST.get('username')
        checkmember0 = MemberProfile.objects.filter(username=username).count()
        #print('At requestActivationCode')
        #print('1. username=', username)
        #print("2. count checkmember0=", checkmember0)
        if checkmember0 != 0:
            #print ('3. User EXIST!!')
            checkmember = MemberProfile.objects.get(username=username)
            mail_subject = 'HBI DigitalHub: Activate Your Account (Immediate Action Needed)'
            current_site = get_current_site(request)
            message = render_to_string('hbi-homepage/acc_active_email.html', {
                'user': checkmember,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(checkmember.pk)),
                'token123': account_activation_token.make_token(checkmember),
                })

            # to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'smilingideas@gmail.com', [username])

            #print("1. mail_subject=", mail_subject)
            #print("2. message=", message)
            #print("3. username=", [username])
            messages.add_message(request, messages.SUCCESS, 'Please check your Email and activate your Account')
            return redirect('login')
        else:
            #print('3. User DOES NOT EXIST!!')
            messages.add_message(request, messages.SUCCESS, 'There is no such User registered in our System, please sign-up')
            return redirect('signup')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MemberProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        ##return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        messages.add_message(request, messages.SUCCESS, 'Thank you for your Email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

class RequestResetLinkView(View):
    def get(self, request):
        return render(request, 'hbi-homepage/request-reset-password.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        print('1. email = ', email)
        if email == '':
        #if not validate_email(email=email):
            messages.add_message(request, messages.ERROR, 'please provide an email')
            return render(request, 'hbi-homepage/request-reset-password.html', context, status=400)
        current_site = get_current_site(request)
        user = MemberProfile.objects.filter(username=email).first()
        print('2. user = ', user)
        if not user:
            messages.add_message(request, messages.ERROR, 'Details not found,please consider a signup')
            return render(request, 'hbi-homepage/request-reset-password.html', context, status=404)

        mail_subject = 'HBI DigitalHub: Reset Your Password'
        message = render_to_string('hbi-homepage/acc_finish-reset.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token123': account_activation_token.make_token(user),
        })

        # to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'smilingideas@gmail.com', [email])

        print("1. mail_subject=", mail_subject)
        print("2. message=", message)
        print("3. email=", [email])

        messages.add_message(request, messages.INFO, 'We have sent you an email with a link to reset your password')
        return render(request, 'hbi-homepage/login.html', context)


class CompletePasswordChangeView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = MemberProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MemberProfile.DoesNotExist):
            user = None
        if user is None or not account_activation_token.check_token(user, token):
            messages.add_message(request, messages.WARNING, 'Link is no longer valid,please request a new one')
            return render(request, 'hbi-homepage/reset-password.html', status=401)
        return render(request, 'hbi-homepage/change-password.html', context={'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        context = {'uidb64': uidb64, 'token': token}
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = MemberProfile.objects.get(pk=uid)
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if len(password) < 6:
                messages.add_message(request, messages.ERROR, 'Password should be at least 6 characters long')
                return render(request, 'hbi-homepage/change-password.html', context, status=400)
            if password != password2:
                messages.add_message(request, messages.ERROR, 'Passwords must match')
                return render(request, 'hbi-homepage/change-password.html', context, status=400)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.INFO, 'Password changed successfully,login with your new password')
            return redirect('login')
        except DjangoUnicodeDecodeError:
            messages.add_message(request, messages.ERROR, 'Something went wrong,you could not update your password')
            return render(request, 'hbi-homepage/change-password.html', context, status=401)
