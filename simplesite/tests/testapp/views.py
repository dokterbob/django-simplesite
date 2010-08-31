from django.http import HttpResponse
from django.template import Template, RequestContext

def myview(request):
    t = Template('')
    c = RequestContext(request)
    
    return HttpResponse(t.render(c))
