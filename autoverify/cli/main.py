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

from experiment import (
    verify_network,
    configure_algorithm,
    construct_portfolio,
    execute_portfolio,
)

from benchmark import run_benchmark


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
        dest="command",
    )

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument(
        "verifier",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="install specified verifiers and exit",
    )

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument(
        "verifier",
        nargs="+",
        choices=get_all_complete_verifier_names(),
        help="uninstall specified verifiers and exit",
    )

    verify_network_parser = subparsers.add_parser("verify_network")
    verify_network_parser.add_argument(
        "verifier",
        metavar="verifier",
        nargs=1,
        choices=get_all_complete_verifier_names(),
        help="verifier to be used for verification",
    )
    verify_network_parser.add_argument(
        "property",
        nargs=1,
        help="property file to be used for verification",
    )
    verify_network_parser.add_argument(
        "network",
        nargs=1,
        help="network file to be used for verification",
    )

    configure_algorithm_parser = subparsers.add_parser("configure_algorithm")
    configure_algorithm_parser.add_argument(
        "verifier",
        metavar="verifier",
        nargs=1,
        choices=get_all_complete_verifier_names(),
        help="verifier to be used for verification",
    )

    construct_portfolio_parser = subparsers.add_parser("construct_portfolio")

    execute_portfolio_parser = subparsers.add_parser("execute_portfolio")

    run_benchmark_perser = subparsers.add_parser("run_benchmark")

    return parser


def main():
    """Parse and process cli args."""
    parser = _build_arg_parser()
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    command = args.command

    if args.check_versions:
        check_commit_hashes()

    if command == "install":
        try_install_verifiers(args.verifier)
    elif command == "uninstall":
        try_uninstall_verifiers(args.verifier)
    elif command == "verify_network":
        verify_network(args.verifier[0], args.property[0], args.network[0])
    elif command == "configure_algorithm":
        configure_algorithm(args.verifier[0])
    elif command == "construct_portfolio":
        construct_portfolio("asda", "asasda")
    elif command == "execute_portfolio":
        execute_portfolio()
    elif command == "run_benchmark":
        run_benchmark()


if __name__ == "__main__":
    main()
