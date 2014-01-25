"""
Various utilities for the TornadoRPC library.
"""

import inspect


def getcallargs(func, *positional, **named):
    """
    Simple implementation of inspect.getcallargs function in
    the Python 2.7 standard library.

    Takes a function and the position and keyword arguments and
    returns a dictionary with the appropriate named arguments.
    Raises an exception if invalid arguments are passed.
    """
    args, varargs, varkw, defaults = inspect.getargspec(func)

    final_kwargs = {}
    extra_args = []
    has_self = inspect.ismethod(func) and func.im_self is not None
    if has_self:
        args.pop(0)

    # (Since our RPC supports only positional OR named.)
    if named:
        for key, value in named.iteritems():
            arg_key = None
            try:
                arg_key = args[args.index(key)]
            except ValueError:
                if not varkw:
                    raise TypeError("Keyword argument '%s' not valid" % key)
            if key in final_kwargs.keys():
                message = "Keyword argument '%s' used more than once" % key
                raise TypeError(message)
            final_kwargs[key] = value
    else:
        for i in range(len(positional)):
            value = positional[i]
            arg_key = None
            try:
                arg_key = args[i]
            except IndexError:
                if not varargs:
                    raise TypeError("Too many positional arguments")
            if arg_key:
                final_kwargs[arg_key] = value
            else:
                extra_args.append(value)
    if defaults:
        for kwarg, default in zip(args[-len(defaults):], defaults):
            final_kwargs.setdefault(kwarg, default)
    for arg in args:
        if arg not in final_kwargs:
            raise TypeError("Not all arguments supplied. (%s)", arg)
    return final_kwargs, extra_args
