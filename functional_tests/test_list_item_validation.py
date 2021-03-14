import pytest


@pytest.mark.xfail
@pytest.mark.functest
def test_cannot_add_empty_list_items(live_server, selenium):
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box

    # The home page refreshes, and there is an error message syaing
    # that list items cannot be blank

    # She tries again with some text for the item, which now works

    # Perversely, she now decides to submit a second blank list item

    # She recieves a similar warning on the list page

    # And she can correct it by filling some text in
    assert False, "Write this test"