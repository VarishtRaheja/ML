import importlib.util
def module_check(packages):
    """ Check for module import"""
    result = {}
    for module in packages:
        spec = importlib.util.find_spec(module)
        if spec is not None:
            result[module] = True
        else:
            result[module] = False
    return result
