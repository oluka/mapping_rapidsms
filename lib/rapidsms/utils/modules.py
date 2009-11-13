#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import os, sys, traceback


def try_import(module_name):
    """
        Attempts to import and return *module_name*, returning None if an
        ImportError was raised. Unlike the standard try/except approach to
        optional imports, this method jumps through a few hoops to avoid
        catching ImportErrors raised from within *module_name*.

          # import a module from the python
          # stdlib. this should always work
          >>> try_import("csv") # doctest: +ELLIPSIS
          <module 'csv' from '...'>

          # attempt to import a module that
          # doesn't exist; no exception raised
          >>> try_import("spam.spam.spam") is None
          True
    """

    try:
        __import__(module_name)
        return sys.modules[module_name]

    except ImportError:

        # extract a backtrace, so we can find out where the exception was
        # raised from. if there is a NEXT frame, it means that the import
        # statement succeeded, but an ImportError was raised from _within_
        # the imported module. we must allow this error to propagate, to
        # avoid silently masking it with this optional import
        traceback = sys.exc_info()[2]
        if traceback.tb_next:
            raise

        # otherwise, the exception was raised
        # from this scope. *module_name* couldn't
        # be imported,which isn't such a big deal
        return None


def find_python_files(path):
    """
        Returns a list of the Python files (*.py) in a directory. Note that the
        existance of a Python source file does not guarantee that it is a valid
        module, because the directory (or any number of its parents) may not
        contain an __init__.py, rendering it a non-module.

        This seems a bit of an oversimplification, given that Python modules can
        live inside eggs and zips and the such, but if it's good enough for
        django.core.management.find_commands, it's good enough for me.

        Returns an empty list if the directory doesn't exist, couldn't be
        iterated, or contains no relevant files.
    """

    try:
        return [
            # trim the extension
            file[:-3]

            # iterate all files in the path
            # (doesn't include . and .. links)
            for file in os.listdir(path)

            # ignore __magic__ files and those
            # not ending with the .py suffix
            if not file.startswith("_")
            and file.endswith('.py')]

    except OSError:
        return []


def get_classes(module, superclass=None):
    """
        Returns a list of new-style classes defined in *module*, excluding
        _private and __magic__ names, and optionally filtering only those
        inheriting from *superclass*. Note that both arguments are actual
        modules, not names.

        This method only returns classes that were defined in *module*. Those
        imported from elsewhere are ignored.
    """

    objects = [
        getattr(module, name)
        for name in dir(module)
        if not name.startswith("_")]

    # filter out everything that isn't a new-style
    # class, or wasn't defined in *module* (ie, it
    # is imported from somewhere else)
    classes = [
        obj for obj in objects
        if isinstance(obj, type)
        and (obj.__module__ == module.__name__)]

    # if a superclass was given, filter the classes
    # again to remove those that aren't its subclass
    if superclass is not None:
        classes = [
            cls for cls in classes
            if issubclass(cls, superclass)]

    return classes


def get_class(module, superclass=None):
    """
        Returns the lone class contained by *module*, or raises a descriptive
        AttributeError if *module* contains zero or more than one class. This is
        useful when expecting a single class from a module without knowing its
        name, to avoid the usual constantly-named object in a module (eg. App,
        Backend, Command, Handler).
    """

    classes = get_classes(
        module, superclass)

    if len(classes) == 1:
        return classes[0]

    # the error message includes *superclass*
    # if one was given, otherwise it's generic
    desc = "subclasses of %s" % (superclass.__name__)\
        if superclass else "new-style classes"

    if len(classes) > 1:
        names = ", ".join([cls.__name__ for cls in classes])
        raise(AttributeError("Module %s contains multiple %s (%s)." %
            (module.__name__, desc, names)))

    else: # len < 1
        raise(AttributeError("Module %s contains no %s." %
            (module.__name__, desc)))


def get_module_path(module_name):
    """
        Imports *module_name*, and returns the absolute path to its directory.
        Raises AttributeError if the module is a Python file (*.py).

          # distutils is a directory in the stdlib
          # this probably won't work on \\windows\
          >>> get_module_path("distutils") # doctest: +ELLIPSIS
          '/.../python.../distutils'

          # csv is a single .py in the stdlib
          >>> get_module_path("csv")
          Traceback (most recent call last):
          ...
          AttributeError: Module named "csv" is not a directory
    """
    try:
        __import__(module_name)
        return sys.modules[module_name].__path__[0]

    # wrap with a better message
    except AttributeError:
        raise(AttributeError(
            'Module named "%s" is not a directory' %
                (module_name)))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
