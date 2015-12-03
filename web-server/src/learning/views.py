from django.http import HttpResponse
from django.template import RequestContext, loader

from django.utils.safestring import SafeString
import os
from django.conf import settings

# Create your views here.
def index(request):

	template = loader.get_template('learning/index.html')
	content = open(os.path.join(settings.STATIC_ROOT, 'learning/learning.json'), 'rb').read()

	context = RequestContext(request, {
		'page_title': 'Wiki',
		'content': SafeString(content),
	})

	return HttpResponse(template.render(context))