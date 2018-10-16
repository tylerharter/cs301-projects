#!/usr/bin/env python

import argparse
import logging
import json
import os
import sys

import structlog

import tacli.commands
import tacli.constants

def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    pull_parser = subparsers.add_parser("pull", help="Downloads code to be reviewed")
    pull_parser.add_argument("project_id", type=int, help="Integer value for the project to review")
    pull_parser.set_defaults(func=tacli.commands.pull_cmd)

    list_parser = subparsers.add_parser("list", help="Lists all reviews")
    list_parser.set_defaults(func=tacli.commands.list_cmd)

    refresh_parser = subparsers.add_parser("refresh", help="recomputes the metainfo in the .state file")
    refresh_parser.set_defaults(func=tacli.commands.refresh_cmd)

    edit_parser = subparsers.add_parser("edit", help="Opens up an editor for current review based on the EDITOR variable, defaults to vim")
    edit_parser.set_defaults(func=tacli.commands.edit_cmd)

    exec_parser = subparsers.add_parser("exec", help="Executes the current code being reviewed")
    exec_parser.set_defaults(func=tacli.commands.exec_cmd)

    jump_parser = subparsers.add_parser("jump", help="Jump to a specific review")
    jump_parser.add_argument("review_num", type=int, help="Integer value corresponding to the index from tacli list")
    jump_parser.set_defaults(func=tacli.commands.jump_cmd)

    prev_parser = subparsers.add_parser("prev", help="Moves to the previous review")
    prev_parser.set_defaults(func=tacli.commands.prev_cmd)

    next_parser = subparsers.add_parser("next", help="Moves to the next review")
    next_parser.set_defaults(func=tacli.commands.next_cmd)

    push_parser = subparsers.add_parser("push", help="Uploads reviews")
    push_parser.add_argument("--push-all", default=False, action="store_true")
    push_parser.set_defaults(func=tacli.commands.push_cmd)

    difftool_parser = subparsers.add_parser("difftool",
        help="difftool defaults to vimdiff unless {} is set".format(tacli.constants.tacli_difftool_env))
    difftool_parser.set_defaults(func=tacli.commands.difftool_cmd)

    diff_parser = subparsers.add_parser("diff", help="diff original modified")
    diff_parser.set_defaults(func=tacli.commands.diff_cmd)

    check_token_parser = subparsers.add_parser("check_token", help="checks if google token is valid")
    check_token_parser.set_defaults(func=tacli.commands.check_token_cmd)

    expand_parser = subparsers.add_parser("expand", help="expands all macros (defined in macros.txt) in current file")
    expand_parser.add_argument("--overwrite", default=False, action="store_true")
    expand_parser.set_defaults(func=tacli.commands.expand_cmd)


    dump_parser = subparsers.add_parser("dump", help="dumps the reviews for current file")
    dump_parser.set_defaults(func=tacli.commands.dump_cmd)


    # TODO delete_review
    # TODO pull reviews when pulling submissions

    return parser.parse_args()

def init_logger(level):
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(message)s", stream=sys.stderr, level=log_level,
    )
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.stdlib.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

def main():
    args = parse_args()
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    init_logger(log_level)
    log = structlog.get_logger()

    # pull is the only command that creates a new state file
    # so every other command should be run from within a state file (except for check_token)
    if args.func not in (tacli.commands.pull_cmd, tacli.commands.check_token_cmd):
        state_file = os.path.abspath(tacli.constants.state_file)
        if not os.path.exists(state_file):
            log.error("Could not find state file", loc=state_file)
            return
        with open(state_file) as fp:
            args.state = json.load(fp)

    args.func(args)

if __name__ == '__main__':
    main()
