from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from pomadoro.models import PomadoroModel
#from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User

from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm

from django.utils import simplejson as json


#@ensure_csrf_cookie
def index(request):
    if request.user.is_authenticated():
        now = datetime.datetime.now()
        pomadoro = PomadoroModel.objects.filter(end__gt=now, squashed=False)
        if pomadoro:
            pomadoro = pomadoro[0]
            delta = pomadoro.end - datetime.datetime.now()
            pomadoro.total_seconds = delta.seconds
            #import pdb; pdb.set_trace()
            pomadoro.minutes = delta.seconds / 60
            pomadoro.seconds = delta.seconds % 60

        old_pomadoros = PomadoroModel.objects.filter(end__lt=now)

        return render_to_response('index.html', {'pomadoro': pomadoro,
                                  'old_pomadoros': old_pomadoros},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login?next=/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.clean_username()
            password = form.clean_password2()
            user = User.objects.create_user(username, username, password)
            user.save()
            return render_to_response('registered.html')

    form = UserCreationForm() # A form bound to the POST data
    return render_to_response('register.html', {'form': form},
                              context_instance=RequestContext(request))

@csrf_exempt
def pomadoro_start(request):
    if request.is_ajax():
        mimetype = 'application/javascript'
        pomadoro = PomadoroModel()
        pomadoro.end = datetime.datetime.now() + datetime.timedelta(seconds=25*60)
        pomadoro.save()
        from django.template.loader import render_to_string
        import pdb; pdb.set_trace()
        rendered = render_to_string('active_pomadoro.html', {'pomadoro': pomadoro})

        result = {'html': rendered}
        result = json.dumps(result)
        #data = serializers.serialize('json', PomadoroModel.objects.all())
        return HttpResponse(result, mimetype)
    else:
        return HttpResponse(status=400)
    return render_to_response('index.html', {})


@csrf_exempt
def pomadoro_squash(request):
    if request.is_ajax():
        now = datetime.datetime.now()
        pomadoro = PomadoroModel.objects.filter(end__gt=now, squashed=False)
        if pomadoro:
            pomadoro = pomadoro[0]
            pomadoro.squashed = True
            pomadoro.end = datetime.datetime.now()
            pomadoro.save()

            result = {'success' : True}
            answer = json.dumps(result)
            return HttpResponse(answer, mimetype='application/javascript')
    else:
        return HttpResponse(status=400)
    return render_to_response('index.html', {})
