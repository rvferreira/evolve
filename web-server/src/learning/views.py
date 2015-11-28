from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def index(request):

	template = loader.get_template('learning/index.html')
	context = RequestContext(request, {
		'page_title': 'Wiki',
	})

	return HttpResponse(template.render(context))