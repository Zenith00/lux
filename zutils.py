def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer

def query_dict_softcase(dictionary: dict, key):
    if key in dictionary.keys():
        return dictionary[key]
    if not isinstance(key, str):
        raise KeyError(f"Key {key} not found in dict {dictionary}")
    case_insensitive_dict = {k.lower(): v for k, v in dictionary.values()}
    if key.lower() in case_insensitive_dict.keys():
        return case_insensitive_dict[key.lower()]

def magic_search(key):
    import inspect
    try:
        return dict(inspect.getmembers(
            inspect.stack()[-1][0]))["f_globals"][key]
    except KeyError:
        for i in inspect.stack()[::-1]:
            try:
                return dict(inspect.getmembers(i[0]))["f_locals"][key]
            except KeyError:
                pass
    raise KeyError("Could not find key " + key)


def execute(exec_type, statement, async_loop=None):
    return_val = None
    if exec_type == "exec":
        exec(statement)
    if exec_type == "eval":
        return_val = eval(statement)
    if exec_type == "aexec":
        ms = magic_search
        if not async_loop:
            async_loop = ms("client").loop
        indent = "    "
        indented_values = "\n".join([indent + statement for statement in statement.split("\n")])
        wrapped_to_run = ("import asyncio\n"
                          "async def main():\n"
                          f"{indented_values}\n\n"
                          "async_loop.create_task(main())")
        exec(wrapped_to_run, locals())
        return_val = f"Created task successfully"

    return return_val
