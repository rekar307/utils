import unittest
import util as ut


class TestUnflattenJson(unittest.TestCase):

    def test_unflatten_simple(self):
        flat_data = {"name": "John", "age": 30}
        expected = {"name": "John", "age": 30}
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_unflatten_nested_dict(self):
        flat_data = {"name": "John", "info.age": 30, "info.city": "New York"}
        expected = {"name": "John", "info": {"age": 30, "city": "New York"}}
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_unflatten_nested_list(self):
        flat_data = {
            "name": "John",
            "preferences.foods.0": "pizza",
            "preferences.foods.1": "sushi",
        }
        expected = {"name": "John", "preferences": {"foods": ["pizza", "sushi"]}}
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_unflatten_mixed(self):
        flat_data = {
            "name": "John",
            "info.age": 30,
            "info.address.city": "New York",
            "info.address.zipcode": "10001",
            "preferences.colors.primary": "blue",
            "preferences.colors.secondary": "green",
        }
        expected = {
            "name": "John",
            "info": {"age": 30, "address": {"city": "New York", "zipcode": "10001"}},
            "preferences": {"colors": {"primary": "blue", "secondary": "green"}},
        }
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_empty_dict(self):
        flat_data = {}
        expected = {}
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_nested_empty_dict(self):
        flat_data = {"info": {}}
        expected = {"info": {}}
        self.assertEqual(ut.unflatten_json(flat_data), expected)

    def test_flattened_with_lists(self):
        flat_data = {
            "info.address.0.city": "New York",
            "info.address.0.zipcode": "10001",
        }
        expected = {"info": {"address": [{"city": "New York", "zipcode": "10001"}]}}
        self.assertEqual(ut.unflatten_json(flat_data), expected)


if __name__ == "__main__":
    unittest.main()
