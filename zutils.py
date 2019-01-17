def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def query_dict_softcase(dictionary : dict, key):
    if key in dictionary.keys():
        return dictionary[key]
    if not isinstance(key, str):
        raise KeyError(f"Key {key} not found in dict {dictionary}")
    case_insensitive_dict = {k.lower() : v for k,v in dictionary.values()}
    if key.lower() in case_insensitive_dict.keys():
        return case_insensitive_dict[key.lower()]
