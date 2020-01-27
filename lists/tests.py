from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

from pytest_django.asserts import assertTemplateUsed


def test_home_page_returns_correct_html(client):
    response = client.get("/")

    assertTemplateUsed(response, "home.html")
