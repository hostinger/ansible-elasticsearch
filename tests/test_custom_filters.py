from filter_plugins.custom import (
    FilterModule,
    filter_reserved,
    remove_reserved,
)

ENTRIES = {
    "elastic": {"metadata": {"_reserved": True}},
    "kibana": {"metadata": {"_reserved": True}},
    "custom_user": {"metadata": {"_reserved": False}},
    "no_reserved_key": {"metadata": {"other": "value"}},
    "no_metadata": {"roles": ["admin"]},
}


def test_filter_reserved_returns_only_reserved_entries():
    assert sorted(filter_reserved(ENTRIES)) == ["elastic", "kibana"]


def test_remove_reserved_returns_only_unreserved_entries():
    assert sorted(remove_reserved(ENTRIES)) == [
        "custom_user",
        "no_metadata",
        "no_reserved_key",
    ]


def test_filter_reserved_and_remove_reserved_are_complementary():
    assert sorted(filter_reserved(ENTRIES) + remove_reserved(ENTRIES)) == sorted(
        ENTRIES
    )


def test_empty_input_yields_empty_lists():
    assert filter_reserved({}) == []
    assert remove_reserved({}) == []


def test_filters_are_registered():
    filters = FilterModule().filters()
    assert filters["filter_reserved"] is filter_reserved
    assert filters["remove_reserved"] is remove_reserved
