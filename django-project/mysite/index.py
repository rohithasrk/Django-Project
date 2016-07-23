from django.http import HttpResponse,HttpResponseRedirect

def tem(request):
	return HttpResponseRedirect("/polls/")
