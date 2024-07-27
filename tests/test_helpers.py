import pytest


def test_get_updated_subset_keys():
    from prevedict.conf.helpers import get_updated_subset_keys

    # Test case 1: Simple key-value updates
    full_dict = {"a": 1, "b": 2, "c": 3}
    subset_dict = {"a": 1, "b": 20, "c": 3}
    expected = {"b": True}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected

    # Test case 2: Nested dictionary updates
    full_dict = {"a": {"x": 10, "y": 20}, "b": 2}
    subset_dict = {"a": {"x": 10, "y": 25}, "b": 2}
    expected = {"a": {"y": True}}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected

    # Test case 3: No updates
    full_dict = {"a": 1, "b": 2}
    subset_dict = {"a": 1, "b": 2}
    expected = {}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected

    # Test case 4: All keys updated
    full_dict = {"a": 1, "b": 2}
    subset_dict = {"a": 10, "b": 20}
    expected = {"a": True, "b": True}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected

    # Test case 5: Nested dictionaries with no updates
    full_dict = {"a": {"x": 10, "y": 20}, "b": 2}
    subset_dict = {"a": {"x": 10, "y": 20}, "b": 2}
    expected = {}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected

    # Test case 6: Complex nested structure with mixed updates
    full_dict = {"a": {"x": 10, "y": 20, "z": {"m": 30}}, "b": 2}
    subset_dict = {"a": {"x": 15, "y": 20, "z": {"m": 35}}, "b": 3}
    expected = {"a": {"x": True, "z": {"m": True}}, "b": True}
    assert get_updated_subset_keys(full_dict, subset_dict) == expected


if __name__ == "__main__":
    pytest.main()
