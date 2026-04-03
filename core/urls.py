from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-pdf/", views.upload_pdf, name="upload_pdf"),
    path("ask/", views.ask_question, name="ask_question"),
]
