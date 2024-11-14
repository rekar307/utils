from itertools import chain, starmap
import re


def unpack(parent_key, parent_value):
    """Unpack one level of nesting in a dictionary"""
    try:
        items = parent_value.items()
    except AttributeError:
        # parent_value was not a dict, no need to flatten
        yield (parent_key, parent_value)
    else:
        for key, value in items:
            if type(value) == list:
                for k, v in enumerate(value):
                    yield parent_key + "." + key + "." + str(k), v
            else:
                yield parent_key + "." + key, value


def flatten_json(dictionary):
    if len(dictionary.values()) == 0:
        return dictionary
    while True:
        # Keep unpacking the dictionary until all value's are not dictionary's
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        if not any(isinstance(value, dict) for value in dictionary.values()):
            break
    return dictionary


def unflatten_json(json_dict):
    dictionary = {}
    for key, value in json_dict.items():
        temp_dict = dictionary
        tokens = re.findall(r"\w+", key)
        for count, (index, next_token) in enumerate(
            zip(tokens, tokens[1:] + [value]), 1
        ):
            value = (
                next_token
                if count == len(tokens)
                else [] if next_token.isdigit() else {}
            )
            if isinstance(temp_dict, list):
                index = int(index)
                while index >= len(temp_dict):
                    temp_dict.append(value)
            elif index not in temp_dict:
                temp_dict[index] = value
            temp_dict = temp_dict[index]
    return dictionary


def compare_json(json1, json2):
    return json1 == json2
