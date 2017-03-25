from django.conf.urls import url

from . import views

app_name = "web_search"
urlpatterns = [
    url(r"^$", views.search_page, name="search_page")
]
