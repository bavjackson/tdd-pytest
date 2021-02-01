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


def test_can_save_a_POST_request(client):
    item_text = "A new list item"
    client.post("/", data={"item_text": item_text})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == item_text


def test_redirects_after_POST(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert response.status_code == 302
    assert response["location"] == "/"


def test_only_saves_items_when_necessary(client):
    client.get("/")
    assert Item.objects.count() == 0


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


def test_displays_all_list_items(client):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = client.get("/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode()


@pytest.mark.xfail
def test_azure_pipeline_fails_with_bad_test():
    assert 0
