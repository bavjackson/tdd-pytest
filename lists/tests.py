from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from pytest_django.asserts import assertTemplateUsed

import pytest

from lists.views import home_page
from lists.models import Item


def test_home_page_returns_correct_html(client):
    response = client.get("/")

    print("the test is running")
    assertTemplateUsed(response, "home.html")


def test_can_save_a_POST_requrest(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert "A new list item" in response.content.decode()
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_saving_and_retrieving_items():
    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2
    assert saved_items[0].text == "The first (ever) list item"
    assert saved_items[1].text == "Item the second"


@pytest.mark.xfail
def test_azure_pipeline_fails_with_bad_test():
    assert 0
