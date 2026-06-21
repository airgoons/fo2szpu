# Native Dependencies
from types import SimpleNamespace
import os.path
import json
from operator import attrgetter

# External Dependencies
import dcs

def to_namespace(data):
    """Utility function to cleanly bring data into an object's namespace"""
    if isinstance(data, dict):
        return SimpleNamespace(**{
            k: to_namespace(v)
            for k, v in data.items()
        })
    return data

def UnitMap(path):
    """Imports unit mapping data from a json"""
    # Input Validation
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise RuntimeError("Path does not exist or is not a file [{0}]".format(self._path))

    data = {}
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)

            return SimpleNamespace(**{k: to_namespace(v) for k, v in data.items()})
    except:
        print("ERROR:  JSON mangled [{0}]".format(path))
        raise

def nation_unit_map_to_pydcs_units(string_data):
    """Parses unit/quantity strings from within the dataset to a list of pydcs objects"""
    # expectation is a comma separated string of the form "pydcs_unit_object, quantity"

    try:
        unit_str, qty_str = [item.strip() for item in string_data.split(",")]  # ignore whitespace
    except:
        print("ERROR:  mangled data [{0}]".format(string_data))
        raise

    try:
        unit_ref = attrgetter(unit_str)(dcs)
        quantity = int(qty_str)

        return (unit_ref, quantity)
    
    except:
        print("ERROR:  mangled data --- unit_str={0} | qty_str={1}".format(unit_str, qty_str))
        raise


if __name__ == "__main__":
    unit_map = UnitMap("unit_map.json")  # TODO: Add input argument
    
    unit_ref, qty = nation_unit_map_to_pydcs_units("vehicles.AirDefence.SA_11_Buk_CC_9S470M1, 1")
    print(unit_ref)


