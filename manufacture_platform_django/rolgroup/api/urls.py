from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^add_colors', views.api_add_colors),
    url(r'^add_dim', views.api_add_dim),
    url(r'^add_classes', views.api_add_classes),
    url(r'^add_materials', views.api_add_materials),
    url(r'^add_parts', views.api_add_parts),
    url(r'^add_composition', views.api_add_composition),
    url(r'^get_projects', views.api_get_projects),

    path('color/', views.ColorsList.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)