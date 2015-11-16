from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^new_algorithm$', views.new_algorithm, name='new_algorithm'),
	url(r'^get_parameter$', views.get_parameter, name='get_parameter'),
	url(r'^run_algorithm$', views.run_algorithm, name='run_algorithm'),
	url(r'^$', views.index, name='index'),
]