from django.urls import re_path

from apps.verifications import views

urlpatterns = [

    re_path(r'^email_codes/(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', views.CodeView.as_view()),
]
