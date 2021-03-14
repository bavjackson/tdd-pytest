import pytest
from pytest_django.asserts import (
    assertTemplateUsed,
    assertContains,
    assertNotContains,
    assertRedirects,
)
from django.utils.html import escape

from lists.models import Item, List


# Home view
def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


# List view
def test_uses_list_template(client):
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")
    assertTemplateUsed(response, "list.html")


def test_displays_all_items(client):
    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)
    other_list = List.objects.create()
    Item.objects.create(text="other list item 1", list=other_list)
    Item.objects.create(text="other list item 2", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assertContains(response, "itemey 1")
    assertContains(response, "itemey 2")
    assertNotContains(response, "other list item 1")
    assertNotContains(response, "other list item 2")


def test_passes_correct_list_to_template(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = client.get(f"/lists/{correct_list.id}/")
    assert response.context["list"] == correct_list


# New list test
def test_can_save_a_POST_request(client):
    item_text = "A new list item"
    client.post("/lists/new", data={"item_text": item_text})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == item_text


def test_redirects_after_POST(client):
    response = client.post("/lists/new", data={"item_text": "A new list item"})
    new_list = List.objects.first()
    assertRedirects(response, f"/lists/{new_list.id}/")


def test_validation_errors_are_sent_back_to_home_page_template(client):
    response = client.post("/lists/new", data={"item_text": ""})

    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")
    expected_error = escape("You can't have an empty list item")
    assertContains(response, expected_error)


def test_invalid_list_items_arent_saved(client):
    client.post("/lists/new", data={"item_text": ""})
    assert List.objects.count() == 0
    assert Item.objects.count() == 0


# New item test
def test_can_save_a_post_request_to_an_existing_list(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


def test_redirects_to_list_view(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )
    assertRedirects(response, f"/lists/{correct_list.id}/")
