from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from wopa_submitter.models import Reading, Assignment


def user_login(request):
    context = RequestContext(request)
    account_diasbled = False
    invalid_account = False
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                print "logged in"
                return HttpResponseRedirect('/')
            else:
                # return HttpResponse("Your WOPA account is disabled.")
                account_diasbled = True

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            invalid_account = True
            # return HttpResponse("Invalid login details supplied.")

    return render_to_response('wopa_submitter/auth/index.html',
                              {'account_diasbled': account_diasbled, 'invalid_account': invalid_account,
                               'username': username, 'password': password}, context)


@login_required
def user_logout(request):
    print "in logout"
    logout(request)
    return HttpResponseRedirect('/')


class Index(TemplateView, LoginRequiredMixin):
    template_name = "wopa_submitter/index.html"


# def register(request):
# context = RequestContext(request)
# registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         invitation_code = request.POST['code']
#         username = request.POST['username']
#         password = request.POST['password']
#         print invitation_code
#         if user_form.is_valid() & (invitation_code == '@wopa256'):
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             registered = True
#             published_assignments = Assignment.objects.filter(is_published=True)
#             for assignment in published_assignments:
#                 Submission.objects.create(student=user, assignment=assignment)
#             the_user = authenticate(username=username, password=password)
#             login(request, the_user)
#             return HttpResponseRedirect('/')
#         else:
#             print user_form.errors
#     else:
#         user_form = UserForm()
#
#     return render_to_response(
#         'wopa_submitter/auth/index.html',
#         {'user_form': user_form, 'user_errors': user_form.errors, 'registered': registered},
#         context)
#
#

class ReadingView(ListView, LoginRequiredMixin):
    template_name = "wopa_submitter/readings/index.html"
    model = Reading
    context_object_name = 'readings'


class AssignmentsView(ListView, LoginRequiredMixin):
    template_name = "wopa_submitter/assignments/index.html"
    model = Assignment
    context_object_name = "assignments"
