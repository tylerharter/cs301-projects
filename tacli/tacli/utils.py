import argparse
import contextlib
import inspect
import json
import os
from functools import wraps
from collections import OrderedDict

import structlog

import tacli.constants

log = structlog.get_logger()

@contextlib.contextmanager
def chdir(path):
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield os.getcwd()
    finally:
        os.chdir(old_path)

def pass_obj_as_args(fn):
    signature = inspect.signature(fn)
    params = signature.parameters

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if len(args) != 1 or (len(args) == 1 and not isinstance(args[0], argparse.Namespace)):
            result = fn(*args, **kwargs)
            return result

        obj = args[0]
        args = []
        for k, v in params.items():
            if hasattr(obj, k):
                args.append(getattr(obj, k))
                continue

            # the object doesn't exist, can use a default arg if present
            if v.default == inspect._empty:
                raise TypeError("object does not have attribute {}".format(k))

            args.append(v.default)

        result = fn(*args)
        return result

    return wrapper

def launch_editor(filename):
    editor = os.environ.get(tacli.constants.tacli_editor_env, "vim")
    cmd = "{} {}".format(editor, filename)
    os.system(cmd)

def launch_difftool(f1, f2):
    difftool = os.environ.get(tacli.constants.tacli_difftool_env, "vimdiff")
    cmd = "{} {} {}".format(difftool, f1, f2)
    os.system(cmd)

def dump_state(state):
    with open(tacli.constants.state_file, "w") as fp:
        json.dump(state, fp, indent=2)

def load_state(state):
    with open(tacli.constants.state_file) as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)
