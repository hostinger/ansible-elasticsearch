from filter_plugins.custom import (
    FilterModule,
    append_to_list,
    array_to_str,
    extract_role_users,
    filename,
    filter_reserved,
    modify_list,
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


def test_modify_list_substitutes_every_item():
    assert modify_list(["a-1", "a-2"], pattern="a-", replacement="b-") == [
        "b-1",
        "b-2",
    ]


def test_modify_list_honours_ignorecase():
    assert modify_list(["A-1"], pattern="a-", replacement="b-") == ["A-1"]
    assert modify_list(["A-1"], pattern="a-", replacement="b-", ignorecase=True) == [
        "b-1"
    ]


def test_append_to_list_accepts_a_list_or_a_comma_separated_string():
    assert append_to_list(["/data1", "/data2"], suffix="/es") == [
        "/data1/es",
        "/data2/es",
    ]
    assert append_to_list("/data1,/data2", suffix="/es") == ["/data1/es", "/data2/es"]


def test_append_to_list_keeps_empty_string_as_string_input():
    assert append_to_list("", suffix="/es") == ["/es"]


def test_array_to_str_joins_with_the_separator():
    assert array_to_str(["/data1", "/data2"]) == "/data1,/data2"
    assert array_to_str(["/data1", "/data2"], separator=";") == "/data1;/data2"


def test_extract_role_users_pairs_each_role_with_its_user():
    users = {
        "es_admin": {"roles": ["admin"]},
        "test_user": {"roles": ["power_user", "user"]},
        "no_roles": {"password": "changeMe"},
    }
    assert sorted(extract_role_users(users)) == [
        "admin:es_admin",
        "power_user:test_user",
        "user:test_user",
    ]


def test_extract_role_users_skips_excluded_users():
    users = {"es_admin": {"roles": ["admin"]}, "kibana": {"roles": ["kibana_system"]}}
    assert extract_role_users(users, exclude_users=["kibana"]) == ["admin:es_admin"]


def test_filename_strips_directory_and_extension():
    assert filename("/tmp/templates/basic.json") == "basic"


def test_filters_tolerate_omitted_arguments():
    """No filter should rely on a mutable default argument."""
    assert modify_list() == []
    assert append_to_list() == []
    assert array_to_str() == ""
    assert extract_role_users() == []
    assert filter_reserved() == []
    assert remove_reserved() == []
    assert filename() == ""
