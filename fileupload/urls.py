from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    # path('', views.mdash, name="home"),
    # path('view', views.show_file, name="view"),
    path('m-dash', views.mdash, name="mdash"),
    path('pageNo', views.Pageno, name="pageno"),
    path('JuncCharacter', views.junkChar, name="junkchar"),
    path('orderWise', views.alphaOrder, name="alphaOrder"),
    path('missingPages', views.missingpages, name="missingpages"),
    path('actionUrl', views.deleteAll),


]
