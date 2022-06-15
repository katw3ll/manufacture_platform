from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from .views import CustomAuthToken

router = routers.DefaultRouter()
router.register(r'project', views.ProjectList)
router.register(r'composition', views.CompositiontList)
router.register(r'stock', views.StocktList)
# router.register(r'color', views.ColorsList)


urlpatterns = [
    #path('', views.index, name='index'),
    path('', include(router.urls)),

    url(r'token/login/', CustomAuthToken.as_view()),

    url(r'^add_colors', views.api_add_colors),
    url(r'^add_dim', views.api_add_dim),
    url(r'^add_classes', views.api_add_classes),
    url(r'^aadd_materials', views.api_add_materials),
    url(r'^add_parts', views.api_add_parts),
    url(r'^add_composition', views.api_add_composition),
    url(r'^add_rolls', views.api_add_rolls),
    url(r'^add_stock', views.api_add_stock),

    url(r'^get_projects', views.api_get_projects),

    #url(r'^project_cutting', views.api_get_projects),

    path('color/', views.ColorsList.as_view()),
    path('color/<int:pk>', views.ColorsList.as_view()),

    # path('project/', views.ProjectList.as_view()),
    # path('project/<int:pk>', views.ProjectList.as_view()),

    # url(r'^project_cutting', views.snippet_list),

    url(r'^composition_projects', views.composition_projects),

    url(r'^project_cutting2', views.snippet_list_new),

    url(r'^project_rollets', views.project_rollets),
    url(r'^assemble_the_roller', views.assemble_the_roller),

    

    url(r'^project_composition', views.project_composition),

    url(r'^cutting', views.cutting_new),
    url(r'^save_cutting', views.cutting_save),
    url(r'^remove_cutting', views.cutting_remove),
    url(r'^defect_cutting', views.defect_cutting),

    url(r'^materials_quantity', views.materials_quantity),

    url(r'^lengths_accessories', views.lengths_accessories),
    url(r'^lengths_search', views.lengths_search),
    url(r'^accessories_search', views.accessories_search),

    url(r'^upload_file', views.upload_file),


    url(r'^aadd_mat', views.add_materials),
    url(r'^show_materials_in_stock', views.show_materials_in_stock),

    url(r'^add_material_stock', views.add_material_stock),
    url(r'^delete_material_stock', views.delete_material_stock),


    url(r'^add_queue', views.add_queue),
    url(r'^get_queue', views.get_queue),
    url(r'^queue', views.queue),
    #path('queue', views.queue),
    url(r'^del_queue', views.del_queue),
    



   #  path('all-profiles', views.UserProfileListCreateView, name="all-profiles"),
   # # retrieves profile details of the currently logged in user
   #  path('profile/<int:pk>', views.userProfileDetailView, name="profile"),


    # url(r'^cutting', views.cutting_new),

    #path('project/', views.ProjectList.as_view()),

    #path('color/', views.ColorsList.as_view()),

    #path('^get_composition', include('api.url')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
