from django.urls import re_path, path
from .views import Userfiles

urlpatterns = [
    re_path(r'^home/$', Userfiles.as_view()),

]
