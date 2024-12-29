from django.urls import path
from . import views

app_name = "faqs"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("<slug:slug>", views.show, name="show"),
    path("<slug:slug>/edit", views.edit, name="edit"),
    path("<slug:slug>/delete", views.delete, name="delete"),
]
