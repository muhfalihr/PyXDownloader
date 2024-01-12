import os

from PyXD.xdownloader import PyXDownloader
from PyXD.exception import *
from typing import Any
from argparse import ArgumentParser


def main(script_path: str) -> Any:
    path = os.path.dirname(script_path) + "/download"

    argument_parser = ArgumentParser(
        description="PyXDownloader is a tool used to download media from a specified username or link."
    )
    argument_parser.add_argument(
        "-func", "--function", type=str, dest="function", help="\"am | allmedia\", \"i | images\", \"ld | linkdownloader\"", required=True
    )
    argument_parser.add_argument(
        "-link", "--link", type=str, dest="link", help="Image or video link."
    )
    argument_parser.add_argument(
        "-p", "--path", type=str, dest="path", help="Path where to save photos or videos.", default=path
    )
    argument_parser.add_argument(
        "-sn", "--screenname", type=str, dest="screenname", help="Example: @screen_name but not included @."
    )
    argument_parser.add_argument(
        "-count", "--count", type=int, dest="count", help="The amount of data to be downloaded.", default=20
    )
    argument_parser.add_argument(
        "-cursor", "--cursor", type=str, dest="cursor", help="The key used to load the next page.", default=None
    )
    argument_parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0'
    )

    args = argument_parser.parse_args()

    cookie = ''  # Required
    PXD = PyXDownloader(cookie=cookie)

    match args.function:
        case "allmedia" | "am":
            PXD.allmedia(
                screen_name=args.screenname,
                path=args.path,
                count=args.count,
                cursor=args.cursor
            )

        case "images" | "i":
            PXD.images(
                screen_name=args.screenname,
                path=args.path,
                cursor=args.cursor
            )

        case "linkdownloader" | "ld":
            PXD.linkdownloader(
                link=args.link,
                path=args.path
            )

        case _:
            raise FunctionNotFoundError(
                f"Error! The function with the name '{args.function}' is not available."
            )
