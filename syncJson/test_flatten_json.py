import unittest
import util as ut


class TestFlattenJson(unittest.TestCase):

    # def test_flatten_simple(self):
    #     data = {"name": "John", "age": 30}
    #     expected = {"name": "John", "age": 30}
    #     self.assertEqual(ut.flatten_json(data), expected)
    #
    # def test_flatten_nested_dict(self):
    #     data = {"name": "John", "info": {"age": 30, "city": "New York"}}
    #     expected = {"name": "John", "info.age": 30, "info.city": "New York"}
    #     self.assertEqual(ut.flatten_json(data), expected)
    #
    # def test_flatten_nested_list(self):
    #     data = {"name": "John", "preferences": {"foods": ["pizza", "sushi"]}}
    #     expected = {
    #         "name": "John",
    #         "preferences.foods.0": "pizza",
    #         "preferences.foods.1": "sushi",
    #     }
    #     self.assertEqual(ut.flatten_json(data), expected)
    #
    # def test_flatten_mixed(self):
    #     data = {
    #         "name": "John",
    #         "info": {"age": 30, "address": {"city": "New York", "zipcode": "10001"}},
    #         "preferences": {"colors": {"primary": "blue", "secondary": "green"}},
    #     }
    #     expected = {
    #         "name": "John",
    #         "info.age": 30,
    #         "info.address.city": "New York",
    #         "info.address.zipcode": "10001",
    #         "preferences.colors.primary": "blue",
    #         "preferences.colors.secondary": "green",
    #     }
    #     self.assertEqual(ut.flatten_json(data), expected)

    # def test_empty_dict(self):
    #     data = {}
    #     expected = {}
    #     self.assertEqual(ut.flatten_json(data), expected)

    def test_nested_empty_dict(self):
        data = {"info": {}}
        expected = {"info": {}}
        self.assertEqual(ut.flatten_json(data), expected)


if __name__ == "__main__":
    unittest.main()
