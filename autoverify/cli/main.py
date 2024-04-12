"""CLI entry point module."""

import argparse
import sys

from autoverify import __version__ as AV_VERSION
from autoverify.util.verifiers import get_all_complete_verifier_names

from install import (
    check_commit_hashes,
    try_install_verifiers,
    try_uninstall_verifiers,
)

from verify import verify_network


def _build_arg_parser() -> argparse.ArgumentParser:
    """Setup the cli arg options."""
    parser = argparse.ArgumentParser()

    # FIXME: This command and others are slow on bad hardware; Likely because
    # we are importing many elements from the package which takes a while.
    parser.add_argument("-V", "--version", action="version", version=AV_VERSION)
    parser.add_argument(
        "--check_versions",
        action="store_true",
        help="""Check if the commit hash for each installed verifier
        is the latest commit hash.""",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        help="""run <subcommand> --help for a list of available options""",
    )

    install_parser = subparsers.add_parser("install")
    uninstall_parser = subparsers.add_parser("uninstall")

    install_parser.add_argument(
        "install",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="install specified verifiers and exit",
    )

    uninstall_parser.add_argument(
        "uninstall",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="uninstall specified verifiers and exit",
    )

    experiment_parser = subparsers.add_parser("experiment")

    experiment_parser.add_argument(
        "type",
        metavar="experiment_type",
        nargs=1,
        choices=["single"],
        help="specify the type of experiment",
    )
    experiment_parser.add_argument(
        "verifier",
        metavar="verifier",
        nargs=1,
        choices=get_all_complete_verifier_names(),
        help="verifier to be used for verification",
    )
    experiment_parser.add_argument(
        "property",
        nargs=1,
        help="property file to be used for verification",
    )
    experiment_parser.add_argument(
        "network",
        nargs=1,
        help="network file to be used for verification",
    )

    return parser


def main():
    """Parse and process cli args."""
    parser = _build_arg_parser()
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.check_versions:
        check_commit_hashes()

    if hasattr(args, "install"):
        try_install_verifiers(args.install)
    elif hasattr(args, "uninstall"):
        try_uninstall_verifiers(args.uninstall)
    elif hasattr(args, "type"):
        # TODO: Add different types of experiments
        verify_network(args.verifier[0], args.property[0], args.network[0])


if __name__ == "__main__":
    main()
