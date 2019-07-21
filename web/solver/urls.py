from django.urls import path

from . import views

urlpatterns = [
    path('<str:turn>/<str:code>', views.index, name='index'),
]
